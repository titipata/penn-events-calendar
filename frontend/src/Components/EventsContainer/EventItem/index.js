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
  cursor: ${props => (props.cursorPointer ? 'pointer' : 'default')};
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

    this._handleCardClick = this._handleCardClick.bind(this);
    this._handleCollapseClick = this._handleCollapseClick.bind(this);
  }

  _handleCardClick() {
    if (!this.state.descriptionVisible) {
      this.setState({
        descriptionVisible: true,
      });
    }
  }

  _handleCollapseClick() {
    this.setState({
      descriptionVisible: false,
    });
  }

  render() {
    return (
      <StyledListItem
        onClick={this._handleCardClick}
        color={Category.getColor(this.props.ev.category)}
        cursorPointer={this.props.ev.description && !this.state.descriptionVisible}
      >
        <StyledContentWrapper>
          <TimeBox
            eventDate={this.props.ev.date}
            eventStartTime={this.props.ev.starttime}
            eventEndTime={this.props.ev.endtime}
          />
          <DetailBox
            eventCategory={this.props.ev.category}
            eventDescription={this.props.ev.description}
            eventLocation={this.props.ev.location}
            eventTitle={this.props.ev.title}
            isDescriptionExpanded={this.state.descriptionVisible}
            onCollapseClick={this._handleCollapseClick}
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
