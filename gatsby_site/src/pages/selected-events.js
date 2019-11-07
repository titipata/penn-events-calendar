import React from 'react';
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

  const [selectedEvents, isLoading] = useFetchEvents(
    '/api/getevents',
    selectedEventsIndexes,
  );

  return (
    <Layout>
      <h1>Selected Events</h1>
      <EventsContainer
        isLoading={isLoading}
        allEvents={selectedEvents}
        noEventDefaultText="You don't have selected events in your library."
      />
    </Layout>
  );
};
