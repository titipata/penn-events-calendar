import React from 'react';
import { Link } from 'gatsby';
import PropTypes from 'prop-types';
import styled from 'styled-components';

import { Container } from './BaseComponents/container';
import NavBar from './Navbar';
import Footer from './Footer';

const StickyFooterWrapper = styled.div`
  /* sticky footer */
  display: flex;
  height: 100%;
  min-height: 100vh;
  flex-direction: column;
`;

const Layout = ({ children }) => (
  <StickyFooterWrapper>
    <NavBar>
      <Link to="/">
        Home
      </Link>
      <Link to="/selected-events">
        Selected Events
      </Link>
      <Link to="/">
        Recommendations
      </Link>
    </NavBar>

    <Container>
      {children}
    </Container>

    <Footer />
  </StickyFooterWrapper>
);

Layout.propTypes = {
  children: PropTypes.node,
};

Layout.defaultProps = {
  children: null,
};

export default Layout;
