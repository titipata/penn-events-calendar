# Events at the University of Pennsylvania

All events happening at the University of Pennsylvania event with built-in search and recommendation engine.

### Backend

We use Python as our backend. Backend mainly contains scripts to fetch events from Penn, search and recommendation API using [hug](https://www.hug.rest/), 
and index fetched events to `elasticsearch`. The hug backend is set by default to run on port `8888` and elasticsearch is run on port `9200`. 
See `backend` folder on how to run the backend scripts. 

In short, you can start backend server with a given example data by running and indexing data into `elasticsearch`

```sh
bash serve_elasticsearch.sh
python index_elasticsearch.py
```


### Frontend

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

This will, by default, concurrently run Gatsby frontend site on port `8000` and hug API backend on port `8888`.


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
