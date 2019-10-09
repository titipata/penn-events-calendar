import json
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dateutil.parser import parse
from tqdm import tqdm


es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])
INDEX_NAME = 'penn-events'


def generate_event(events):
    """
    For a given list of events, yield event for inserting to elasticsearch
    """
    for event in events:
        try:
            timestamp = parse(
                event['date_dt'] + ' ' + event['starttime'], dayfirst=True)
        except:
            timestamp = datetime.now()
        event['timestamp'] = timestamp
        event['date'] = timestamp.strftime("%B %d %Y")
        event_add = {
            k: event[k] for k in
            ('date', 'timestamp', 'location',
             'starttime', 'endtime', 'owner',
             'speaker', 'title', 'description',
             'url', 'speaker', 'summary')
        }
        yield {
            "_index": "penn-events",
            "_type": "event",
            "_id": event['event_index'],
            "_source": event_add
        }


# define custom analyzer and map to index
# https://blog.bitsrc.io/how-to-build-an-autocomplete-widget-with-react-and-elastic-search-dd4f846f784
settings = {
    "settings": {
        "index": {
            "analysis": {
                "filter": {},
                "analyzer": {
                    "analyzer_keyword": {
                        "tokenizer": "keyword",
                        "filter": "lowercase"
                    },
                    "edge_ngram_analyzer": {
                        "filter": [
                            "lowercase"
                        ],
                        "tokenizer": "edge_ngram_tokenizer"
                    }
                },
                "tokenizer": {
                    "edge_ngram_tokenizer": {
                        "type": "edge_ngram",
                        "min_gram": 2,
                        "max_gram": 5,
                        "token_chars": [
                            "letter"
                        ]
                    }
                }
            }
        }
    },
    "mappings": {
        "event": {
            "properties": {
                "suggest": {
                    "type": "completion"
                },
                "title": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                },
                "description": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                },
                "owner": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                },
                "speaker": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                },
                "location": {
                    "type": "text",
                    "analyzer": "edge_ngram_analyzer"
                }
            }
        }
    }
}


def index_events_elasticsearch():
    print('Indexing events to ElasticSearch...')
    events = json.loads(open('data/events.json', 'r').read())
    events = pd.DataFrame(events).fillna('').to_dict(orient='records')

    es.indices.delete(index=INDEX_NAME, ignore=[
                      400, 404])  # delete current index
    # add settings to es indices client
    # include_type_name is very important!
    # also dont ignore 400, 404 here to know what the error is
    es.indices.create(index=INDEX_NAME,
                      body=settings,
                      include_type_name=True)

    # insert all events to elasticsearch
    helpers.bulk(es, generate_event(events))
    print('Done indexing events to ElasticSearch!')

    print('Updating elasticsearch index...\n')
    events_feature = json.loads(open('data/events_vector.json', 'r').read())
    events_feature_df = pd.DataFrame(events_feature).fillna('')
    for _, r in tqdm(
        events_feature_df.iterrows(),
        total=len(events_feature_df.index)
    ):
        es.update(
            index='penn-events',
            id=r['event_index'],
            doc_type='event',
            body={
                'doc': {
                    'suggest': r['suggest_candidates']
                }
            },
            refresh=True,
        )
    print('\nDone updating search keywords to ElasticSearch!')


if __name__ == '__main__':
    index_events_elasticsearch()
