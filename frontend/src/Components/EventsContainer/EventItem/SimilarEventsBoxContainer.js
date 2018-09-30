import PropTypes from 'prop-types';
import React, { Component } from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { Key } from '../../../Utils';
import { fetchSimilarEvents } from '../../../Actions';

const StyledBox = styled.div`
  flex: 1;
  margin: 15px;
  margin-bottom: 5px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 5px;
`;

const StyledHeader = styled.div`
  font-size: 1.15rem;
  font-weight: bold;
`;

const StyledContent = styled.div`
  color: #222;
  text-indent: 1.15rem;
  padding: 0 1.15rem;
  padding-top: 0.75rem;
  line-height: 1.3rem;
`;

class SimilarEventsBox extends Component {
  componentDidMount() {
    // get similar events of this
    // this.props.getSimilarEvents(this.props.id);
  }

  render() {
    const { similarEvents, id } = this.props;
    const matchId = similarEvents.find(x => x.id === id);
    const similarEvent = matchId ? matchId.data : null;

    // check first if the returned event is array and is not empty
    return Array.isArray(similarEvent) && similarEvent.length ? (
      <StyledBox>
        <StyledHeader>
          Similar Events:
        </StyledHeader>
        <StyledContent>
          {/* {console.log('HERE is similar events:', similarEvents)} */}
          {/* {console.log('HERE is filters events:', similarEvents.find(x => x.id === id))} */}
          <ul>
            {
              similarEvent.map(simevs => <li key={Key.getShortKey()}>{simevs.title}</li>)
            }
          </ul>
        </StyledContent>
      </StyledBox>
    ) : null;
  }
}

SimilarEventsBox.propTypes = {
  similarEvents: PropTypes.arrayOf(Object).isRequired,
  id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  getSimilarEvents: PropTypes.func.isRequired,
};

const mapStateToProps = state => ({
  similarEvents: state.events.similarEvents,
});

const mapDispatchToProps = dispatch => ({
  getSimilarEvents: eventId => dispatch(fetchSimilarEvents(eventId)),
});

export default connect(
  mapStateToProps,
  mapDispatchToProps,
)(SimilarEventsBox);
