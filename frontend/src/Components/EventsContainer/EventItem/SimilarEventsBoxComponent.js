import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { connect } from 'react-redux';
import { Key } from '../../../Utils';
import { xml2js } from '../../../../node_modules/xml-js';

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

const SimilarEventsBox = ({ similarEvents, id }) => (
  <StyledBox>
    <StyledHeader>
      Similar Events:
    </StyledHeader>
    <StyledContent>
      {/* {console.log('HERE is similar events:', similarEvents)} */}
      {console.log('HERE is filters events:', similarEvents.find(x => x.id === id))}
      <ul>
        {similarEvents.map(event => <li key={Key.getShortKey()}>{event.title}</li>)}
      </ul>
    </StyledContent>
  </StyledBox>
);

SimilarEventsBox.propTypes = {
  similarEvents: PropTypes.arrayOf(Object).isRequired,
  id: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
};

const mapStateToProps = state => ({
  similarEvents: state.events.similarEvents,
});

export default connect(
  mapStateToProps,
  null,
)(SimilarEventsBox);
