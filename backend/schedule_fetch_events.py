import schedule
import time
from datetime import datetime

from fetch_events import fetch_all_events
from create_events_features import create_events_feautures
from index_elasticsearch import index_events_elasticsearch

def job():
    fetch_all_events() # fetch all events
    create_events_feautures() # create events features: event topics, search keywords
    index_events_elasticsearch() # index events and keywords to elasticsearch
    print("Done fetching events at {}...".format(str(datetime.now())))


schedule.every().sunday.at("23:59").do(job)
while True:
    schedule.run_pending()
    time.sleep(300)
