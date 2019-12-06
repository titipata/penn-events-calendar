import { FontAwesomeIcon as Fa } from '@fortawesome/react-fontawesome';
import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { getRandomColorFromText } from '../../../../utils';

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
  border: 1px solid ${(props) => props.color};
  background-color: ${(props) => `${props.color}1A`};
  border-radius: 5px;
  width: fit-content;
  margin-right: 5px;
`;

const StyledSpan = styled.span`
  cursor: pointer;
  color: ${(props) => `${props.color}A6`};
`;

const StyledGroup = styled.div`
  display: inline-flex;
  align-items: center;
  padding-right: 10px;
`;

const CategoryLabel = ({
  owner,
  description,
  isDescriptionExpanded,
  // onCollapseClick,
}) => (
  <CatContainer>
    <StyledGroup>
      <StyledCat color={getRandomColorFromText(owner)}>
        {owner}
      </StyledCat>
    </StyledGroup>
    {
      description
        ? (
          <StyledSpan
            color={getRandomColorFromText(owner)}
          >
            <Fa icon={`chevron-circle-${isDescriptionExpanded ? 'up' : 'down'}`} />
          </StyledSpan>
        )
        : null
    }
  </CatContainer>
);

CategoryLabel.propTypes = {
  owner: PropTypes.string,
  description: PropTypes.string,
  // eventCategoryData: PropTypes.shape({
  //   category: PropTypes.string.isRequired,
  //   description: PropTypes.string.isRequired,
  //   school: PropTypes.string.isRequired,
  // }).isRequired,
  isDescriptionExpanded: PropTypes.bool.isRequired,
  // onCollapseClick: PropTypes.func.isRequired,
};

CategoryLabel.defaultProps = {
  owner: null,
  description: null,
};

export default CategoryLabel;
