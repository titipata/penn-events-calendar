import PropTypes from 'prop-types';
import React from 'react';
import styled from 'styled-components';
import { Container } from '../BaseComponents';

const pennLogo = require('../../images/penn-logo.png');

const StyledNavBar = styled.div`
  height: 60px;
  color: white;
  background-color: #1E303C;

  display: flex;
  align-items: center;
`;

const StyledBrandText = Container.extend`
  color: white;
  font-weight: bold;
  padding: 15px;
  /* https://stackoverflow.com/a/30426639/4010864 */
  flex-basis: auto; /* default value */
  flex-grow: 0;
`;

const NavBar = ({ brandname }) => (
  <StyledNavBar>
    <StyledBrandText>
      <img src={pennLogo} alt="Logo" />
      { brandname }
    </StyledBrandText>
  </StyledNavBar>
);

NavBar.propTypes = {
  brandname: PropTypes.string.isRequired,
};

export default NavBar;
