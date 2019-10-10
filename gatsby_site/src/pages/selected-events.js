import { graphql } from 'gatsby';
import React, { useEffect } from 'react';
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
  // this is used to set origin hostname
  const [globalState, globalActions] = useGlobal();

  useEffect(() => {
    globalActions.setHostName(location.hostname);
  }, [globalActions, location.hostname]);

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;
  // filter only selected event to pass to container
  const selectedEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
  ).filter(
    x => selectedEventsIndexes.includes(x.node.event_index),
  );

  // use custom hook to check if it is loading
  const isLoading = useLoadingAllEvents(selectedEvents);

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
    allEventsJson {
      edges {
        node {
          id
          event_index
          date_dt
          title
          description
          starttime
          endtime
          speaker
          owner
          location
          url
        }
      }
    }
  }
`;
