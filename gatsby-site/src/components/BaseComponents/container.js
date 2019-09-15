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
  flex: 1;
  margin: 0 auto;
  justify-content: center;
  padding: ${rhythm(2)};
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
    padding: ${rhythm(0.25)};
  `}

  ${media.extraSmall`
    width: 100%;
    padding: ${rhythm(0.25)};
  `}
`;

const NavContainer = styled(Container)`
  padding: 0 ${rhythm(2)};
`;

export { Container, NavContainer };
