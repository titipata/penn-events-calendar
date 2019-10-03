import { graphql } from 'gatsby';
import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import { Events as evUtil } from '../utils';
import SearchButton from '../components/BaseComponents/SearchButton';

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
  const [searchResultIndexes, setSearchResultIndexes] = useState([]);
  const [searchResultEvents, setSearchResultEvents] = useState([]);

  // handle effect for searchQuery
  useEffect(() => {
    setSearchQuery(decodeURI(parseQueryString(location.search).search_query));
  }, [location.search]);

  // for searchResultsIndexes
  useEffect(() => {
    getSearchResults(`http://${location.hostname}:8888/query?search_query=${searchQuery}}`, x => setSearchResultIndexes(x));
  }, [location.hostname, searchQuery]);

  // for searchResultsEvents
  useEffect(() => {
    // filter only selected event to pass to container
    const filteredEvent = evUtil.getPreprocessedEvents(data.allEventsJson.edges)
      .filter(
        event => searchResultIndexes.find(sri => sri.event_index === event.node.event_index),
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
            rec => rec.event_index === cur.node.event_index,
          ).relevance,
        },
      ]), []);

    console.log('filteredEvent:', filteredEvent);

    setSearchResultEvents(filteredEvent);
  }, [data.allEventsJson.edges, searchResultIndexes]);

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
