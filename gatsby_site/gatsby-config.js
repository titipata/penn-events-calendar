module.exports = {
  pathPrefix: '/penn-events',
  siteMetadata: {
    title: 'Penn Event Calendar',
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
        name: 'data',
        path: `${__dirname}/../backend/data/`,
      },
    },
    'gatsby-transformer-json',
  ],
};
