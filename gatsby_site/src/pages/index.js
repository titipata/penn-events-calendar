import { graphql } from 'gatsby';
import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import { Events as evUtil } from '../utils';

export default ({ data }) => {
  // load static resources
  useStaticResources();
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();

  // preprocess events before sending to events list
  const preprocessedEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
    true,
  );

  return (
    <Layout>
      <h1>Upcoming Events |Search Icon|</h1>
      <EventsContainer
        allEvents={preprocessedEvents}
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
