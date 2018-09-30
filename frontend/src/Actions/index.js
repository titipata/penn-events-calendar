import { API } from '../Data';

export const fetchActions = {
  FETCH_EVENTS_BEGIN: 'FETCH_EVENTS_BEGIN',
  FETCH_EVENTS_SUCCESS: 'FETCH_EVENTS_SUCCESS',
  FETCH_EVENTS_FAILURE: 'FETCH_EVENTS_FAILURE',
  FETCH_SIMILAR_EVENTS: 'FETCH_SIMILAR_EVENTS',
  GET_EVENT_DETAILS: 'GET_EVENT_DETAILS',
};

export const visibilityActions = {
  TOGGLE_VISIBILITY: 'TOGGLE_VISIBILITY',
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
  console.log('GETTING similar for id:', eventId);
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
    }, () => console.log(`fail fetching similar events for id: ${eventId}!`))
    .catch((error) => {
      dispatch({ type: fetchActions.FETCH_EVENTS_FAILURE, error });
      console.log(`[ERROR] failed fetching similar events: ${error}`);
    });
};

const getEventDetails = eventId => (dispatch, getState) => {
  // what to do to get event detail of this id
  // 1 get description of this id
  // 2 get similar events of this id
  // 3 set visibility of detail of this id
  const { events } = getState();
  const thisId = events.allEvents.find(ev => ev.event_id === eventId);
  const description = thisId && thisId.description ? thisId.description : null;

  console.log('GETTING event detail for id:', eventId);
  fetch(API.getSimilarEvents(eventId))
    .then(API.handleErrors)
    .then(res => res.json())
    .then((resJson) => {
      dispatch({
        type: fetchActions.FETCH_SIMILAR_EVENTS,
        eventDetails: {
          id: eventId,
          similarEvents: resJson,
          description,
          visible: false,
        },
      });
    })
    .catch((error) => {
      dispatch({ type: fetchActions.FETCH_EVENTS_FAILURE, error });
      console.log(`[ERROR] failed fetching similar events: ${error}`);
    });
};

const toggleEventDetail = eventId => ({
  type: visibilityActions.TOGGLE_VISIBILITY,
  id: eventId,
});

export {
  fetchEvents,
  fetchSimilarEvents,
  getEventDetails,
  toggleEventDetail,
};

