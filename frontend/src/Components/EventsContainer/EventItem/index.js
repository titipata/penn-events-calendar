import PropTypes from 'prop-types';
import React, { Component } from 'react';
import styled from 'styled-components';
import { Category } from '../../../Data';
import DetailBox from './DetailBoxComponent';
import TimeBox from './TimeBoxComponent';
import DescriptionBox from './DescriptionBoxComponent';

const StyledListItem = styled.li`
  margin-bottom: 5px;
  padding: 10px 0;
  border: 1px solid #eee;
  border-left: 5px solid ${props => props.color};
  border-radius: 5px;
`;

const StyledContentWrapper = styled.div`
  display: flex;
  flex-direction: row;
`;

class EventItem extends Component {
  constructor(props) {
    super(props);
    this.state = {
      descriptionVisible: false,
    };

    this._handleClick = this._handleClick.bind(this);
  }

  _handleClick() {
    this.setState({
      descriptionVisible: !this.state.descriptionVisible,
    });
  }

  render() {
    return (
      <StyledListItem onClick={this._handleClick} color={Category.getColor(this.props.ev.category)}>
        <StyledContentWrapper>
          <TimeBox
            eventDate={this.props.ev.date}
            eventStartTime={this.props.ev.starttime}
            eventEndTime={this.props.ev.endtime}
          />
          <DetailBox
            eventTitle={this.props.ev.title}
            eventLocation={this.props.ev.location}
            eventCategory={this.props.ev.category}
            eventDescription={this.props.ev.description}
          />
        </StyledContentWrapper>
        {
          this.state.descriptionVisible && this.props.ev.description ?
            <DescriptionBox eventDescription={this.props.ev.description} /> :
            null
        }
      </StyledListItem>
    );
  }
}

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
