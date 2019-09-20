import { graphql } from 'gatsby';
import React, { useState, useEffect } from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';

export default ({ data }) => {
  const [globalState] = useGlobal();
  const [recommendedEvents, setRecommendedEvents] = useState([]);

  // get selected event indexes from global state
  const { selectedEvents: selectedEventsIndexes } = globalState;

  useEffect(() => {
    fetch('http://localhost:8888/recommendations', {
      method: 'POST',
      mode: 'cors',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        payload: selectedEventsIndexes,
      }),
    })
      .then(res => res.json())
      .then((recommendedIndexes) => {
        const filteredData = data.allEventsJson.edges.filter(
          x => recommendedIndexes.includes(x.node.event_index),
        );
        setRecommendedEvents(filteredData);
      })
      // eslint-disable-next-line
      .catch(err => console.log(err));
  }, selectedEventsIndexes);

  return (
    <Layout>
      <h1>Recommendations</h1>
      <EventsContainer
        allEvents={recommendedEvents}
      />
    </Layout>
  );
};

export const query = graphql`
  query {
    allEventsJson {
      edges {
        node {
          id
          event_index
          date_dt
          title
          description
          starttime
          endtime
          speaker
          owner
          location
          url
        }
      }
    }
  }
`;
