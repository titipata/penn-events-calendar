import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Key } from '../../../Utils';
import EventItem from '../EventItem';

const StyledEventsList = styled.ul`
  list-style-type: none;
  margin: 0.5rem 0;
  padding: 0;
`;

const EventsList = ({ events }) => (
  <StyledEventsList>
    { events.map(ev =>
      <EventItem key={Key.getShortKey()} ev={ev} />)
    }
  </StyledEventsList>
);

EventsList.propTypes = {
  events: PropTypes.arrayOf(Object).isRequired,
};

export default EventsList;

