import { graphql } from 'gatsby';
import React from 'react';
import styled from 'styled-components';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import { Events as evUtil } from '../utils';
import SearchButton from '../components/BaseComponents/SearchButton';
import useLoadingAllEvents from '../hooks/useLoadingEvents';

const HeaderWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

export default ({ data, location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();

  // use custom hook to check if it is loading
  const isLoading = useLoadingAllEvents(data.dataJson.data);

  // preprocess events before sending to events list
  const preprocessedEvents = evUtil.getPreprocessedEvents(
    data.dataJson.data,
    true,
  );

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Upcoming Events</h1>
        <SearchButton />
      </HeaderWrapper>
      <EventsContainer
        isLoading={isLoading}
        allEvents={preprocessedEvents}
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
