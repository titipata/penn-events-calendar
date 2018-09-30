import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { DataColor } from '../../../../Data';

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

const StyledGroup = styled.div`
  display: inline-flex;
  align-items: center;
  padding-right: 10px;
`;

const CategoryLabel = ({ eventCategoryData }) => (
  <CatContainer>
    <StyledGroup>
      <StyledCat color={DataColor.getSchoolColor(eventCategoryData.school)}>
        {eventCategoryData.school}
      </StyledCat>
      {
        !eventCategoryData.school.includes(eventCategoryData.category.split(/ |,\\\//)[0]) ?
        (
          <StyledCat color={DataColor.getCatColor(eventCategoryData.category)}>
            {eventCategoryData.category}
          </StyledCat>
        ) :
        null
      }
    </StyledGroup>
  </CatContainer>
);

CategoryLabel.propTypes = {
  eventCategoryData: PropTypes.shape({
    category: PropTypes.string.isRequired,
    description: PropTypes.string.isRequired,
    school: PropTypes.string.isRequired,
  }).isRequired,
};

export default CategoryLabel;
