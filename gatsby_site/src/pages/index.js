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

export default ({ data }) => (
  <Layout>
    <h1>Upcoming Events</h1>
    <EventsContainer
      allEvents={data.allEventsCsv.edges}
    />
  </Layout>
);

export const query = graphql`
  query {
    allEventsCsv {
      edges {
        node {
          id
          date_dt
          title
          description
          starttime_dt
          endtime_dt
          speaker
          owner
          location
          url
        }
      }
    }
  }
`;
