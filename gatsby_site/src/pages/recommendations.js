import { graphql } from 'gatsby';
import React, { useState, useEffect } from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useGlobal from '../store';
import useLocalStorage from '../hooks/useLocalStorage';
import { Events as evUtil } from '../utils';

export default ({ data }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();

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
        // stop here if there is no data
        if (!recommendedIndexes || recommendedIndexes.length === 0) {
          return;
        }

        const filteredData = evUtil.getPreprocessedEvents(data.allEventsJson.edges)
          .filter(
            event => recommendedIndexes.find(rec => rec.event_index === event.node.event_index),
          )
          // recommended events should contain relevance value:
          // {
          //   node: { `event_data` },
          //   relevance: `relevance_value`
          // }
          .reduce((acc, cur) => ([
            ...acc,
            {
              ...cur,
              relevance: recommendedIndexes.find(
                rec => rec.event_index === cur.node.event_index,
              ).relevance,
            },
          ]), []);

        // add to global state
        setRecommendedEvents(filteredData);
      })
      // eslint-disable-next-line
      .catch(err => console.log(err));
  }, [selectedEventsIndexes]);

  return (
    <Layout>
      <h1>Recommendations</h1>
      <EventsContainer
        allEvents={recommendedEvents}
        noEventDefaultText="Add some events to your library to see our recommendations."
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
