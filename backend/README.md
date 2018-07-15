# Flask back-end for Penn event


## Running CRON to fetch event daily

We use `cron` to constantly fetch Penn events. Change `username` in `cron_fetch_events`
then run cron job by using the following script

```sh
python cron_fetch_events.py
```


## Running Flask API locally

Start API by running

```sh
python api.py
```


## Dependencies

All dependencies are in `requirements.txt` file, you can install all dependencies by running

```sh
pip install -r requirements.txt
```

Download `spacy` model

```sh
python -m spacy download en_core_web_sm
```