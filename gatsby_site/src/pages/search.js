import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import SearchButton from '../components/BaseComponents/SearchButton';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useFetchEvents from '../hooks/useFetchEvents';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';

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

export default ({ location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();

  const [searchQuery, setSearchQuery] = useState('');

  // handle effect for searchQuery
  useEffect(() => {
    setSearchQuery(decodeURI(parseQueryString(location.search).search_query));
  }, [location.search]);

  // calculate and get correct events for each page before sending to render
  const [currentPageEvents, setCurrentPageEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const [searchResults, isLoading] = useFetchEvents(
    `/api/query?search_query=${searchQuery}}`,
  );

  useEffect(() => {
    const start = 0 + (30 * (currentPage - 1));
    const end = 30 + (30 * (currentPage - 1));

    setCurrentPageEvents(searchResults.slice(start, end));
  }, [currentPage, searchResults]);

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
        currentPageEvents={currentPageEvents}
        noEventDefaultText={`Sorry, there are no events matched from your search query "${searchQuery}".`}
        noOfPages={Math.ceil(searchResults.length / 30)}
        handlePagination={pageNo => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
