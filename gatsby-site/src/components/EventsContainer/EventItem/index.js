import PropTypes from 'prop-types';
import React, { Component } from 'react';
import styled from 'styled-components';
// import { DataColor } from '../../../Data';
import ContentBox from './Components/ContentBox';
import TimeBox from './Components/TimeBox';
import DescriptionBox from './Components/DescriptionBox';

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

    // this._handleCardClick = this._handleCardClick.bind(this);
    // this._handleCollapseClick = this._handleCollapseClick.bind(this);
  }

  // _handleCardClick() {
  //   // dispatch event id to get similar events on click
  //   this.props.similarEvents(this.props.ev.event_id);

  //   if (!this.state.descriptionVisible) {
  //     this.setState({
  //       descriptionVisible: true,
  //     });
  //   }
  // }

  // _handleCollapseClick() {
  //   this.setState({
  //     descriptionVisible: false,
  //   });
  // }

  render() {
    // https://stackoverflow.com/a/39333479/4010864
    // const getEventTime = ({ starttime, endtime }) => ({ starttime, endtime });
    // const getEventDetail = ({
    //   category, description, location, title, school, url,
    // }) => ({
    //   category, description, location, title, school, url,
    // });
    const { descriptionVisible } = this.state;
    const { eventData } = this.props;
    const { node } = eventData;
    const {
      // id,
      // date_dt,
      title,
      description,
      // starttime_dt,
      // endtime_dt,
      speaker,
      owner,
      location,
      url,
    } = eventData.node;

    return (
      // <StyledListItem
      // onClick={this._handleCardClick}
      // color={DataColor.getCatColor(this.props.ev.category)}
      // cursorPointer={this.props.ev.description && !this.state.descriptionVisible}
      // >
      <StyledListItem>
        <StyledContentWrapper>
          <TimeBox
            starttime={node.starttime_dt}
            endtime={node.endtime_dt}
          />
          <ContentBox
            // show by default
            title={title}
            location={location}
            owner={owner}
            url={url}
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
  }
}

EventItem.propTypes = {
  eventData: PropTypes.shape({
    id: PropTypes.string,
    date_dt: PropTypes.string,
    title: PropTypes.string,
    description: PropTypes.string,
    starttime_dt: PropTypes.string,
    endtime_dt: PropTypes.string,
    speaker: PropTypes.string,
    owner: PropTypes.string,
    location: PropTypes.string,
    url: PropTypes.string,
  }).isRequired,
};

export default EventItem;
