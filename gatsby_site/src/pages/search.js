import React, { useEffect, useState } from 'react';
import styled from 'styled-components';
import SearchButton from '../components/BaseComponents/SearchButton';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useFetchEvents from '../hooks/useFetchEvents';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import usePagination from '../hooks/usePagination';

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

  // fetch events from search query
  const [searchResults, isLoading] = useFetchEvents(
    `/api/query?search_query=${searchQuery}}`,
  );

  // use a custom hook to get data
  const [currentPageEvents, totalPage, setCurrentPage] = usePagination(searchResults);

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
        noOfPages={totalPage}
        handlePagination={pageNo => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
