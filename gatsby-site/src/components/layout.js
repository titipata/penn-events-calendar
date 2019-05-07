import React from 'react';
import { css } from 'styled-components';
import { Link } from 'gatsby';
import PropTypes from 'prop-types';

import { rhythm } from '../utils/typography';

const Layout = ({ children }) => (
  <div
    css={css`
      margin: 0 auto;
      max-width: 700px;
      padding: ${rhythm(2)};
      padding-top: ${rhythm(1.5)};
    `}
  >
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
  </div>
);

Layout.propTypes = {
  children: PropTypes.node,
};

Layout.defaultProps = {
  children: null,
};

export default Layout;
