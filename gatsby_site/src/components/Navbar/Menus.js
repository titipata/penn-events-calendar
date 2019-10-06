import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import { Key } from '../../utils';

// variables
const navHeight = 60;

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

const Menus = ({ items }) => {
  if (items.length === 0) {
    return null;
  }

  return (
    <NavList>
      {
        items.map(item => (
          <NavItem key={Key.getShortKey()}>
            {item}
          </NavItem>
        ))
      }
    </NavList>
  );
};

Menus.propTypes = {
  items: PropTypes.arrayOf(PropTypes.node),
};

Menus.defaultProps = {
  items: [],
};

export default Menus;
