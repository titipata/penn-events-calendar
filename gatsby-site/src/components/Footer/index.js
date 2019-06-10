import React from 'react';
import styled from 'styled-components';
import { Container } from '../BaseComponents';

const StyledFooter = styled.div`
  height: auto;
  background-color: #44464b;
  font-family: 'Open Sans';

  display: flex;
  align-items: center;
  justify-content: center;

  margin-top: 1rem;
  padding: 1.8rem 0;
`;

const StyledFooterText = styled.div`
  text-align: center;
  color: white;
`;

const StyledLink = styled.a.attrs({
  target: '_blank',
  rel: 'noopener noreferrer',
})`
  color: #e0e0e0;
`;

const Footer = () => (
  <StyledFooter>
    <Container>
      <StyledFooterText>
        Made at <StyledLink href="http://kordinglab.com/">kordinglab.com</StyledLink> at University of Pennsylvania
        <br />
        Help us make it better at <StyledLink href="https://github.com/titipata/penn-events-calendar/issues/">titipata/penn-events-calendar</StyledLink>
      </StyledFooterText>
    </Container>
  </StyledFooter>
);

export default Footer;
