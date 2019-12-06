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

  // fetch selected events from saved indexes
  const [selectedEvents, isLoading] = useFetchEvents(
    '/api/getevents',
    selectedEventsIndexes,
  );

  // use a custom hook to get data
  const [currentPageEvents, totalPage, setCurrentPage] = usePagination(selectedEvents);

  return (
    <Layout>
      <h1>Selected Events</h1>
      <EventsContainer
        isLoading={isLoading}
        currentPageEvents={currentPageEvents}
        noEventDefaultText="You don't have selected events in your library."
        noOfPages={totalPage}
        handlePagination={(pageNo) => setCurrentPage(pageNo)}
      />
    </Layout>
  );
};
