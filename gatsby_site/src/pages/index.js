import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faBookmark, faCalendarAlt, faChevronCircleDown,
  faChevronCircleUp, faClock, faCopy, faExternalLinkAlt,
  faFileAlt, faMapMarkerAlt, faSchool, faUniversity, faUserTie,
  faStar,
} from '@fortawesome/free-solid-svg-icons';
import { graphql } from 'gatsby';
import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';

// add fa font to use
library.add(
  faCalendarAlt, faMapMarkerAlt, faClock, faFileAlt,
  faExternalLinkAlt, faUserTie, faSchool, faUniversity,
  faBookmark, faChevronCircleDown, faChevronCircleUp,
  faCopy, faStar,
);

export default ({ data }) => {
  fetch('http://localhost:8888/recommendations', {
    method: 'POST',
    mode: 'cors',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      payload: [1, 2, 3, 4, 5],
    }),
  }).then(res => console.log(res.json()));

  return (
    <Layout>
      <h1>Upcoming Events</h1>
      <EventsContainer
        allEvents={data.allEventsJson.edges}
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
