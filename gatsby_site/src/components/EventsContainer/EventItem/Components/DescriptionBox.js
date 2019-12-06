import PropTypes from 'prop-types';
import React from 'react';
import styled, { css, keyframes } from 'styled-components';

const animateCss = {
  visible: css`
    height: 100%;
    padding: 15px;
    margin: 15px;
    opacity: 1;
    visibility: visible;
  `,
  invisible: css`
    height: 0;
    padding: 0 15px;
    margin: 0 15px;
    opacity: 0;
    visibility: hidden;
  `,
};

const showAnimation = keyframes`
  0% {
    ${animateCss.invisible}
  }
  100% {
    ${animateCss.visible}
  }
`;

const hideAnimation = keyframes`
  0% {
    ${animateCss.visible}
  }
  100% {
    ${animateCss.invisible}
  }
`;

const StyledDescriptionBox = styled.div`
  flex: 1;
  margin-bottom: 5px;
  border: 1px solid #eee;
  border-radius: 5px;

  ${(props) => (props.visible === null
    ? animateCss.invisible
    : props.visible
      ? css`
        animation: 0.45s ${showAnimation} forwards;
      `
      : css`
        animation: 0.22s ${hideAnimation} forwards;
      `)}
`;

const StyledHeader = styled.div`
  font-size: 1.15rem;
  font-weight: bold;
`;

const StyledContent = styled.div`
  color: #222;
  text-indent: 1.15rem;
  padding: 0.5rem 1.15rem;
  /* padding-top: 0.75rem; */
  line-height: 1.3rem;
  margin-bottom: 5px;
`;

const DescriptionBox = ({ description, speaker, shouldVisible }) => (
  <StyledDescriptionBox
    visible={shouldVisible}
  >
    {
      speaker
        ? (
          <>
            <StyledHeader>
              Speaker:
            </StyledHeader>
            <StyledContent>
              {speaker}
            </StyledContent>
          </>
        )
        : null
    }
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
  shouldVisible: PropTypes.bool,
};

DescriptionBox.defaultProps = {
  description: null,
  speaker: null,
  shouldVisible: null,
};

export default DescriptionBox;
