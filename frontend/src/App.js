import { library } from '@fortawesome/fontawesome-svg-core';
import { faBookmark, faCalendarAlt, faClock, faExternalLinkAlt, faFileAlt, faMapMarkerAlt, faSchool, faUniversity, faUserTie } from '@fortawesome/free-solid-svg-icons';
import React, { Component } from 'react';
import styled, { injectGlobal } from 'styled-components';
import { Container } from './Components/BaseComponents';
import EventsContainer from './Components/EventsContainer';
import Fetcher from './Components/Fetcher';
import NavBar from './Components/Navbar';
import Footer from './Components/Footer';

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

class App extends Component {
  componentDidMount() {
    this.globals = injectGlobal`
      @import url('https://fonts.googleapis.com/css?family=Source+Code+Pro');
      @import url('https://fonts.googleapis.com/css?family=Open+Sans');

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
        <NavBar brandname="Upcoming Events" />

        <Fetcher />

        <Container>
          <EventsContainer />
        </Container>

        <Footer />
      </AppWrapper>
    );
  }
}

export default App;
