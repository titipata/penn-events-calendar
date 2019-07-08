import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';

const StyledDescriptionBox = styled.div`
  flex: 1;
  margin: 15px;
  margin-bottom: 5px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 5px;
`;

const StyledHeader = styled.div`
  font-size: 1.15rem;
  font-weight: bold;
`;

const StyledContent = styled.div`
  color: #222;
  text-indent: 1.15rem;
  padding: 0 1.15rem;
  padding-top: 0.75rem;
  line-height: 1.3rem;
`;

const DescriptionBox = ({ description, speaker }) => (
  <StyledDescriptionBox>
    <StyledHeader>
      Speaker:
    </StyledHeader>
    <StyledContent>
      {speaker}
    </StyledContent>
    <StyledHeader>
      Description:
    </StyledHeader>
    <StyledContent>
      {description}
    </StyledContent>
  </StyledDescriptionBox>
);

DescriptionBox.propTypes = {
  description: PropTypes.string,
  speaker: PropTypes.string,
};

DescriptionBox.defaultProps = {
  description: null,
  speaker: null,
};

export default DescriptionBox;
