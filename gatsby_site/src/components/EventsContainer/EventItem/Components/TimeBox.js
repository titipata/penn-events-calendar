import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Datetime as dtutil } from '../../../../utils';

const DatetimeWrapper = styled.div`
  font-size: 2rem;
  align-items: center;
  justify-content: center;
  padding-left: 15px;
  display: flex;
  flex-direction: column;
  width: 5.5rem;
  min-width: 5.5rem;
`;

// const StyledDate = styled.div`
//   font-family: 'Source Code Pro';
//   padding: 0 3px;
// `;

const StyledTime = styled.div`
  text-align: center;
  font-size: 1rem;
  display: inline-flex;
`;

const TimeBox = ({ starttime, endtime }) => {
  let singleTime = null;
  let plusTime = null;
  if (starttime === endtime) {
    if (!starttime || !endtime) {
      singleTime = '-';
    } else if (starttime.includes('allday')) {
      singleTime = 'All day';
    } else {
      plusTime = dtutil.getAssumedEndtime(endtime);
    }
  }

  return (
    <DatetimeWrapper>
      {
        !singleTime
          ? (
            <React.Fragment>
              <StyledTime>
                {dtutil.getTime(starttime)}
              </StyledTime>
              <StyledTime>
                {plusTime || dtutil.getTime(endtime)}
              </StyledTime>
            </React.Fragment>
          )
          : <StyledTime>{singleTime}</StyledTime>
      }
    </DatetimeWrapper>
  );
};

TimeBox.propTypes = {
  starttime: PropTypes.string,
  endtime: PropTypes.string,
};

TimeBox.defaultProps = {
  starttime: null,
  endtime: null,
};

export default TimeBox;
