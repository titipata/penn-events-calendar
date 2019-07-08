// import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Events as evUtil, Key } from '../../utils';
// import EventsList from './EventsList';

const StyledSectionText = styled.div`
  font-family: 'Source Code Pro';
  font-size: 1.75rem;
  font-weight: bold;
  color: #222;
  padding-left: 1rem;
  /* text-align: center; */
`;

const EventsContainer = ({ events }) => {
  const groupedByDates = evUtil.groupByDate(events);

  return groupedByDates.map(grp => (
    <React.Fragment key={Key.getShortKey()}>
      <StyledSectionText>
        {/* <Fa icon="calendar-alt" /> */}
        &nbsp;
        <h2>{grp.dateFormatted}</h2>
      </StyledSectionText>
      {/* <EventsList
        events={grp.events}
        similarEvents={getSimilarEvents}
      /> */}
    </React.Fragment>
  ));
};

EventsContainer.propTypes = {
  events: PropTypes.arrayOf(Object).isRequired,
};

export default EventsContainer;
