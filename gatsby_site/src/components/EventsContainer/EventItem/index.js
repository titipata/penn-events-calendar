import PropTypes from 'prop-types';
import React, { useState } from 'react';
import styled from 'styled-components';
import ContentBox from './Components/ContentBox';
import TimeBox from './Components/TimeBox';
import DescriptionBox from './Components/DescriptionBox';
import { getRandomColorFromText } from '../../../utils';

const StyledListItem = styled.li`
  margin-bottom: 5px;
  padding: 10px 0;
  border: 1px solid #eee;
  border-left: 5px solid ${props => props.color};
  border-radius: 5px;
  cursor: ${props => (props.cursorPointer ? 'pointer' : 'default')};
`;

const StyledContentWrapper = styled.div`
  display: flex;
  flex-direction: row;
`;

const EventItem = ({ eventData }) => {
  // define local hook
  const [
    descriptionVisible,
    setDescriptionVisible,
  ] = useState(false);

  // destructuring variables to use
  const {
    id,
    title,
    description,
    starttime,
    endtime,
    speaker,
    owner,
    location,
    url,
  } = eventData.node;

  // handle functions
  const _handleCardClick = () => {
    // set local state to control description visibility
    setDescriptionVisible(prev => !prev);
  };

  return (
    // <StyledListItem
    // onClick={this._handleCardClick}
    // color={DataColor.getCatColor(this.props.ev.category)}
    // cursorPointer={this.props.ev.description && !this.state.descriptionVisible}
    // >
    <StyledListItem
      color={getRandomColorFromText(owner)}
      cursorPointer={description}
      onClick={_handleCardClick}
    >
      <StyledContentWrapper>
        <TimeBox
          eventId={id}
          starttime={starttime}
          endtime={endtime}
        />
        <ContentBox
          // show by default
          title={title}
          location={location}
          owner={owner}
          url={url}
          description={description}
          isDescriptionExpanded={descriptionVisible}
        />
      </StyledContentWrapper>
      {
        descriptionVisible && description
          ? (
            <DescriptionBox
              // when expanded
              description={description}
              speaker={speaker}
            />
          )
          : null
      }
    </StyledListItem>
  );
};

EventItem.propTypes = {
  eventData: PropTypes.shape({
    node: PropTypes.shape({
      id: PropTypes.string,
      date_dt: PropTypes.string,
      title: PropTypes.string,
      description: PropTypes.string,
      starttime: PropTypes.string,
      endtime: PropTypes.string,
      speaker: PropTypes.string,
      owner: PropTypes.string,
      location: PropTypes.string,
      url: PropTypes.string,
    }),
  }).isRequired,
};

export default EventItem;
