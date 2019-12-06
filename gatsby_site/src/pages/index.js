import React from 'react';
import styled from 'styled-components';
import SearchButton from '../components/BaseComponents/SearchButton';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import usePagination from '../hooks/usePagination';
import useStaticResources from '../hooks/useStaticResources';

const HeaderWrapper = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

export default () => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();

  // use a custom hook to get data
  const [currentPageEvents, totalPage, setCurrentPage, isLoading] = usePagination();

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Upcoming Events</h1>
        <SearchButton />
      </HeaderWrapper>
      <EventsContainer
        isLoading={isLoading}
        allEvents={currentPageEvents}
        handlePagination={(pageNo) => setCurrentPage(pageNo)}
        noOfPages={totalPage}
        currentPageEvents={currentPageEvents}
      />
    </Layout>
  );
};
