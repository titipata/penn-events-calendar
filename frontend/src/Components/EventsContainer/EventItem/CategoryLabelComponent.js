import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Category } from '../../../Data';

const StyledCat = styled.div`
  font-size: 0.9rem;
  margin-top: 10px;
  padding: 5px;
  border: 1px solid ${props => props.color};
  background-color: ${props => `${props.color}1A`};
  border-radius: 5px;
  width: auto;
`;

const CategoryLabel = ({ eventCategory }) => (
  <StyledCat color={Category.getColor(eventCategory)}>
    {eventCategory}
  </StyledCat>
);

CategoryLabel.propTypes = {
  eventCategory: PropTypes.string.isRequired,
};

export default CategoryLabel;
