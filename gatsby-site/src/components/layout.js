import React from 'react';
import { css } from 'styled-components';
import { Link } from 'gatsby';
import PropTypes from 'prop-types';

import { rhythm } from '../utils/typography';
import Container from './BaseComponents/container';

const Layout = ({ children }) => (
  <Container>
    <Link to="/">
      <h3
        css={css`
          margin-bottom: ${rhythm(2)};
          display: inline-block;
          font-style: normal;
        `}
      >
        Pandas Eating Lots
      </h3>
    </Link>
    <Link
      to="/about/"
      css={css`
        float: right;
      `}
    >
      About
    </Link>
    {children}
  </Container>
);

Layout.propTypes = {
  children: PropTypes.node,
};

Layout.defaultProps = {
  children: null,
};

export default Layout;
