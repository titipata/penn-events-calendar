import { graphql } from 'gatsby';
import React from 'react';
import Layout from '../components/layout';

export default ({ data }) => (
  <Layout>
    <h1>Amazing Pandas Eating Things</h1>
    <div>
      <p>
        {JSON.stringify(data)}
      </p>
      <img
        src="https://2.bp.blogspot.com/-BMP2l6Hwvp4/TiAxeGx4CTI/AAAAAAAAD_M/XlC_mY3SoEw/s1600/panda-group-eating-bamboo.jpg"
        alt="Group of pandas eating bamboo"
      />
    </div>
  </Layout>
);

export const query = graphql`
  query {
    allEventsCsv {
      edges {
        node {
          id
          date
          title
          description
          starttime
          endtime
          speaker
          owner
          location
          url
        }
      }
    }
  }
`;
