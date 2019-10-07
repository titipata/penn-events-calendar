// Burger.js
import React from 'react';
import styled from 'styled-components';
import { media } from '../../utils/ui';

export const StyledBurger = styled.button`
  /* position: absolute; */
  display: none;
  flex-direction: column;
  justify-content: space-around;
  width: 1.5rem;
  height: 1.5rem;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 999;

  &:focus {
    outline: none;
  }

  div {
    width: 1.5rem;
    height: 0.2rem;
    background: #333;
    border-radius: 15px;
    transition: all 0.3s linear;
    position: relative;
    transform-origin: 1px;
  }

  ${media.medium`
    display: flex;
  `}
`;

const Burger = () => (
  <StyledBurger>
    <div />
    <div />
    <div />
  </StyledBurger>
);

export default Burger;
