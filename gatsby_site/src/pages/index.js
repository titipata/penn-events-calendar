import React, { useState, useEffect } from 'react';
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

export default () => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();

  // local state
  const [isLoading, setIsLoading] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const [fetchedData, setFetchedData] = useState({});
  const [currentPageEvents, setCurrentPageEvents] = useState([]);

  useEffect(() => {
    setIsLoading(true);
    fetch(`/api/pagination?page=${currentPage}`)
      .then(res => res.json())
      .then((resJson) => {
        setFetchedData(resJson);
        setIsLoading(false);
      });
  }, [currentPage]);

  useEffect(() => {
    if (fetchedData.data) {
      // preprocess events before sending to events list
      const preprocessedEvents = evUtil.getPreprocessedEvents(
        fetchedData.data
          // TODO: this filter step is supposed to be done on backend
          .filter(x => x.title)
          .map(x => ({ node: x })),
        true,
      );

      // set to local state
      setCurrentPageEvents(preprocessedEvents);
    }
  }, [fetchedData.data]);

  return (
    <Layout>
      <HeaderWrapper>
        <h1>Upcoming Events</h1>
        <SearchButton />
      </HeaderWrapper>
      <EventsContainer
        isLoading={isLoading}
        allEvents={currentPageEvents}
        handlePagination={pageNo => setCurrentPage(pageNo)}
        noOfPages={fetchedData.total}
        currentPageEvents={currentPageEvents}
      />
    </Layout>
  );
};
