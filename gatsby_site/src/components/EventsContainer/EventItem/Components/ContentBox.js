import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
// import renderHTML from 'react-render-html';
import styled from 'styled-components';
import CategoryLabel from './CategoryLabel';

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

const StyledLinkIcon = styled.a.attrs({
  target: '_blank',
  rel: 'noopener noreferrer',
})`
  font-weight: lighter;
  font-size: 1rem;
  margin-left: 8px;
  color: #555;
  cursor: pointer;
`;

const StyledMarkerIcon = styled(Fa).attrs({
  icon: 'map-marker-alt',
})`
  margin-right: 8px;
`;

const DetailBox = ({
  title,
  location,
  owner,
  url,
  description,
  isDescriptionExpanded,
  saveToCalendarUrl,
}) => (
  <DetailWrapper>
    <StyledTitle>
      {/* {renderHTML(eventDetail.title)} */}
      {title}
      {
        url
          ? (
            <StyledLinkIcon href={url}>
              <Fa icon="external-link-alt" />
            </StyledLinkIcon>
          )
          : null
      }
      {
        saveToCalendarUrl
          ? (
            <StyledLinkIcon href={saveToCalendarUrl}>
              <Fa icon={['far', 'calendar-plus']} />
            </StyledLinkIcon>
          )
          : null
      }
    </StyledTitle>
    <StyledLocation>
      <StyledMarkerIcon />
      {/* {renderHTML(eventDetail.location)} */}
      {location || 'unknown'}
    </StyledLocation>
    <CategoryLabel
      owner={owner}
      description={description}
      isDescriptionExpanded={isDescriptionExpanded}
      // onCollapseClick={onCollapseClick}
    />
  </DetailWrapper>
);

DetailBox.propTypes = {
  title: PropTypes.string,
  location: PropTypes.string,
  owner: PropTypes.string,
  url: PropTypes.string,
  description: PropTypes.string,
  isDescriptionExpanded: PropTypes.bool.isRequired,
  saveToCalendarUrl: PropTypes.string.isRequired,
};

DetailBox.defaultProps = {
  title: null,
  location: null,
  owner: null,
  url: null,
  description: null,
};

export default DetailBox;
