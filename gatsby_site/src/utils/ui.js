import { css } from 'styled-components';

const mediaSizes = {
  extraSmall: 576,
  small: 768,
  medium: 992,
  large: 1200,
  extraLarge: 1200,
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

export {
  mediaSizes,
  media,
};
