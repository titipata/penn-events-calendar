import { API } from '../Data';

export const fetchActions = {
  FETCH_EVENTS_BEGIN: 'FETCH_EVENTS_BEGIN',
  FETCH_EVENTS_SUCCESS: 'FETCH_EVENTS_SUCCESS',
  FETCH_EVENTS_FAILURE: 'FETCH_EVENTS_FAILURE',
  FETCH_SIMILAR_EVENTS: 'FETCH_SIMILAR_EVENTS',
};

const fetchEvents = () => (dispatch) => {
  // dispatch begin fetching action
  dispatch({ type: fetchActions.FETCH_EVENTS_BEGIN });

  // fetching events
  fetch(API.getEvent())
    .then(API.handleErrors)
    .then(res => res.json())
    .then((resJson) => {
      // success getting events
      dispatch({
        type: fetchActions.FETCH_EVENTS_SUCCESS,
        events: resJson,
      });
    })
    .catch((error) => {
      dispatch({ type: fetchActions.FETCH_EVENTS_FAILURE, error });
      console.log(`[ERROR] failed fetching events: ${error}`);
    });
};

const fetchSimilarEvents = eventId => (dispatch) => {
  fetch(API.getSimilarEvents(eventId))
    .then(API.handleErrors)
    .then(res => res.json())
    .then((resJson) => {
      dispatch({
        type: fetchActions.FETCH_SIMILAR_EVENTS,
        similarEvents: {
          id: eventId,
          data: resJson,
        },
      });
    })
    .catch((error) => {
      dispatch({ type: fetchActions.FETCH_EVENTS_FAILURE, error });
      console.log(`[ERROR] failed fetching similar events: ${error}`);
    });
};

export {
  fetchEvents,
  fetchSimilarEvents,
};

