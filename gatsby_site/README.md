
# Frontend for Penn events

You can run front-end site by the following

```sh
# only once on first time
npm install -g gatsby-cli
```

```sh
npm install
npm start
```

By default, this will concurrently run Gatsby frontend site at port `8000`, hug API backend at port `8888`, 
and ElasticSearch at port `9200`. For deployment, use `npm run deploy` instead. This will run the site at port `9000`.


## Running on remote server

To make it run on a remote server, you can do the following

- Change hostname is `package.json`

```js
"gatsby-prod": "gatsby build && gatsby serve -H bleen.seas.upenn.edu"
```


## Gatsby documentation

Full documentation for Gatsby can be found [here](https://www.gatsbyjs.org/).
