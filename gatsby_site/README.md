
# Frontend for Penn events

You can run frontend site by the following:

```sh
# only once on first time
npm install -g gatsby-cli

# run the frontend app
npm install
npm start
```

By default, this will concurrently run Gatsby frontend site at port `8000`, hug API backend at port `8888`, and ElasticSearch at port `9200`.

## Running on remote server

To make it run on a remote server, you can do the following:

- Run `npm` command with an extra arguments:

```js
npm run gatsby-prod -- -H <host_name>
```


## Gatsby documentation

Full documentation for Gatsby can be found [here](https://www.gatsbyjs.org/).
