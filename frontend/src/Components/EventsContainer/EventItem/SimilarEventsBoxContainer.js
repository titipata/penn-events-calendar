import PropTypes from 'prop-types';
import React, { Component } from 'react';
import styled from 'styled-components';
import { Key } from '../../../Utils';

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

const StyledUl = styled.ul`
  padding: 0;
`;

class SimilarEventsBox extends Component {
  componentDidMount() {
    // get similar events of this
    // this.props.getSimilarEvents(this.props.id);
  }

  render() {
    const { similarEvents } = this.props;

    // check first if the returned event is array and is not empty
    return (
      <StyledBox>
        <StyledHeader>
          Similar Events:
        </StyledHeader>
        <StyledContent>
          {/* {console.log('HERE is similar events:', similarEvents)} */}
          {/* {console.log('HERE is filters events:', similarEvents.find(x => x.id === id))} */}
          {
            similarEvents ?
            (
              <StyledUl>
                {
                  similarEvents.data.length !== 0 ?
                    similarEvents.data.map(simevs =>
                    (
                      <li key={Key.getShortKey()}>{simevs.title}</li>
                    )) :
                    'No similar events for this event.'
                }
              </StyledUl>
            ) : 'No similar events for this event id.'
          }
        </StyledContent>
      </StyledBox>
    );
  }
}

SimilarEventsBox.propTypes = {
  similarEvents: PropTypes.shape({
    id: PropTypes.string,
    data: PropTypes.arrayOf(Object),
  }),
};

SimilarEventsBox.defaultProps = {
  similarEvents: null,
};

export default SimilarEventsBox;
