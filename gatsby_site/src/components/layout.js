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

const StyledLink = styled(Link)`
  height: 100%;
  display: flex;
  flex: 1;
  align-items: center;
  justify-content: center;
`;

const Layout = ({ children }) => (
  <StickyFooterWrapper>
    <NavBar>
      <StyledLink to="/">
        Home
      </StyledLink>
      <StyledLink to="/selected-events">
        Selected Events
      </StyledLink>
      <StyledLink to="/recommendations">
        Recommendations
      </StyledLink>
      <StyledLink to="/how-it-works">
        Usage
      </StyledLink>
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
