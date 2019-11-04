const path = require('path');

exports.createPages = ({ graphql, actions }) => {
  const { createPage } = actions;

  return graphql(`
    {
      allEventsJson(
        sort: { fields: date_dt, order: DESC }
      ) {
        edges {
          node {
            date_dt
            description
            endtime
            event_index
            location
            owner
            speaker
            starttime
            title
            url
          }
        }
      }
    }
  `).then((result) => {
    if (result.errors) {
      throw result.errors;
    }

    // get all events
    const events = result.data.allEventsJson.edges;

    // Create blog post list pages
    const eventsPerPage = 30;
    const numPages = Math.ceil(events.length / eventsPerPage);

    Array.from({ length: numPages }).forEach((_, i) => {
      createPage({
        path: i === 0 ? '/' : `/${i + 1}`,
        component: path.resolve('./src/templates/event-list.js'),
        context: {
          limit: eventsPerPage,
          skip: i * eventsPerPage,
          numPages,
          currentPage: i + 1,
        },
      });
    });
  });
};
