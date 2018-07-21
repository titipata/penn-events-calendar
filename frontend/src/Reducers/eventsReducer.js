import { fetchActions } from '../Actions';

const initialState = {
  allEvents: [],
  loading: false,
  similarEvents: [],
  error: null,
};

export default function eventsReducer(state = initialState, action) {
  switch (action.type) {
    case fetchActions.FETCH_EVENTS_BEGIN:
      // Mark the state as "loading" so we can show a spinner or something
      // Also, reset any errors. We're starting fresh.
      return {
        ...state,
        loading: true,
        error: null,
      };

    case fetchActions.FETCH_EVENTS_SUCCESS:
      // All done: set loading "false".
      // Also, replace the items with the ones from the server
      return {
        ...state,
        loading: false,
        allEvents: action.events,
      };

    case fetchActions.FETCH_EVENTS_FAILURE:
      // The request failed, but it did stop, so set loading to "false".
      // Save the error, and we can display it somewhere
      // Since it failed, we don't have items to display anymore, so set it empty.
      // This is up to you and your app though: maybe you want to keep the items
      // around! Do whatever seems right.
      return {
        ...state,
        loading: false,
        error: action.error,
        allEvents: [],
      };

    case fetchActions.FETCH_SIMILAR_EVENTS:
      return {
        ...state,
        similarEvent: action.similarEvents,
      };

    default:
      // ALWAYS have a default case in a reducer
      return state;
  }
}
