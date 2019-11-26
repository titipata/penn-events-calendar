
# Frontend for Penn events

You can run frontend site by the following:

```sh
# only once on first time
npm install -g gatsby-cli

# run the frontend app
npm install
npm start
```

By default, this will concurrently run Gatsby frontend site at port `8000`, hug API backend at port `8888`, and `Elasticsearch` at port `9200`.

## Running on remote server

To make it run on a remote server, you can do the following:

- Run `npm` command with an extra arguments:

```js
npm run gatsby-prod -- -H <host_name>
```

## Customize metadata and Google Analytics

`gatsby-config.js` contains a script for site metadata for social media sharing and Google Analytics tracking. You can edit this file before serving the frontend.

## Gatsby documentation

Full documentation for Gatsby can be found [here](https://www.gatsbyjs.org/).
