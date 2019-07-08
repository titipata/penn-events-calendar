import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Datetime as dtutil } from '../../../../utils';

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

const TimeBox = ({ starttime, endtime }) => (
  <DatetimeWrapper>
    <StyledTime>
      {dtutil.getTime(starttime)}
      <br />
      -
      <br />
      {dtutil.getTime(endtime)}
    </StyledTime>
  </DatetimeWrapper>
);

TimeBox.propTypes = {
  starttime: PropTypes.string.isRequired,
  endtime: PropTypes.string.isRequired,
};

export default TimeBox;
