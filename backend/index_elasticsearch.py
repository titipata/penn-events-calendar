import json
import pandas as pd
from elasticsearch import Elasticsearch, helpers
from datetime import datetime
from dateutil.parser import parse


es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])
INDEX_NAME = 'penn-events'


def generate_event(events):
    """
    Yield event for inserting to elasticsearch
    """
    for event in events:
        try:
            event['timestamp'] = parse(
                event['date_dt'] + ' ' + event['starttime'], dayfirst=True)
        except:
            event['timestamp'] = datetime.now()
        event_add = {
            k: event[k] for k in
            ('date_dt', 'timestamp', 'location',
             'starttime', 'endtime', 'owner',
             'speaker', 'title', 'description',
             'url', 'speaker', 'summary')
        }
        yield {
            "_index": "penn-events",
            "_type": "doc",
            "_id": event['event_index'],
            "_source": event_add
        }


if __name__ == '__main__':
    print('Indexing events to ElasticSearch...')
    events = json.loads(open('data/events.json', 'r').read())
    events = pd.DataFrame(events).fillna('').to_dict(orient='records')

    es.indices.delete(index=INDEX_NAME, ignore=[
                      400, 404])  # delete current index
    # insert all events to elasticsearch
    helpers.bulk(es, generate_event(events))
    print('Done indexing events to ElasticSearch!')
