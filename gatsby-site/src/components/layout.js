import React from 'react';
import { Link } from 'gatsby';
import PropTypes from 'prop-types';

import { Container } from './BaseComponents/container';
import NavBar from './Navbar';

const Layout = ({ children }) => (
  <React.Fragment>
    <NavBar>
      <Link to="/">
        Home
      </Link>
      <Link to="/">
        Selected Events
      </Link>
      <Link
        to="/about/"
      >
        Recommendations
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
