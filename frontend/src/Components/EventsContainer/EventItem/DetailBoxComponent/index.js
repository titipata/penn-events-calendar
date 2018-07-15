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

const StyledLinkIcon = styled.span`
  font-weight: lighter;
  font-size: 1rem;
  padding-left: 8px;
  color: #555;
`;

// https://stackoverflow.com/a/39333479/4010864
// pick only keys that are used in category
const getEventCategoryData = ({
  category, description, school,
}) => ({
  category, description, school,
});

const DetailBox = ({
  eventDetail,
  isDescriptionExpanded,
  onCollapseClick,
}) => (
  <DetailWrapper>
    <StyledTitle>
      {renderHTML(eventDetail.title)}
      <StyledLinkIcon>
        <Fa icon="external-link-alt" />
      </StyledLinkIcon>
    </StyledTitle>
    <StyledLocation>
      <Fa icon="map-marker-alt" /> {eventDetail.location}
    </StyledLocation>
    <CategoryLabel
      eventCategoryData={getEventCategoryData(eventDetail)}
      isDescriptionExpanded={isDescriptionExpanded}
      onCollapseClick={onCollapseClick}
    />
  </DetailWrapper>
);

DetailBox.propTypes = {
  eventDetail: PropTypes.shape({
    category: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    location: PropTypes.string.isRequired,
    title: PropTypes.string.isRequired,
    school: PropTypes.string.isRequired,
  }).isRequired,
  isDescriptionExpanded: PropTypes.bool.isRequired,
  onCollapseClick: PropTypes.func.isRequired,
};

export default DetailBox;
