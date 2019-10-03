import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled, { css } from 'styled-components';
import { Datetime as dtutil } from '../../../../utils';
import useGlobal from '../../../../store';
import SvgVerticalGradient from '../../../BaseComponents/SvgVerticalGradient';

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

const SubWrapper = styled.div`
  display: flex;
  flex: 1;
  justify-content: center;
  align-items: center;
`;

const StyledTime = styled.div`
  text-align: center;
  font-size: 1rem;
  display: inline-flex;
`;

const starColor = {
  normal: '#eee',
  selected: 'orange',
  relevance: '#3dd',
};

const StyledFavIcon = styled(Fa).attrs(() => ({
  icon: 'star',
}))`
  color: ${props => (props.checked ? starColor.selected : starColor.normal)};
  font-size: 1.75rem;
  /* refer to the id of svg  */
  ${props => props.relevance && !props.checked && css`
    path {
      fill: url(#${`lgrad-${props.relevance}`});
    }
  `}
`;

const TimeBox = ({
  starttime, endtime, eventIndex, relevance,
}) => {
  const [globalState, globalActions] = useGlobal();

  // destructuring state to use
  const { selectedEvents } = globalState;

  // destructuring actions to use
  const { toggleSelectedEvent } = globalActions;

  let singleTime = null;
  if (starttime === endtime) {
    if (!starttime || !endtime) {
      singleTime = '-';
    } else if (starttime.includes('(All day)')) {
      singleTime = 'All day';
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
                {endtime ? dtutil.getTime(endtime) : null}
              </StyledTime>
            </React.Fragment>
          )
          : <StyledTime>{singleTime}</StyledTime>
      }
      <SubWrapper
        onClick={(e) => {
          // set global state
          toggleSelectedEvent(eventIndex);
          // block this because if the item has
          // description this will propagate
          // through invoke showing description
          e.stopPropagation();
        }}
      >
        <SvgVerticalGradient
          fillColor={starColor.relevance}
          bgColor={starColor.normal}
          fillPercent={relevance}
        />
        <StyledFavIcon
          checked={selectedEvents.includes(eventIndex)}
          relevance={relevance}
        />
      </SubWrapper>
    </DatetimeWrapper>
  );
};

TimeBox.propTypes = {
  starttime: PropTypes.string,
  endtime: PropTypes.string,
  eventIndex: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]),
  relevance: PropTypes.oneOfType([
    PropTypes.number,
    PropTypes.string,
  ]),
};

TimeBox.defaultProps = {
  starttime: null,
  endtime: null,
  eventIndex: null,
  relevance: null,
};

export default TimeBox;
