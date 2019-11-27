import os
import hug
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
from scipy.spatial.distance import cosine

from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search

# enable CORS
api = hug.API(__name__)
api.http.base_url = '/api'
api.http.add_middleware(hug.middleware.CORSMiddleware(api))

path_data = os.path.join('data', 'events.json')
path_vector = os.path.join('data', 'events_vector.json')
event_vectors = json.load(open(path_vector, 'r'))
events = json.load(open(path_data, 'r'))
events_map = {
    e['event_index']: e
    for e in events
}
event_vectors_map = {
    e['event_index']: e['event_vector']
    for e in event_vectors
}

# elasticsearch
es = Elasticsearch([
    {'host': 'localhost', 'port': 9200},
])
es_search = Search(using=es)


def get_future_event(date, days=0, hours=9):
    """
    Function to get future or recent events

    It returns True if the event happens before determined certain days and hours

    Input
    =====
    date: str, date string in '%d-%m-%Y'
    """
    try:
        if datetime.now() - timedelta(days=days, hours=hours) <= parser.parse(date, dayfirst=True, fuzzy=True):
            return True
        else:
            return False
    except:
        return False


@hug.post("/getevents")
def getevents(body):
    """
    Return full dataset for the given list of event indices
    Body is sent as JSON from the frontend with data as a value of a key 'payload':

    {
        "payload": data
    }

    """
    event_indices = body['payload']
    events_body = []
    for event_idx in event_indices:
        events_body.append(events_map[event_idx])
    return events_body


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
    n_recommendation = 25
    event_indices = body['payload']
    # in case frond-end sending index out of range
    event_indices = [event_idx for event_idx in event_indices
                     if int(event_idx) in event_vectors_map.keys()]

    if len(event_indices) == 0:
        return []

    pref_indices = [int(event_idx) for event_idx in event_indices]
    pref_vector = np.mean([np.array(event_vectors_map[idx])
                           for idx in pref_indices], axis=0)
    # get indices of event happens after current time
    future_event_indices = [e['event_index'] for e in filter(
        lambda r: get_future_event(r['date_dt']), events)]
    # rank indices by cosine distance and get indices
    relevances = np.array([
        cosine(pref_vector, np.array(event_vectors_map[idx]))
        for idx in future_event_indices
    ]).ravel()
    rank_indices = np.argsort(relevances)
    relevances = np.clip(np.sort(relevances)[
                         ::-1] * 100, 0, 100).astype(int)[0:n_recommendation]
    indices_recommendation = [future_event_indices[i]
                              for i in rank_indices][0:n_recommendation]

    recommendations = []
    for idx, rel in zip(indices_recommendation, relevances):
        recommendation = events_map[idx]
        recommendation['relevance'] = rel
        recommendations.append(recommendation)
    return recommendations


@hug.get("/query", examples="search_query=CNI")
def query(search_query: hug.types.text):
    """
    Search events from index,
    this function will return empty list if no events are found

    example query: http://localhost:8888/api/query?search_query=CNI

    See more query examples at: https://elasticsearch-dsl.readthedocs.io/en/latest/search_dsl.html
    """
    fields = ['title^2', 'owner^2', 'speaker^2', 'location^2', 'description']
    n_results = 30
    responses = es_search.query(
        "multi_match",
        query=search_query,
        fields=fields
    ).filter(
        'range',
        timestamp={
            'from': (datetime.now() - timedelta(hours=12)).strftime('%Y-%m-%dT%H:%M:%S'),
            'to': (datetime.now() + timedelta(weeks=50)).strftime('%Y-%m-%dT%H:%M:%S')
        })
    search_responses = responses[0:n_results].execute()
    search_responses = search_responses.to_dict()['hits']['hits']

    # return future events for a given query
    future_events, relevances = [], []
    for response in search_responses:
        event = response['_source']
        event['event_index'] = int(response['_id'])
        if 'suggest' in event:
            del event['suggest']
        future_events.append(event)
        relevances.append(response['_score'])
    relevances = [
        int(100 * (r / max(relevances)))
        for r in relevances
    ]  # normalize by the maximum relevance
    query_events = []
    for event, rel in zip(future_events, relevances):
        event['relevance'] = rel
        query_events.append(event)
    return query_events


@hug.get("/suggestion", examples="text=department")
def suggestion(text: hug.types.text):
    """
    For a given text, return possible terms from a suggest list in elastic search index

    example query: http://localhost:8888/api/suggestion?text=department
    """
    suggest_body = {
        "suggest": {
            "field-suggest": {
                "prefix": text,
                "completion": {
                    "field": "suggest"
                }
            }
        }
    }
    responses = es.search(index='penn-events', body=suggest_body)

    # return all possible full term from suggest list
    suggest_terms = []
    for response in responses['suggest']['field-suggest'][0]['options']:
        for s in response['_source']['suggest']:
            if text.lower() in s.lower():
                suggest_terms.append(s)
    return list(pd.unique(suggest_terms))


@hug.get("/pagination", examples="page=1")
def pagination(page: hug.types.number=1):
    """
    Get pagination of a given page

    example query: http://localhost:8888/api/pagination?page=1
    """

    search_responses = es_search.filter(
        'range',
        timestamp={
            'from': (datetime.utcnow().date() - timedelta(hours=1)).strftime('%Y-%m-%dT%H:%M:%S'),
            'to': (datetime.now() + timedelta(weeks=50)).strftime('%Y-%m-%dT%H:%M:%S')
        }
    ).sort("timestamp")

    query_events = []
    for response in search_responses[(page - 1) * 30: (page * 30)].execute().to_dict()['hits']['hits']:
        event = response['_source']
        if 'suggest' in event:
            del event['suggest']
        query_events.append(event)

    return query_events
