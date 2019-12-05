import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useFetchEvents from '../hooks/useFetchEvents';
import useLocalStorage from '../hooks/useLocalStorage';
import usePagination from '../hooks/usePagination';
import useStaticResources from '../hooks/useStaticResources';
import useGlobal from '../store';

export default () => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  useStaticResources();
  const [globalState] = useGlobal();

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;

  // fetch recommended events from saved indexes
  const [recommendedEvents, isLoading] = useFetchEvents(
    '/api/recommendations',
    selectedEventsIndexes,
  );

  // use a custom hook to get data
  const [currentPageEvents, totalPage, setCurrentPage] = usePagination(recommendedEvents);

  return (
    <Layout>
      <h1>Recommendations</h1>
      <EventsContainer
        isLoading={isLoading}
        currentPageEvents={currentPageEvents}
        noEventDefaultText="Add some events to your library to see your recommendations."
        noOfPages={totalPage}
        handlePagination={pageNo => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
