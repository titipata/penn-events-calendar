import { graphql } from 'gatsby';
import React from 'react';
import Layout from '../components/layout';
import EventsContainer from '../components/EventsContainer';

export default ({ data }) => (
  <Layout>
    <h1>Upcoming Events</h1>
    <EventsContainer
      allEvents={data.allEventsCsv.edges}
    />
    {/* <div>
      {
        data.allEventsCsv.edges.map((x) => {
          const {
            date, title, description, starttime, endtime, speaker, owner, location, url,
          } = x.node;

          return (
            <span>
              <b>date:</b>
              <p>{date}</p>
              <b>title:</b>
              <p>{title}</p>
              <b>description:</b>
              <p>{description}</p>
              <b>starttime&nbsp;-&nbsp;endtime:</b>
              <p>
                {
                  starttime === endtime
                    ? starttime.replace(/[()]/g, '')
                    : `${starttime} - ${endtime}`
                }
              </p>
              <b>speaker: </b>
              <p>{speaker || '-'}</p>
              <b>owner: </b>
              <p>{owner}</p>
              <b>location: </b>
              <p>{location}</p>
              <b>url: </b>
              <p>{url}</p>
              <hr />
            </span>
          );
        })
      }
      <img
        src="https://2.bp.blogspot.com/-BMP2l6Hwvp4/TiAxeGx4CTI/AAAAAAAAD_M/XlC_mY3SoEw/s1600/panda-group-eating-bamboo.jpg"
        alt="Group of pandas eating bamboo"
      />
    </div> */}
  </Layout>
);

export const query = graphql`
  query {
    allEventsCsv {
      edges {
        node {
          id
          date_dt
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
