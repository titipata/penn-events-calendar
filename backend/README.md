# Backend for Penn events

We use Python as our backend. Backend mainly contains scripts to fetch events from Penn, search and recommendation API using [hug](https://www.hug.rest/), and index fetched events to `Elasticsearch`. For development, the hug backend is set by default to run on port `8888` and `Elasticsearch` is run on port `9200`. See `backend` folder on how to run the backend scripts.

## Fetch events

The `fetch_events.py` script contains functions to fetch Penn events. We use GROBID to parse PDF and fetch all event to `data/events.json`. `create_events_features.py` contains a script to transform events to LSA vectors and list of search keywords.

```sh
bash serve_grobid.sh
python fetch_events.py # scrape data
python create_events_features.py # create LSA vectors and search candidates
```

## Serve and index events to `Elasticsearch`

Run the following to serve and index events to `Elasticsearch`

```sh
bash serve_elasticsearch.sh # this will run Elasticsearch by default at port 9200
python index_elasticsearch.py # index events and search candidates to Elasticsearch
```

## Running schedule to fetch, index events weekly

We use [`schedule`](https://github.com/dbader/schedule) to fetch events weekly from Penn using `fetch_events.py`.
You can run

```**sh**
python schedule_fetch_events.py
```

in order to schedule the script for fetching, creating features, and indexing events to `Elasticsearch`.

## Running Hug API locally

We use Hug API as a backend site for the search keywords and recommendation engine. You can start Hug API by running:

```sh
hug -f hug_api.py -p 8888
```

To serve hug with `uwsgi`, use the following command

```sh
uwsgi --http 127.0.0.1:8888 --wsgi-file hug_api.py -p 2 --callable __hug_wsgi__
```

this will serve `uwsgi` with 2 processes. Before running, make sure that `uwsgi` is installed via `conda install -c conda-forge uwsgi`. If it does not work, you might have to check this [Stack Overflow post](https://stackoverflow.com/questions/41775441/chef-installing-uwsgi-libiconv-so-2-no-such-file-or-directory).

## Requirements

Apart from the packages specified in `requirements.txt`, you need to download corpora and models
from `nltk` and `spacy` respectively.

```sh
python -m nltk.downloader all
python -m spacy download en_core_web_sm
```
