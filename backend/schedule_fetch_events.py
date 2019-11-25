import os
import subprocess
from pathlib import Path

import schedule
import time
from datetime import datetime

from fetch_events import fetch_all_events
from create_events_features import create_events_features
from index_elasticsearch import index_events_elasticsearch
import config

home_dir = str(Path.home())
if not os.path.isdir(os.path.join(home_dir, 'nltk_data')):
    subprocess.run(['python', '-m', 'nltk.downloader', 'all'])
subprocess.run(['python', '-m', 'spacy', 'download', 'en_core_web_sm'])


def job():
    print("Start fetching events...")
    subprocess.run(['supervisorctl', 'start', 'supervisor-grobid']) # start GROBID
    time.sleep(30)
    fetch_all_events(config.scrapers) # fetch all events
    subprocess.run(['supervisorctl', 'stop', 'supervisor-grobid']) # stop GROBID

    create_events_features() # create events features: event topics, search keywords
    index_events_elasticsearch() # index events and keywords to elasticsearch
    print("Done fetching events at {}...".format(str(datetime.now())))

    # restart supervisor-hug after fetching
    subprocess.run(['supervisorctl', 'restart', 'supervisor-hug'])
    subprocess.run(['supervisorctl', 'restart', 'supervisor-gatsby'])


schedule.every().sunday.at("23:59").do(job)
while True:
    schedule.run_pending()
    time.sleep(300)
