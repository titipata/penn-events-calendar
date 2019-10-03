import { graphql } from 'gatsby';
import React, { useEffect } from 'react';
import styled from 'styled-components';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import { Events as evUtil } from '../utils';
import SearchButton from '../components/BaseComponents/SearchButton';
import useGlobal from '../store';

const HeaderWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

export default ({ data, location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();
  // this is used to set origin hostname
  const [, globalActions] = useGlobal();

  useEffect(() => {
    globalActions.setHostName(location.hostname);
  }, [globalActions, location.hostname]);

  // preprocess events before sending to events list
  const preprocessedEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
    true,
  );

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Upcoming Events</h1>
        <SearchButton />
      </HeaderWrapper>
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
