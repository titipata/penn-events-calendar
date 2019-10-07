import React from 'react';
import styled from 'styled-components';
import PropTypes from 'prop-types';
import { Key } from '../../utils';
import { media } from '../../utils/ui';

// variables
const navHeight = 60;

// nav items container using ul/li
const NavList = styled.ul`
  /* flex 1 makes it a flex 1 to its parent */
  flex: 1;
  /* display flex makes its children has flex effect */
  display: flex;
  list-style-type: none;
  margin: 0;
  padding: 0;

  ${media.extraLarge`
    flex-direction: row;
    /* put all children items to the right */
    justify-content: flex-end;
  `}
  ${media.large`
    flex-direction: row;
    /* put all children items to the right */
    justify-content: flex-end;
  `}
  ${media.medium`
    flex-direction: column;
    justify-content: flex-end;
    flex: 1 1 100%;

    li {
      height: ${navHeight - 10}px;
    }

    li a {
      justify-content: flex-start;
    }

    & :active {
      background-color: #eee;
    }
  `}
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

  ${media.medium`
    padding: 0;
  `}
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
