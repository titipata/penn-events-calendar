import { graphql } from 'gatsby';
import React, { useEffect, useState } from 'react';
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

const BoldText = styled.span`
  font-weight: bold;
`;

const parseQueryString = (searchString) => {
  const [, key, val] = searchString.match(/([a-zA-Z0-9_]+)=(.+)/);

  return {
    [key]: val,
  };
};

const getSearchResults = (requestUrl, callback) => {
  if (!requestUrl) return;
  fetch(requestUrl)
    .then(res => res.json())
    .then((resJson) => {
      callback(resJson);
    })
    .catch(err => console.warn(err));
};

export default ({ data, location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResultIndexes, setSearchResultIndexes] = useState([]);
  const [searchResultEvents, setSearchResultEvents] = useState([]);

  // handle effect for searchQuery
  useEffect(() => {
    setSearchQuery(decodeURI(parseQueryString(location.search).search_query));
  }, [location.search]);

  // for searchResultsIndexes
  useEffect(() => {
    getSearchResults(`/api/query?search_query=${searchQuery}}`, x => setSearchResultIndexes(x));
  }, [searchQuery]);

  // for searchResultsEvents
  useEffect(() => {
    // filter only selected event to pass to container
    const filteredEvent = evUtil.getPreprocessedEvents(data.dataJson.data)
      .filter(
        event => searchResultIndexes.find(sri => sri.event_index === event.event_index),
      )
      // recommended events should contain relevance value:
      // {
      //   node: { `event_data` },
      //   relevance: `relevance_value`
      // }
      .reduce((acc, cur) => ([
        ...acc,
        {
          ...cur,
          relevance: searchResultIndexes.find(
            rec => rec.event_index === cur.event_index,
          ).relevance,
        },
      ]), []);

    setSearchResultEvents(filteredEvent);
  }, [data.dataJson.data, searchResultIndexes]);

  // use custom hook to check if it is loading
  const isLoading = useLoadingAllEvents(searchResultEvents);

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Search Results</h1>
        <SearchButton />
      </HeaderWrapper>
      <p>
        <BoldText>Search results for</BoldText>
        {` ${searchQuery}`}
      </p>
      <EventsContainer
        isLoading={isLoading}
        allEvents={searchResultEvents}
        noEventDefaultText={`Sorry, there are no events matched from your search query "${searchQuery}".`}
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
