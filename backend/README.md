# Backend for Penn events


We use Python as our backend. Backend mainly contains scripts to fetch events from Penn, search and recommendation API using [hug](https://www.hug.rest/), 
and index fetched events to `elasticsearch`. The hug backend is set by default to run on port `8888` and elasticsearch is run on port `9200`. 
See `backend` folder on how to run the backend scripts. 


## Fetch all events

`fetch_events.py` contains functions to fetch Penn events. We use GROBID to parse PDF 
and fetch all event to `data/events.json`. `create_events_features.py` contains a script 
to transform events to LSA vectors and list of search keywords.

```sh
bash serve_grobid.sh
python fetch_events.py # scrape data
python create_events_features.py # create LSA vectors and search candidates
```

**Running CRON to fetch event daily**

We can use CRON to make `fetch_events.py` constantly fetch events from Penn. Edit your `username` in `cron_fetch_events.py`
then run cron job by using the following script

```sh
python cron_fetch_events.py
```

## Serve ElasticSearch backend

Run the following to serve and index events to `elasticsearch`

```sh
bash serve_elasticsearch.sh # this will run elasticsearch by default at port 9200
python index_elasticsearch.py # index events and search candidates to elasticsearch
```


## Running Hug API locally

We use Hug API as a backend site for the recommendation engine. You can start Hug API by running:

```sh
hug -f hug_api.py -p 8888
```
