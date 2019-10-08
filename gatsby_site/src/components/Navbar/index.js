import React, { useState } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { NavContainer } from '../BaseComponents/container';
import Burger from '../BaseComponents/BurgerMenu';
import Menus from './Menus';

// get logo image using require
const pennLogoURI = require('../../images/penn-logo.png');

// variables
const navHeight = 60;

// navbar component
const Navbar = styled.nav`
  background-color: #fefefe;
  min-height: ${navHeight}px;
  position: fixed;
  top: 0;
  width: 100%;
  box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.19);
  z-index: 999;
`;

// nav is fixed, so it needs padder underneath
const NavPadder = styled.div`
  height: ${navHeight}px;
`;

const LogoWrapper = styled.div`
  display: flex;
  /* determine image size here */
  height: ${navHeight}px;
  padding: 6px 0;
`;

const StyledImg = styled.img`
  margin: 0;
  /* this fix image color by multiplying color of image through bg */
  mix-blend-mode: multiply;
  /* grow to fit its wrapper */
  height: 100%;
`;

const NavbarComponent = ({ children }) => {
  const [hideMenu, setHideMenu] = useState(true);

  return (
    <>
      <Navbar>
        <NavContainer>
          <LogoWrapper>
            <StyledImg src={pennLogoURI} alt="Penn Logo" />
          </LogoWrapper>
          <Burger handlePress={() => setHideMenu(!hideMenu)} />
          <Menus
            hidden={hideMenu}
            items={children}
          />
        </NavContainer>
      </Navbar>
      <NavPadder />
    </>
  );
};

NavbarComponent.propTypes = {
  children: PropTypes.node,
};

NavbarComponent.defaultProps = {
  children: null,
};

export default NavbarComponent;
