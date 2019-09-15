import React from 'react';
import { css } from 'styled-components';
import { Link } from 'gatsby';
import PropTypes from 'prop-types';

// import { rhythm } from '../utils/typography';
import { Container } from './BaseComponents/container';
import NavBar from './Navbar';

const Layout = ({ children }) => (
  <React.Fragment>
    <NavBar>
      <Link to="/">
        Home
      </Link>
      <Link
        to="/about/"
        css={css`
          float: right;
        `}
      >
        About
      </Link>
    </NavBar>
    <Container>
      {children}
    </Container>
  </React.Fragment>
);

Layout.propTypes = {
  children: PropTypes.node,
};

Layout.defaultProps = {
  children: null,
};

export default Layout;
