import { graphql } from 'gatsby';
import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import { Events as evUtil } from '../utils';
import SearchButton from '../components/BaseComponents/SearchButton';
// import SearchButton from '../components/BaseComponents/SearchButton';

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
  // load static resources
  useStaticResources();
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();

  const [searchQuery, setSearchQuery] = useState('');
  const [searchResultsIndexes, setSearchResultsIndexes] = useState([]);

  getSearchResults();

  useEffect(() => {
    if (!searchQuery) {
      setSearchQuery(decodeURI(parseQueryString(location.search).search_query));
    }

    if (searchResultsIndexes.length === 0) {
      getSearchResults(`http://${location.hostname}:8888/query?search_query=${searchQuery}}`, x => setSearchResultsIndexes(x));
    }
  }, [location.hostname, location.search, searchQuery, searchResultsIndexes]);

  // filter only selected event to pass to container
  const searchResultEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
  ).filter(
    x => searchResultsIndexes.includes(x.node.event_index),
  );

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Search Results</h1>
        {/* need to fix dont redirect */}
        <SearchButton />
      </HeaderWrapper>
      <p>
        <BoldText>Results for</BoldText>
        {` ${searchQuery}`}
      </p>
      <EventsContainer
        allEvents={searchResultEvents}
        noEventDefaultText={`Sorry, there are no events matched from your search query "${searchQuery}".`}
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
