#!/usr/bin/python
import os
import requests
import json
import time
from unidecode import unidecode
from datetime import datetime
from dateutil import parser
from lxml import etree, html
from bs4 import BeautifulSoup

DAYS = [
    "Mon", "Tue",
    "Wed", "Thu",
    "Fri", "Sat",
    "Sun"
]
PATH_JSON = 'events.json'


def read_json(file_path):
    """
    Read collected file from path
    """
    if not os.path.exists(file_path):
        events = []
        return events
    else:
        with open(file_path, 'r') as fp:
            events = [json.loads(line) for line in fp]
        return events


def save_json(ls, file_path):
    """
    Save list of dictionary to JSON
    """
    with open(file_path, 'w') as fp:
        fp.write('\n'.join(json.dumps(i) for i in ls))


def convert_event_to_dict(event):
    """
    Convert event XML to dictionary
    """
    event_dict = {}
    keys = [
        'date', 'starttime', 'endtime',
        'title', 'description', 'location',
        'room', 'url', 'student', 'privacy',
        'category', 'school', 'owner',
        'link'
    ]
    for key in keys:
        value = event.find(key).text or ''
        if key == 'description' :
            value = BeautifulSoup(value, 'html.parser').text # description
        elif key in ('starttime', 'endtime'):
            value = datetime.strptime(value, "%H:%M:%S").strftime("%I:%M %p")
        elif key == 'date':
            event_dict[key] = value
            dow = parser.parse(value).weekday()
            event_dict['day_of_week'] = DAYS[dow]
        elif key == 'url':
            if len(value) > 0:
                event_dict['event_id'] = int(value.rsplit('/')[-1])
            else:
                event_dict['event_id'] = ''
        else:
            value = unidecode(value)
        event_dict[key] = value
    return event_dict


def fetch_events():
    """
    Saving Penn events to JSON format
    """
    URL = 'http://www.upenn.edu/calendar-export/?showndays=50'
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    events = tree.findall('event')

    # read JSON file is exist
    if os.path.isfile(PATH_JSON):
        events_list = read_json(PATH_JSON)
    else:
        events_list = []

    for event in events:
        try:
            event_dict = convert_event_to_dict(event)
            if len(events_list) > 0:
                event_ids = [e_['event_id'] for e_ in events_list]
            else:
                event_ids = []
            if event_dict['event_id'] not in event_ids:
                events_list.append(event_dict)
        except:
            pass
    save_json(events_list, PATH_JSON)
    print('Events Downloaded!')


if __name__ == '__main__':
    fetch_events()
