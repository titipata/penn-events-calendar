import { API } from '../Data';

export const fetchActions = {
  FETCH_EVENTS_BEGIN: 'FETCH_EVENTS_BEGIN',
  FETCH_EVENTS_SUCCESS: 'FETCH_EVENTS_SUCCESS',
  FETCH_EVENTS_FAILURE: 'FETCH_EVENTS_FAILURE',
  FETCH_SIMILAR_EVENTS: 'FETCH_SIMILAR_EVENTS',
};

const fetchEventsBegin = () => ({
  type: fetchActions.FETCH_EVENTS_BEGIN,
});

const fetchEventsSuccess = events => ({
  type: fetchActions.FETCH_EVENTS_SUCCESS,
  events,
});

const fetchEventsError = error => ({
  type: fetchActions.FETCH_EVENTS_FAILURE,
  error,
});

const fetchSimilarEvents = eventId => (dispatch) => {
  fetch(API.getSimilarEvents(eventId))
    .then(res => res.json())
    .then((resJson) => {
      dispatch({
        type: fetchActions.FETCH_SIMILAR_EVENTS,
        similarEvents: resJson,
      });
    })
    .catch((error) => {
      console.log(`[ERROR] failed fetching similar events: ${error}`);
    });
};

export {
  fetchEventsBegin,
  fetchEventsSuccess,
  fetchEventsError,
  fetchSimilarEvents,
};

