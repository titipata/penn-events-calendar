import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import { NavContainer } from '../BaseComponents/container';

// TODO: responsive menu items => hamburger

// get logo image using require
const pennLogoURI = require('../../images/penn-logo.png');

// variables
const navHeight = 60;

// navbar component
const Navbar = styled.nav`
  background-color: #fefefe;
  height: ${navHeight}px;
  position: fixed;
  top: 0;
  width: 100%;
  box-shadow: 0 6px 10px 0 rgba(0, 0, 0, 0.19);
`;

// nav is fixed, so it needs padder underneath
const NavPadder = styled.div`
  height: ${navHeight}px;
`;

// nav items container using ul/li
const NavList = styled.ul`
  /* flex 1 makes it a flex 1 to its parent */
  flex: 1;
  /* display flex makes its children has flex effect */
  display: flex;
  flex-direction: row;
  list-style-type: none;
  margin: 0;
  padding: 0;
  /* put all children items to the right */
  justify-content: flex-end;
`;

const NavItem = styled.li`
  display: flex;
  margin: 0;
  padding: 0 20px;
  /* control height of this item here */
  height: ${navHeight}px;
  width: auto;
  justify-content: center;
  align-items: center;
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


const NavbarComponent = ({ children }) => (
  <React.Fragment>
    <Navbar>
      <NavContainer>
        <LogoWrapper>
          <StyledImg src={pennLogoURI} alt="Penn Logo" />
        </LogoWrapper>
        {
          children
            ? (
              <NavList>
                { children.map(x => <NavItem>{x}</NavItem>) }
              </NavList>
            )
            : null
        }
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
