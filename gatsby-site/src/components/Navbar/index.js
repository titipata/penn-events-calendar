import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { NavContainer } from '../BaseComponents/container';

// get logo image using require
const pennLogoURI = require('../../images/penn-logo.png');

// variables
const navHeight = 60;

// navbar component
const Navbar = styled.nav`
  background-color: #fff;
  height: ${navHeight}px;
  justify-content: center;
  position: fixed;
  top: 0;
  width: 100%;
  box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.19);
`;

// nav is fixed, so it needs padder underneath
const NavPadder = styled.div`
  height: ${navHeight}px;
`;

const StyledImg = styled.img`
  margin: 0;
  height: ${navHeight}px;
  width: auto;
  justify-self: flex-start;
  mix-blend-mode: multiply;
  padding: 6px 0;
`;

const NavbarComponent = ({ children }) => (
  <React.Fragment>
    <Navbar>
      <NavContainer>
        <StyledImg src={pennLogoURI} alt="Penn Logo" />
        { children }
      </NavContainer>
    </Navbar>
    <NavPadder />
  </React.Fragment>
);

NavbarComponent.propTypes = {
  children: PropTypes.node,
};

NavbarComponent.defaultProps = {
  children: null,
};

export default NavbarComponent;
