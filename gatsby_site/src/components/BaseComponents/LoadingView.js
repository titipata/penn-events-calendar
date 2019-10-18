import React from 'react';
import Loader from 'react-spinners/ClipLoader';
import styled from 'styled-components';

const Wrapper = styled.div`
  display: flex;
  flex: 1 1 100%;
  justify-content: center;
  align-items: center;
  margin-top: 22vh;
`;

const LoadingView = () => (
  <Wrapper>
    <Loader
      sizeUnit="px"
      size={60}
      color="#8cb3d9"
      loading
    />
  </Wrapper>
);

export default LoadingView;
