# Events at the University of Pennsylvania

A web application that collects all events happening at the University of Pennsylvania with built-in search and recommendation engine.

## Run web application

We use [`Gatsby.js`](https://www.gatsbyjs.org/) as our frontend. The frontend is located in `gatsby_site` folder. Before running, make sure that you have a recent version of `npm` installed (NodeJS 8+). If it is the first time, you need to install `gatsby-cli`.

```sh
# only once on first time
npm install -g gatsby-cli
```

and run frontend application from the [`gatsby_site`](https://github.com/titipata/penn-events-calendar/tree/master/gatsby_site) folder as follows:

```sh
cd gatsby_site
npm install
npm start
```

Then index given example data to `Elasticsearch` located in [`backend/data`](https://github.com/titipata/penn-events-calendar/tree/master/backend/data) using:

```sh
npm run index-elastic # index data to Elasticsearch
```

By default, this will concurrently run Gatsby frontend site at port `8000`, hug API backend at port `8888`, and `Elasticsearch` at port `9200`. For deployment, use `npm run deploy` instead. This will run the site at port `9000`. See [`gatsby_site`](https://github.com/titipata/penn-events-calendar/tree/master/gatsby_site#running-on-remote-server), to see how to run on a remote server.

**For production** see [`devops`](https://github.com/titipata/penn-events-calendar/tree/master/devops) folder on how to set up [supervisord](http://supervisord.org).

## Customize for your events

You can customize the site so that it works on your events. Please see `backend` on how to create your own fetch events script and `frontend` on how to customize site's metadata and Google Analytics.

## Usage

Here is an instruction on how to use the web application:

1. See upcoming events on the main page, search for anything you are interested

    ![upcoming-search.png](images/upcoming-search.png)

2. Select events by clicking the star icon

    ![images/search-result.png](images/search-result.png)

3. See recommendation based on your selected events

    ![images/recommendation.png](images/recommendation.png)

## Core members

- Titipat Achakulvisut ([titipata](https://github.com/titipata))
- Tulakan Ruangrong ([bluenex](https://github.com/bluenex))
- Kittinan Srithaworn ([kittinan](https://github.com/kittinan))

## Sponsors

This project is sponsored by Department of Bioengineering at the University of Pennsylvania thanks to professor [David Meaney](https://www.seas.upenn.edu/directory/profile.php?ID=64) and professor [Konrad Kording](http://kordinglab.com).

## Contributions

We are welcome to all contribution. If you spot any errors, incomplete events or missing events on the web application, please feel free to report them on the [issue page](https://github.com/titipata/penn-events-calendar/issues).
