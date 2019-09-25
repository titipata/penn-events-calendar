import { graphql } from 'gatsby';
import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';
import useLocalStorage from '../hooks/useLocalStorage';
import { Events as evUtil } from '../utils';

export default ({ data }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();

  const [globalState] = useGlobal();

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;
  // filter only selected event to pass to container
  const selectedEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
  ).filter(
    x => selectedEventsIndexes.includes(x.node.event_index),
  );

  return (
    <Layout>
      <h1>Selected Events</h1>
      <EventsContainer
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
