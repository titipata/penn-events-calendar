import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Category } from '../../../Data';
import DetailBox from './DetailBoxComponent';
import TimeBox from './TimeBoxComponent';

const StyledListItem = styled.li`
  margin-bottom: 5px;
  padding: 10px 0;
  border: 1px solid #eee;
  border-left: 5px solid ${props => props.color};
  border-radius: 5px;
`;

const StyledContentWrapper = styled.div`
  display: inline-flex;
  flex-direction: row;
`;

const EventItem = ({ ev }) => (
  <StyledListItem onClick={()=>console.log(ev.event_id, ': is clicked!')} color={Category.getColor(ev.category)}>
    <StyledContentWrapper>
      <TimeBox
        eventDate={ev.date}
        eventStartTime={ev.starttime}
        eventEndTime={ev.endtime}
      />
      <DetailBox
        eventTitle={ev.title}
        eventLocation={ev.location}
        eventCategory={ev.category}
      />
    </StyledContentWrapper>
  </StyledListItem>
);

EventItem.propTypes = {
  ev: PropTypes.shape({
    date: PropTypes.string,
    day_of_week: PropTypes.string,
    starttime: PropTypes.string,
    endtime: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
    location: PropTypes.string,
    room: PropTypes.string,
    event_id: PropTypes.number,
    url: PropTypes.string,
    student: PropTypes.string,
    privacy: PropTypes.string,
    category: PropTypes.string,
    school: PropTypes.string,
    owner: PropTypes.string,
    link: PropTypes.string,
  }).isRequired,
};

export default EventItem;
