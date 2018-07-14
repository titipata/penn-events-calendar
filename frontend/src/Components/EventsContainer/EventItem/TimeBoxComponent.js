import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Datetime as dtutil } from '../../../Utils';

const DatetimeWrapper = styled.div`
  font-size: 2rem;
  align-items: center;
  justify-content: center;
  padding: 0 20px;
  display: flex;
  flex-direction: column;
`;

// const StyledDate = styled.div`
//   font-family: 'Source Code Pro';
//   padding: 0 3px;
// `;

const StyledTime = styled.div`
  text-align: center;
  font-size: 0.75rem;
  display: inline-flex;
`;

const StyledTimeIcon = styled.div`
  align-self: center;
  padding-right: 7px;
  font-size: 0.95rem;
`;

const TimeBox = ({ eventStartTime, eventEndTime }) => (
  <DatetimeWrapper>
    <StyledTime>
      <StyledTimeIcon>
        <Fa icon="clock" />
      </StyledTimeIcon>
      {dtutil.getTime(eventStartTime)}
      <br />
      {dtutil.getTime(eventEndTime)}
    </StyledTime>
  </DatetimeWrapper>
);

TimeBox.propTypes = {
  // eventDate: PropTypes.string.isRequired,
  eventStartTime: PropTypes.string.isRequired,
  eventEndTime: PropTypes.string.isRequired,
};

export default TimeBox;
