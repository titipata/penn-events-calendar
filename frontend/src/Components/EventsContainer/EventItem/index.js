import PropTypes from 'prop-types';
import React, { Component } from 'react';
import styled from 'styled-components';
import { DataColor } from '../../../Data';
import DetailBox from './DetailBoxComponent';
import TimeBox from './TimeBoxComponent';
import DescriptionBox from './DescriptionBoxComponent';
import SimilarEventsBox from './SimilarEventsBoxContainer';

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
    // https://stackoverflow.com/a/39333479/4010864
    const getEventTime = ({ starttime, endtime }) => ({ starttime, endtime });
    const getEventDetail = ({
      category, description, location, title, school, url,
    }) => ({
      category, description, location, title, school, url,
    });

    return (
      <StyledListItem
        onClick={this._handleCardClick}
        color={DataColor.getCatColor(this.props.ev.category)}
        cursorPointer={this.props.ev.description && !this.state.descriptionVisible}
      >
        <StyledContentWrapper>
          <TimeBox
            eventTime={getEventTime(this.props.ev)}
          />
          <DetailBox
            eventDetail={getEventDetail(this.props.ev)}
            isDescriptionExpanded={this.state.descriptionVisible}
            onCollapseClick={this._handleCollapseClick}
          />
        </StyledContentWrapper>
        {
          this.state.descriptionVisible && this.props.ev.description ?
            <DescriptionBox eventDescription={this.props.ev.description} /> :
            null
        }
        {
          this.state.descriptionVisible ?
            <SimilarEventsBox id={this.props.ev.event_id} /> :
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
    event_id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]),
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
