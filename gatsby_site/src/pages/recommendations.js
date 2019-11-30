import React, { useEffect, useState } from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import useFetchEvents from '../hooks/useFetchEvents';

export default () => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();
  const [globalState] = useGlobal();

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;

  // calculate and get correct events for each page before sending to render
  const [currentPageEvents, setCurrentPageEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const [recommendedEvents, isLoading] = useFetchEvents(
    '/api/recommendations',
    selectedEventsIndexes,
  );

  useEffect(() => {
    const start = 0 + (30 * (currentPage - 1));
    const end = 30 + (30 * (currentPage - 1));

    setCurrentPageEvents(recommendedEvents.slice(start, end));
  }, [currentPage, recommendedEvents]);

  return (
    <Layout>
      <h1>Recommendations</h1>
      <EventsContainer
        isLoading={isLoading}
        currentPageEvents={currentPageEvents}
        noEventDefaultText="Add some events to your library to see your recommendations."
        noOfPages={Math.ceil(recommendedEvents.length / 30)}
        handlePagination={pageNo => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
