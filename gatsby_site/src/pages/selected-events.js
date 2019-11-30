import React, { useState, useEffect } from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';
import useLocalStorage from '../hooks/useLocalStorage';
import useStaticResources from '../hooks/useStaticResources';
import useFetchEvents from '../hooks/useFetchEvents';

export default ({ data, location }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();
  const [globalState] = useGlobal();

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;

  // calculate and get correct events for each page before sending to render
  const [currentPageEvents, setCurrentPageEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);

  const [selectedEvents, isLoading] = useFetchEvents(
    '/api/getevents',
    selectedEventsIndexes,
  );

  useEffect(() => {
    const start = 0 + (30 * (currentPage - 1));
    const end = 30 + (30 * (currentPage - 1));

    setCurrentPageEvents(selectedEvents.slice(start, end));
  }, [currentPage, selectedEvents]);

  return (
    <Layout>
      <h1>Selected Events</h1>
      <EventsContainer
        isLoading={isLoading}
        currentPageEvents={currentPageEvents}
        noEventDefaultText="You don't have selected events in your library."
        noOfPages={Math.ceil(selectedEvents.length / 30)}
        handlePagination={pageNo => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
