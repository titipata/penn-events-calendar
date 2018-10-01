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
  padding-right: 20px;
  word-break: break-all;
`;

const StyledLocation = styled.div`
  font-size: 0.9rem;
  padding-top: 5px;
`;

const StyledLinkIcon = styled.a.attrs({
  target: '_blank',
  rel: 'noopener noreferrer',
})`
  display: ${props => (props.href ? 'inline-flex' : 'none')};
  font-weight: lighter;
  font-size: 1rem;
  padding-right: 8px;
  color: #555;
  cursor: pointer;
`;

// https://stackoverflow.com/a/39333479/4010864
// pick only keys that are used in category
const getEventCategoryData = ({
  category, description, school,
}) => ({
  category, description, school,
});

const DetailBox = ({ eventDetail }) => (
  <DetailWrapper>
    <StyledTitle>
      <StyledLinkIcon
        href={eventDetail.url}
        // do not pass click to children underneath, only open a link
        onClick={e => e.stopPropagation()}
      >
        <Fa icon="external-link-alt" />
      </StyledLinkIcon>
      {renderHTML(eventDetail.title)}
    </StyledTitle>
    <StyledLocation>
      <Fa icon="map-marker-alt" /> {renderHTML(eventDetail.location)}
    </StyledLocation>
    <CategoryLabel
      eventCategoryData={getEventCategoryData(eventDetail)}
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
    url: PropTypes.string.isRequired,
  }).isRequired,
};

export default DetailBox;
