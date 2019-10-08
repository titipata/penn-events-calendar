import styled from 'styled-components';
import { media } from '../../utils/ui';
import { rhythm } from '../../utils/typography';

const bsContainerWidth = {
  extraSmall: null,
  small: '540px',
  medium: '720px',
  large: '960px',
  // extraLarge: '960px',
  extraLarge: '1140px',
};

const Container = styled.div`
  /* this is for footer to sticky at bottom */
  flex: 1;
  margin: 0 auto;
  padding: ${rhythm(1)};
  padding-top: ${rhythm(1.5)};

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
    padding: ${rhythm(1)} ${rhythm(0.25)};
  `}

  ${media.extraSmall`
    width: 100%;
  `}
`;

const NavContainer = styled(Container)`
  flex: 1;
  display: flex;
  flex-wrap: wrap;
  flex-direction: row;
  justify-content: space-between;
  align-items: center;
  padding: 0 ${rhythm(2)};

  ${media.small`
    width: ${bsContainerWidth.small};
    padding: 0 ${rhythm(0.25)};
  `}

  ${media.extraSmall`
    width: 100%;
  `}
`;

export { Container, NavContainer };
