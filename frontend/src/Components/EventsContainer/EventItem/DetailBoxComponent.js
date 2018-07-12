import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import renderHTML from 'react-render-html';
import styled from 'styled-components';
import CategoryLabel from './CategoryLabelComponent';

const DetailWrapper = styled.div`
  padding: 0 15px;
  flex: 1;
`;

const StyledTitle = styled.div`
  font-size: 1.3rem;
  font-weight: 600;
`;

const StyledLocation = styled.div`
  font-size: 0.9rem;
  padding-top: 5px;
`;

const DetailBox = ({ eventTitle, eventLocation, eventCategory, eventDescription, isDescriptionExpanded, onCollapseClick }) => (
  <DetailWrapper>
    <StyledTitle>
      {renderHTML(eventTitle)}
    </StyledTitle>
    <StyledLocation>
      <Fa icon="map-marker-alt" /> {eventLocation}
    </StyledLocation>
    <CategoryLabel
      eventCategory={eventCategory}
      eventDescription={eventDescription}
      isDescriptionExpanded={isDescriptionExpanded}
      onCollapseClick={onCollapseClick}
    />
  </DetailWrapper>
);

DetailBox.propTypes = {
  eventTitle: PropTypes.string.isRequired,
  eventLocation: PropTypes.string.isRequired,
  eventCategory: PropTypes.string.isRequired,
};

export default DetailBox;
