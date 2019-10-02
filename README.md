# Events at the University of Pennsylvania

All events happening at the University of Pennsylvania event with built-in search and recommendation engine.
The repository contains **backend** and **frontend (gatsby_site)**.

### Backend

We use Python as our backend. Backend mainly contains scripts to fetch events from Penn, search and recommendation API using [hug](https://www.hug.rest/), 
and index fetched events to `elasticsearch`. See `backend` folder on how to run the backend scripts

### Frontend

We use react-js as a front-end. Before running, make sure that you have recent version of `npm` installed (NodeJS 8+).

In order to run the web-application, if it is the first time, you need to install `gatsby-cli`:

```sh
# only once on first time
npm install -g gatsby-cli
```

and run front-end application from the `gatsby_site` folder as follows:

```sh
cd gatsby_site
npm install
gatsby develop
```

This will run Gatsby site on port `8000`. You will see the demo looks something like the following:


## Core members

- [titipata](https://github.com/titipata)
- [bluenex](https://github.com/bluenex)
- [kittinan](https://github.com/kittinan)

## Sponsors

This project is sponsored by professor [David Meaney](https://www.seas.upenn.edu/directory/profile.php?ID=64) and 
professor [Konrad Kording](http://kordinglab.com) from Department of Bioengineering at 
the University of Pennsylvania.


## Contributions

We are welcome to all contribution. If you spot any errors in the web-application, 
please feel free to report them in the issue.
