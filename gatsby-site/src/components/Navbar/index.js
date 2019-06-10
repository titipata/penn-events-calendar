import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Container } from '../BaseComponents';

const pennLogo = require('../../images/penn-logo.png');

const navHeight = '3.75rem';

const StyledNavBar = styled.div`
  font-family: 'Open Sans';
  height: auto;
  color: white;
  /* background-color: #1E303C; */
  background-color: white;

  display: flex;
  align-items: center;

  padding-top: 15px;
  padding-bottom: 5px;
`;

const NavContainer = Container.extend`
  /* https://stackoverflow.com/a/30426639/4010864 */
  flex-basis: auto; /* default value */
  flex-grow: 0;
  display: flex;
  flex-direction: column;
  /* justify-content: space-between; */
`;

const StyledBrandText = styled.div`
  align-items: center;
  color: #1E303C;
  /* display: flex; */
  font-size: 1.05rem;
  font-weight: bold;
  padding-top: 5px;
  text-align: center;
`;

const LogoWrapper = styled.div`
  padding: 0 15px;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const StyledLogo = styled.img`
  height: ${navHeight};
  mix-blend-mode: multiply;
`;

const NavBar = ({ brandname }) => (
  <StyledNavBar>
    <NavContainer>
      <LogoWrapper>
        <StyledLogo src={pennLogo} alt="Logo" />
      </LogoWrapper>
      <StyledBrandText>
        { brandname }
      </StyledBrandText>
    </NavContainer>
  </StyledNavBar>
);

NavBar.propTypes = {
  brandname: PropTypes.string.isRequired,
};

export default NavBar;
