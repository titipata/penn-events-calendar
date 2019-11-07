import React from 'react';
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

  const [recommendedEvents, isLoading] = useFetchEvents(
    '/api/recommendations',
    selectedEventsIndexes,
  );

  return (
    <Layout>
      <h1>Recommendations</h1>
      <EventsContainer
        isLoading={isLoading}
        allEvents={recommendedEvents}
        noEventDefaultText="Add some events to your library to see your recommendations."
      />
    </Layout>
  );
};
