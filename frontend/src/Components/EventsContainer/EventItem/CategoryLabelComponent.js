import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Category } from '../../../Data';

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

const CategoryLabel = ({ eventCategory, eventDescription }) => (
  <CatContainer>
    <StyledCat color={Category.getColor(eventCategory)}>
      {eventCategory}
    </StyledCat>
    {
      eventDescription ?
        <span>See Details <Fa icon="chevron-circle-down" /></span> :
        null
    }
  </CatContainer>
);

CategoryLabel.propTypes = {
  eventCategory: PropTypes.string.isRequired,
};

export default CategoryLabel;
