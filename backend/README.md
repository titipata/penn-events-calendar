# Flask back-end for Penn event

## Fetch events

`fetch_events.py` contains functions to fetch Penn events. We can run GROBID and fetch to update data in `data/events.json` file
as follows

```sh
bash serve_grobid.sh
python fetch_events.py
```

## Running CRON to fetch event daily

We use CRON to make `fetch_events.py` constantly fetch Penn events. Change `username` in `cron_fetch_events.py`
then run cron job by using the following script

```sh
python cron_fetch_events.py
```

## Serve ElasticSearch

Run the following to serve and index events to `elasticsearch`

```
bash serve_elasticsearch.sh
python index_elasticsearch.py
```


## Running Hug API locally

Start Hug API by running:

```sh
hug -f hug_api.py -p 8888
```
