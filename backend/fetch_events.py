#!/usr/bin/python
import os
import requests
import json
import time
from unidecode import unidecode
from datetime import datetime
import dateutil.parser
from itertools import chain
from lxml import etree, html
from bs4 import BeautifulSoup
from urllib.parse import urljoin


PATH_JSON = 'events.json'
URL = 'http://www.upenn.edu/calendar-export/?showndays=50'


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

            # get current event ids
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


def stringify_children(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ''.join(filter(None, parts))


def extract_event_details(event_site):
    """
    Extract event details from CNI detail page
    """
    dt, location, description = [stringify_children(s).strip() 
                                 for s in event_site.xpath('//div[@class="field-item even"]')]
    event_time = dateutil.parser.parse(dt)
    date = event_time.strftime("%Y-%m-%d")
    starttime = event_time.strftime("%I:%M %p")
    title = event_site.xpath('//h1[@class="page-header"]')[0].text

    event_json = {
        "date": date,
        "starttime": starttime,
        "endtime": "",
        "title": title,
        "description": description,
        "location": location,
        "room": "",
        "student": "0",
        "privacy": "0",
        "category": "CNI",
        "school": "Computational Neuroscience Initiative",
        "owner": "Computational Neuroscience Initiative",
        "link": ""
    }
    return event_json


def fetch_events_cni():
    """
    Saving Computational Neuroscience Initiative to JSON format
    """

    # read JSON file is exist
    if os.path.isfile(PATH_JSON):
        events_list = read_json(PATH_JSON)
    else:
        events_list = []

    page = requests.get('https://cni.upenn.edu/events')
    site = html.fromstring(page.text)
    events = site.xpath('//h4/span/a[@href]/@href') # all events
    for event_id in events:
        try:
            event_url = urljoin('https://cni.upenn.edu/events', event_id)
            event_page = requests.get(event_url)
            event_site = html.fromstring(event_page.text)
            event_dict = extract_event_details(event_site)
            event_dict['event_id'] = event_id
            event_dict['url'] = event_url

            # get current event ids
            if len(events_list) > 0:
                event_ids = [e_['event_id'] for e_ in events_list]
            else:
                event_ids = []
            if event_dict['event_id'] not in event_ids:
                events_list.append(event_dict)
        except:
            pass

    save_json(events_list, PATH_JSON)
    print('CNI Events Downloaded!')


if __name__ == '__main__':
    fetch_events()
    fetch_events_cni()