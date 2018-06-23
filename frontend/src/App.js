import React, { Component } from 'react';
import styled, { injectGlobal } from 'styled-components';
import Fetcher from './Components/Fetcher';
import NavBar from './Components/Navbar';

const AppWrapper = styled.div`
  /* sticky footer */
  display: flex;
  height: 100%;
  min-height: 100vh;
  flex-direction: column;
`;

const Container = styled.div`
  flex: 1;
`;

class App extends Component {
  componentDidMount() {
    this.globals = injectGlobal`
      body {
        margin: 0;
        padding: 0;
        font-family: -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif,"Apple Color Emoji","Segoe UI Emoji","Segoe UI Symbol";
      }
    `;
  }

  componentWillUnmount() {
    this.globals.remove();
  }

  render() {
    return (
      <AppWrapper>
        <NavBar brandname="Events at Penn" />

        <Container>
          Content goes here!
          
          <Fetcher />

        </Container>

        <NavBar brandname="this is footer" />
      </AppWrapper>
    );
  }
}

export default App;
