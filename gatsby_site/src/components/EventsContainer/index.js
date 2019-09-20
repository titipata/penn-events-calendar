import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Events as evUtil, Key } from '../../utils';
import EventList from './EventList';

const StyledContainer = styled.div`
  margin-bottom: 2rem;
`;

const StyledSectionText = styled.div`
  padding-left: 1rem;
  /* text-align: center; */
`;

const StyledH2 = styled.h2`
  font-size: 1.75rem;
  font-weight: normal;
  color: #333;
  margin: 1rem 0;
`;

const EventsContainer = ({ allEvents }) => {
  // render no data screen
  if (allEvents.length === 0) {
    return (
      <StyledContainer>
        <p>No available events!</p>
      </StyledContainer>
    );
  }

  // group event by date before rendering
  const groupedByDates = evUtil.groupByDate(allEvents);

  return groupedByDates.map(grp => (
    <StyledContainer key={Key.getShortKey()}>
      <StyledSectionText>
        <StyledH2>
          <Fa icon="calendar-alt" />
          &nbsp;&nbsp;
          {grp.dateFormatted}
        </StyledH2>
      </StyledSectionText>
      <EventList
        groupedEvents={grp.events}
      />
    </StyledContainer>
  ));
};

EventsContainer.propTypes = {
  allEvents: PropTypes.arrayOf(Object).isRequired,
};

export default EventsContainer;
