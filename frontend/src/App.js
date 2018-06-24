import { library } from '@fortawesome/fontawesome-svg-core';
import { faCalendarAlt, faMapMarkerAlt, faClock, faFileAlt, faExternalLinkAlt, faUserTie, faSchool, faUniversity, faBookmark } from '@fortawesome/free-solid-svg-icons';
import React, { Component } from 'react';
import styled, { injectGlobal } from 'styled-components';
import Fetcher from './Components/Fetcher';
import NavBar from './Components/Navbar';

// add fa font to use
library.add(
  faCalendarAlt, faMapMarkerAlt, faClock, faFileAlt,
  faExternalLinkAlt, faUserTie, faSchool, faUniversity,
  faBookmark,
);

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
      @import url('https://fonts.googleapis.com/css?family=Source+Code+Pro');

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
