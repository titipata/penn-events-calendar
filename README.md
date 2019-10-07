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

Then index given example data to elasticsearch located in `backend/data` using

```sh
npm run index-elastic # index data to elasticsearch
```

By default, this will concurrently run Gatsby frontend site at port `8000`, 
hug API backend at port `8888`,  and ElasticSearch at port `9200`. 
For deployment, use `npm run deploy` instead. This will run the site at port `9000`.
See `gatsby_site`, to see how to run on a remote serveer.

**For production** see `devops` folder on how to set up [supervisord](http://supervisord.org)


## Usage

Here is an instruction on how to use the web application

1. See upcoming events on the main page, search for anything you are interested

<img src="images/upcoming-search.png" width="700" />

2. Select events by clicking the star icon

<img src="images/search-result.png" width="700" />

3. See recommendation based on your selected events

<img src="images/recommendation.png" width="700" />


## Core members

- Titipat Achakulvisut ([titipata](https://github.com/titipata))
- Tulakan Ruangrong ([bluenex](https://github.com/bluenex))
- Kittinan Srithaworn ([kittinan](https://github.com/kittinan))


## Sponsors

This project is sponsored by Department of Bioengineering at the University of Pennsylvania 
thanks to professor [David Meaney](https://www.seas.upenn.edu/directory/profile.php?ID=64) and 
professor [Konrad Kording](http://kordinglab.com).


## Contributions

We are welcome to all contribution. If you spot any errors, events incomplete or events missing on the web application, 
please feel free to report them on the [issue page](https://github.com/titipata/penn-events-calendar/issues).
