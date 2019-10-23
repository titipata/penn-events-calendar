import { graphql } from 'gatsby';
import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';
import useLocalStorage from '../hooks/useLocalStorage';
import { Events as evUtil } from '../utils';
import useStaticResources from '../hooks/useStaticResources';
import useLoadingAllEvents from '../hooks/useLoadingEvents';

export default ({ data, location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();
  const [globalState] = useGlobal();

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;
  // filter only selected event to pass to container
  const selectedEvents = evUtil.getPreprocessedEvents(
    data.dataJson.data,
  ).filter(
    x => selectedEventsIndexes.includes(x.event_index),
  );

  // use custom hook to check if it is loading
  const isLoading = useLoadingAllEvents(data.dataJson.data);

  return (
    <Layout>
      <h1>Selected Events</h1>
      <EventsContainer
        isLoading={isLoading}
        allEvents={selectedEvents}
        noEventDefaultText="You don't have selected events in your library."
      />
    </Layout>
  );
};

export const query = graphql`
  query {
    dataJson {
      modified_date
      data {
        date_dt
        description
        endtime
        event_index
        location
        owner
        speaker
        starttime
        title
        url
      }
    }
  }
`;
