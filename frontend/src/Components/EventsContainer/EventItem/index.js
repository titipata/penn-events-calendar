import PropTypes from 'prop-types';
import React, { Component } from 'react';
import { connect } from 'react-redux';
import styled from 'styled-components';
import { getEventDetails, fetchSimilarEvents, toggleEventDetail } from '../../../Actions';
import { DataColor } from '../../../Data';
import DescriptionBox from './DescriptionBoxComponent';
import DetailBox from './DetailBoxComponent';
import SimilarEventsBox from './SimilarEventsBoxContainer';
import TimeBox from './TimeBoxComponent';

const StyledListItem = styled.li`
  margin-bottom: 5px;
  padding: 10px 0;
  border: 1px solid #eee;
  border-left: 5px solid ${props => props.color};
  border-radius: 5px;
  /* cursor: ${props => (props.cursorPointer ? 'pointer' : 'default')}; */
  cursor: pointer;
`;

const StyledContentWrapper = styled.div`
  display: flex;
  flex-direction: row;
`;

class EventItem extends Component {
  componentDidMount() {
    console.log('yay');
  }

  render() {
    const eventId = this.props.ev.event_id;
    // https://stackoverflow.com/a/39333479/4010864
    const getEventTime = ({ starttime, endtime }) => ({ starttime, endtime });
    const getEventDetail = ({
      category, description, location, title, school, url,
    }) => ({
      category, description, location, title, school, url,
    });

    return (
      <StyledListItem
        onClick={() => {
          this.props.toggleVisibility(eventId);
          this.props.getSimilarEvents(eventId);
        }}
        color={DataColor.getCatColor(this.props.ev.category)}
        // cursorPointer={!this.state.descriptionVisible}
      >
        <StyledContentWrapper>
          <TimeBox
            eventTime={getEventTime(this.props.ev)}
          />
          <DetailBox
            eventDetail={getEventDetail(this.props.ev)}
          />
        </StyledContentWrapper>
        {
          this.props.ev.detailVisible ?
            <React.Fragment>
              <DescriptionBox description={this.props.ev.description} />
              <SimilarEventsBox similarEvents={null} />
            </React.Fragment> :
            null
        }
      </StyledListItem>
    );
  }
}

EventItem.propTypes = {
  getSimilarEvents: PropTypes.func.isRequired,
  toggleVisibility: PropTypes.func.isRequired,
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
    visible: PropTypes.bool,
  }).isRequired,
};

const mapDispatchToProps = dispatch => ({
  getSimilarEvents: eventId => dispatch(fetchSimilarEvents(eventId)),
  toggleVisibility: eventId => dispatch(toggleEventDetail(eventId)),
});

export default connect(
  null,
  mapDispatchToProps,
)(EventItem);
