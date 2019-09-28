import hug
import json
import numpy as np
from datetime import datetime
from scipy.spatial.distance import cosine

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

# enable CORS
api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api))


path_data, path_vector = 'data/events.json', 'data/events_vector.json'
event_vectors = json.load(open(path_vector, 'r'))
events = json.load(open(path_data, 'r'))
event_vectors_map = {e['event_index']: e['event_vector']
                     for e in event_vectors}


# elasticsearch
es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])
es_search = Search(using=es)


def get_future_event(date):
    """
    Function return True if the event happens after now
    """
    try:
        if datetime.strptime(date, '%d-%m-%Y') > datetime.now():
            return True
        else:
            return False
    except:
        return False


@hug.post("/recommendations")
def recommendations(body):
    """
    Suggest event from a given comma separated indices.
    Body is sent as JSON from the frontend with data as a value of a key 'payload':

    {
        "payload": data
    }

    The body is then passed as an argument to this function, as a dictionary.
    """
    event_indices = body['payload']

    if len(event_indices) == 0:
        return []

    pref_indices = [int(event_idx) for event_idx in event_indices]
    pref_vector = np.mean([np.array(event_vectors_map[idx])
                           for idx in pref_indices], axis=0)
    # get indices of event happens after current time
    future_event_indices = [e['event_index'] for e in
                            filter(lambda r: get_future_event(r['date_dt']), events)]

    # rank indices by cosine distance and get indices
    rank_indices = np.argsort([cosine(pref_vector, event_vectors_map[idx])
                               for idx in future_event_indices])[0:20]
    indices_recommendation = [future_event_indices[i] for i in rank_indices]
    return indices_recommendation


@hug.get("/query", examples="search_query=CNI")
def query(search_query: hug.types.text):
    """
    Search events from index,
    this function will return empty list if no events are found

    example query: http://localhost:8888/query?search_query=CNI

    See more query examples at: https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
    """
    fields = ['title', 'description', 'owner', 'speaker', 'location']
    responses = es_search.query(
        "multi_match",
        query=search_query,
        fields=fields
    )
    search_responses = [r.to_dict() for r in responses[0:40].execute()]
    return search_responses
