import React from 'react';
import styled from 'styled-components';

const StyledFooter = styled.div`
  height: 100px;
  background-color: #44464b;

  display: flex;
  align-items: center;
  justify-content: center;
`;

const StyledFooterText = styled.div`
  text-align: center;
  color: white;
`;

const StyledLink = styled.a.attrs({
  target: '_blank',
  rel: 'noopener noreferrer',
})`
  color: #419eda;
`;

const Footer = () => (
  <StyledFooter>
    <StyledFooterText>
      Made at&nbsp;
      <StyledLink href="http://kordinglab.com/">kordinglab.com</StyledLink>
      &nbsp;at University of Pennsylvania
      <br />
      Help us make it better at&nbsp;
      <StyledLink href="https://github.com/titipata/penn-events-calendar/issues/">titipata/penn-events-calendar</StyledLink>
    </StyledFooterText>
  </StyledFooter>
);

export default Footer;
