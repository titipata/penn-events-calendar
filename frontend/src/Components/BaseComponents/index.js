import styled, { css } from 'styled-components';
import LoadingScreen from './LoadingScreenComponent';

const mediaSizes = {
  extraSmall: 576,
  small: 768,
  medium: 992,
  large: 1200,
  extraLarge: 1200,
};

const bsContainerWidth = {
  extraSmall: null,
  small: '540px',
  medium: '720px',
  large: '960px',
  extraLarge: '960px',
  // extraLarge: '1140px',
};

// https://www.styled-components.com/docs/advanced#media-templates
// Iterate through the sizes and create a media template
const media = Object.keys(mediaSizes).reduce((acc, label) => {
  if (label === 'extraLarge') {
    acc[label] = (...args) => css`
      @media (min-width: ${mediaSizes[label] / 16}em) {
        ${css(...args)}
      }
    `;
  } else {
    acc[label] = (...args) => css`
      @media (max-width: ${mediaSizes[label] / 16}em) {
        ${css(...args)}
      }
    `;
  }

  return acc;
}, {});

const Container = styled.div`
  flex: 1;
  margin: 0 auto;
  justify-content: center;

  ${media.extraLarge`
    width: ${bsContainerWidth.extraLarge};
  `}

  ${media.large`
    width: ${bsContainerWidth.large};
  `}

  ${media.medium`
    width: ${bsContainerWidth.medium};
  `}

  ${media.small`
    width: ${bsContainerWidth.small};
  `}

  ${media.extraSmall`
    width: 100%;
  `}
`;

export { media, Container, LoadingScreen };
