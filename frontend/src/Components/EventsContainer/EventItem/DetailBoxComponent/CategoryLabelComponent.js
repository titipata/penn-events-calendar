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
`;

const StyledSpan = styled.span`
  cursor: pointer;
  color: ${props => `${props.color}A6`};
`;

const CategoryLabel = ({
  eventCategory,
  eventDescription,
  isDescriptionExpanded,
  onCollapseClick,
}) => (
  <CatContainer>
    <StyledCat color={Category.getColor(eventCategory)}>
      {eventCategory}
    </StyledCat>
    {
      eventDescription && !isDescriptionExpanded ?
        <StyledSpan
          color={Category.getColor(eventCategory)}
        >
          See Details <Fa icon="chevron-circle-down" />
        </StyledSpan> :
        null
    }
    {
      eventDescription && isDescriptionExpanded ?
        <StyledSpan
          color={Category.getColor(eventCategory)}
          onClick={onCollapseClick}
        >
          Collapse <Fa icon="chevron-circle-up" />
        </StyledSpan> :
        null
    }
  </CatContainer>
);

CategoryLabel.propTypes = {
  eventCategory: PropTypes.string.isRequired,
  eventDescription: PropTypes.string.isRequired,
  isDescriptionExpanded: PropTypes.bool.isRequired,
  onCollapseClick: PropTypes.func.isRequired,
};

export default CategoryLabel;
