# Events at the University of Pennsylvania

All events happening at the University of Pennsylvania event with built-in search and recommendation engine.


## Run web application

We use [`Gatsby.js`](https://www.gatsbyjs.org/) as our frontend. The frontend is located in `gatsby_site` folder. 
Before running, make sure that you have recent version of `npm` installed (NodeJS 8+).
If it is the first time, you need to install `gatsby-cli`.

```sh
# only once on first time
npm install -g gatsby-cli
```

and run front-end application from the `gatsby_site` folder as follows:

```sh
cd gatsby_site
npm install
npm start
```

Then index given example data to elasticsearch using

```sh
npm run index-elastic # index data to elasticsearch
```

By default, this will concurrently run Gatsby frontend site at port `8000`, 
hug API backend at port `8888`,  and ElasticSearch at port `9200`. 
For deployment, use `npm run deploy` instead. This will run the site at port `9000`.


## Core members

- Titipat Achakulvisut ([titipata](https://github.com/titipata))
- Tulakan Ruangrong ([bluenex](https://github.com/bluenex))
- Kittinan Srithaworn ([kittinan](https://github.com/kittinan))


## Sponsors

This project is sponsored by professor [David Meaney](https://www.seas.upenn.edu/directory/profile.php?ID=64) and 
professor [Konrad Kording](http://kordinglab.com) from Department of Bioengineering at 
the University of Pennsylvania.


## Contributions

We are welcome to all contribution. If you spot any errors in the web-application, 
please feel free to report them on the [issue page](https://github.com/titipata/penn-events-calendar/issues).
