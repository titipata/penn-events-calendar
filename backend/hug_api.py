import hug
import json
import numpy as np
from datetime import datetime
from scipy.spatial.distance import cosine

# enable CORS
api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api))


path_data, path_vector = 'data/events.json', 'data/events_vector.json'
event_vectors = json.load(open(path_vector, 'r'))
events = json.load(open(path_data, 'r'))
event_vectors_map = {e['event_index']: e['event_vector']
                     for e in event_vectors}


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
