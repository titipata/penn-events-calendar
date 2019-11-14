module.exports = {
  proxy: {
    prefix: '/api',
    url: 'http://localhost:8888',
  },
  pathPrefix: '/penn-events',
  siteMetadata: {
    title: 'Events at Penn',
    description: 'A web application that collects all events happening at the University of Pennsylvania with built-in search and recommendation engine.',
    siteUrl: 'http://35.160.123.103',
    image: 'http://35.160.123.103/og-image-penn.png',
    logo: 'http://35.160.123.103/favicon.ico',
    type: 'website',
  },
  plugins: [
    {
      resolve: 'gatsby-plugin-typography',
      options: {
        pathToConfigModule: 'src/utils/typography',
      },
    },
    {
      resolve: 'gatsby-plugin-styled-components',
      options: {
        // Add any options here
      },
    },
    'gatsby-plugin-eslint',
    {
      resolve: 'gatsby-source-filesystem',
      options: {
        path: `${__dirname}/../backend/data/events.json`,
      },
    },
    'gatsby-transformer-json',
    'gatsby-plugin-react-helmet',
    {
      resolve: 'gatsby-plugin-google-analytics',
      options: {
        trackingId: 'UA-152564648-1',
        exclude: ['/*.png', '/*.ico', '/static/**'],
      },
    },
  ],
};
