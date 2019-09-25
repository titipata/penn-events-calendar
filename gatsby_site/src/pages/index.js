import { library } from '@fortawesome/fontawesome-svg-core';
import {
  faBookmark, faCalendarAlt, faChevronCircleDown,
  faChevronCircleUp, faClock, faCopy, faExternalLinkAlt,
  faFileAlt, faMapMarkerAlt, faSchool,
  faStar, faUniversity, faUserTie,
} from '@fortawesome/free-solid-svg-icons';
import { graphql } from 'gatsby';
import React from 'react';
import EventsContainer from '../components/EventsContainer';
import Layout from '../components/layout';
import useLocalStorage from '../hooks/useLocalStorage';
import { Events as evUtil } from '../utils';
import 'rc-pagination/assets/index.css';

// add fa font to use
library.add(
  faCalendarAlt, faMapMarkerAlt, faClock, faFileAlt,
  faExternalLinkAlt, faUserTie, faSchool, faUniversity,
  faBookmark, faChevronCircleDown, faChevronCircleUp,
  faCopy, faStar,
);

export default ({ data }) => {
  // use this to retrieve data and rehydrate before globalState is used
  useLocalStorage();
  // preprocess events before sending to events list
  const preprocessedEvents = evUtil.getPreprocessedEvents(
    data.allEventsJson.edges,
    true,
  );

  return (
    <Layout>
      <h1>Upcoming Events</h1>
      <EventsContainer
        allEvents={preprocessedEvents}
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
