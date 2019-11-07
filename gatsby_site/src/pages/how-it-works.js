import React from 'react';
import styled from 'styled-components';
import Layout from '../components/layout';

const HeaderWrapper = styled.div`
  display: flex;
  align-items: center;
`;

const StyledImg = styled.img`
  border-radius: 5px;
  border: 1px solid #ddd;
  padding: 3px;
  margin-top: 10px;
`;

const img1 = require('../images/instruction-1.png');
const img2 = require('../images/instruction-2.png');
const img3 = require('../images/instruction-3.png');

export default () => (
  <Layout>
    <HeaderWrapper>
      <h1>How it works</h1>
    </HeaderWrapper>
    <p>
      This web application collects all events happening at the University of Pennsylvania with
      built-in search and recommendation engine. Here is an instruction on how to use the web
      application:
    </p>
    <ul>
      <li>
        See upcoming events on the main page, search for anything you are interested:
        <StyledImg src={img1} alt="upcoming events" />
      </li>
      <li>
        Select events by clicking the star icon:
        <StyledImg src={img2} alt="select events" />
      </li>
      <li>
        See recommendation based on your selected events:
        <StyledImg src={img3} alt="recommendations" />
      </li>
    </ul>
  </Layout>
);
