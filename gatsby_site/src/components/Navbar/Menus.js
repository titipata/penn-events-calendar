import React, { useState, useRef, useEffect } from 'react';
import styled, { css, keyframes } from 'styled-components';
import PropTypes from 'prop-types';
import { Key } from '../../utils';
import { media } from '../../utils/ui';

// variables
const navHeight = 60;
const animateMenu = (startH, endH) => keyframes`
  0% {
    height: ${startH}px;
  }
  100% {
    height: ${endH}px;
  }
`;

// nav items container using ul/li
const NavList = styled.ul`
  /* flex 1 makes it a flex 1 to its parent */
  flex: 1;
  /* display flex makes its children has flex effect */
  display: flex;
  list-style-type: none;
  margin: 0;
  padding: 0;
  overflow: hidden;

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
    display: block;
    flex-direction: column;
    justify-content: flex-end;
    flex: 1 1 100%;

    li {
      height: ${navHeight - 10}px;
    }

    li:last-child {
      margin-bottom: 5px;
    }

    li a {
      justify-content: flex-start;
    }

    & :active {
      background-color: #eee;
    }

    ${props => (props.hidden
    ? css`
      animation: ${props.hideDuration || 0}s ${props.animateHide} forwards;
    ` : css`
      animation: 0.5s ${props.animateShow} forwards;
    `)}
  `}
`;

const NavItem = styled.li`
  display: flex;
  margin: 0;
  padding: 0 20px;
  width: auto;
  justify-content: center;
  align-items: center;

  ${media.medium`
    padding: 0 10px;
  `}
`;

const Menus = ({ items, hidden }) => {
  // workaround for hiding hiccup on first load
  const [hideDuration, setHideDuration] = useState(false);
  const [menuHeight, setMenuHeight] = useState(null);
  const navListRef = useRef(null);

  useEffect(() => {
    setMenuHeight(navListRef.current.scrollHeight);
    setTimeout(() => {
      setHideDuration(0.5);
    }, 500);
  }, [navListRef]);

  if (items.length === 0) {
    return null;
  }

  return (
    <NavList
      hidden={hidden}
      animateHide={animateMenu(menuHeight, 0)}
      animateShow={animateMenu(0, menuHeight)}
      hideDuration={hideDuration}
      ref={navListRef}
    >
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
  hidden: PropTypes.bool,
};

Menus.defaultProps = {
  items: [],
  hidden: true,
};

export default Menus;
