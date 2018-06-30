export const FETCH_EVENTS_BEGIN = 'FETCH_EVENTS_BEGIN';
export const FETCH_EVENTS_SUCCESS = 'FETCH_EVENTS_SUCCESS';
export const FETCH_EVENTS_FAILURE = 'FETCH_EVENTS_FAILURE';

export const fetchEventsBegin = () => ({
  type: FETCH_EVENTS_BEGIN,
});

export const fetchEventsSuccess = events => ({
  type: FETCH_EVENTS_SUCCESS,
  payload: { events },
});

export const fetchEventsError = error => ({
  type: FETCH_EVENTS_FAILURE,
  payload: { error },
});
