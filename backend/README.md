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


## Running Flask API locally

Start Flask API by running

```sh
python api.py
```


## Dependencies

All dependencies are in `requirements.txt` file, you can install all dependencies by running

```sh
pip install -r requirements.txt
```

And download `spacy` model

```sh
python -m spacy download en_core_web_sm
```