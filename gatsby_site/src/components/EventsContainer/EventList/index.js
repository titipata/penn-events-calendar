import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Key } from '../../../utils';
import EventItem from '../EventItem';

const StyledEventsList = styled.ul`
  list-style-type: none;
  margin: 0.5rem 0;
  padding: 0;
`;

const EventsList = ({ groupedEvents }) => (
  <StyledEventsList>
    {
      groupedEvents.map(ev => (
        <EventItem
          key={Key.getShortKey()}
          eventData={ev}
        />
      ))
    }
  </StyledEventsList>
);

EventsList.propTypes = {
  groupedEvents: PropTypes.arrayOf(Object).isRequired,
};

export default EventsList;
