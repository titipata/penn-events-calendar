import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Category } from '../../../../Data';

const CatContainer = styled.div`
  display: flex;
  align-items: center;
  margin-top: 10px;
  justify-content: space-between;
`;

const StyledCat = styled.div`
  font-size: 0.9rem;
  /* margin-top: 10px; */
  padding: 5px;
  border: 1px solid ${props => props.color};
  background-color: ${props => `${props.color}1A`};
  border-radius: 5px;
  width: fit-content;
  margin-right: 5px;
`;

const StyledSpan = styled.span`
  cursor: pointer;
  color: ${props => `${props.color}A6`};
`;

const StyledGroup = styled.div`
  display: inline-flex;
  align-items: center;
  padding-right: 10px;
`;

const CategoryLabel = ({
  eventCategoryData,
  isDescriptionExpanded,
  onCollapseClick,
}) => (
  <CatContainer>
    <StyledGroup>
      <StyledCat color="#ddd">
        {eventCategoryData.school}
      </StyledCat>
      <StyledCat color={Category.getColor(eventCategoryData.category)}>
        {eventCategoryData.category}
      </StyledCat>
    </StyledGroup>
    {
      eventCategoryData.description && !isDescriptionExpanded ?
        <StyledSpan
          color={Category.getColor(eventCategoryData.category)}
        >
          See Details <Fa icon="chevron-circle-down" />
        </StyledSpan> :
        null
    }
    {
      eventCategoryData.description && isDescriptionExpanded ?
        <StyledSpan
          color={Category.getColor(eventCategoryData.category)}
          onClick={onCollapseClick}
        >
          Collapse <Fa icon="chevron-circle-up" />
        </StyledSpan> :
        null
    }
  </CatContainer>
);

CategoryLabel.propTypes = {
  eventCategoryData: PropTypes.shape({
    category: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    school: PropTypes.string.isRequired,
  }).isRequired,
  isDescriptionExpanded: PropTypes.bool.isRequired,
  onCollapseClick: PropTypes.func.isRequired,
};

export default CategoryLabel;
