#!/usr/bin/python
import os
import re
import requests
import json
import time
from unidecode import unidecode
from datetime import datetime, timedelta
import dateutil.parser
from itertools import chain
from lxml import etree, html
from bs4 import BeautifulSoup
from urllib.parse import urljoin


PATH_JSON = 'events.json'
PATH_SIMILAR_EVENTS = 'similar_events.json'


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
                event_dict['event_id'] = str(int(value.rsplit('/')[-1]))
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
    base_url = 'http://www.upenn.edu/calendar-export/?showndays=50'
    page = requests.get(base_url)
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


def fetch_events_english_dept():
    """
    Saving English Department events to JSON format
    """

    # read JSON file is exist
    if os.path.isfile(PATH_JSON):
        events_list = read_json(PATH_JSON)
    else:
        events_list = []

    base_url = 'https://www.english.upenn.edu/events/calendar-export/'
    page = requests.get(base_url)
    site = html.fromstring(page.text)
    events = site.xpath('//ul[@class="unstyled"]//li//span[@class="field-content"]')
    events = events[0]
    event_months = [stringify_children(e).strip() for e in events.xpath('//div[@class="month-date"]')]
    event_days = [stringify_children(e).strip() for e in events.xpath('//div[@class="day-date"]')]
    event_locations = events.xpath('//p[@class="location"]/text()')

    starttimes = []
    endtimes = []
    for div in events.xpath('//div[@class="date-time"]'):
        event_time = div.find('span[@class="date-display-single"]')
        if event_time is not None and event_time.find('span[@class="date-display-start"]') is not None:
            starttime = event_time.find('span[@class="date-display-start"]').text
            endtime = event_time.find('span[@class="date-display-end"]').text
            starttimes.append(starttime)
            endtimes.append(endtime)
        else:
            starttimes.append(event_time.text or '')
            endtimes.append(event_time.text or '')

    titles = [span.find('a').text for span in events.xpath('//span[@class="field-content"]') 
            if span.find('a') is not None]
    urls = [span.find('a').attrib.get('href') for span in events.xpath('//span[@class="field-content"]') 
            if span.find('a') is not None]
    descriptions = [stringify_children(e).strip() for e in events.xpath('//div[@class="span10"]')]

    for (month, day, location, starttime, endtime, title, description, url) in zip(event_months, event_days, event_locations, starttimes, endtimes, titles, descriptions, urls):
        try:
            date = '{} {}'.format(day, month)
            event_dict = {
                "date": dateutil.parser.parse(re.sub('\d+ to \d+', '', date)).strftime("%Y-%m-%d"),
                "starttime": starttime,
                "endtime": endtime,
                "title": title,
                "description": description,
                "location": location,
                "room": "",
                "event_id": url + date, # using url and date, probably change later
                "url": urljoin(base_url, url),
                "student": "0",
                "privacy": "0",
                "category": "English Dept",
                "school": "English Department",
                "owner": "English Department",
                "link": ""
            }
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
    print('English Department events Downloaded!')


def calculate_document_similarity(n_documents=6, days=21):
    """
    Calculate similarity between talks, 
    only calculate for recent one
    """
    import numpy as np
    import spacy
    nlp = spacy.load('en_core_web_sm')
    events = read_json('events.json')

    # filter only next 21 days
    date_retrieve = datetime.today() + timedelta(days=days)
    events = list(filter(lambda x: dateutil.parser.parse(x['date']) >= datetime.today() and dateutil.parser.parse(x['date']) <= date_retrieve,
                        events))

    # transforming description to spacy tokens 
    docs = []
    for event in events:
        description = '{} {}'.format(event.get('title', ''), event.get('description'))
        docs.append(nlp(description))
    
    # dates
    dates = [dateutil.parser.parse(event['date']) for event in events]

    similar_events = {}
    for i, event in enumerate(events):
        document_similarities = np.array([docs[i].similarity(doc) for doc in docs])

        # looking for future documents only
        date_filter = np.array([d >= dates[i] for d in dates])
        document_similarities[np.logical_not(date_filter)] = 0
        
        similar_events_idx = np.argsort(document_similarities)[::-1][1: n_documents + 1]
        top_similar_events = [events[idx] for idx in similar_events_idx]    
        similar_events[event['event_id']] = top_similar_events
    
    json.dump(similar_events, open(PATH_SIMILAR_EVENTS, 'w'))


if __name__ == '__main__':
    fetch_events()
    fetch_events_cni()
    fetch_events_english_dept()
    calculate_document_similarity()