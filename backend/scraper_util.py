"""Utility functions for scraping data from calendars and schedule webpages"""

import json
import re
from datetime import timedelta, datetime
from itertools import chain
from urllib.request import urlopen

import dateutil.parser
import requests
from bs4 import BeautifulSoup
from ics import Calendar
from unidecode import unidecode


PATTERNS = [
    r'^[a-zA-Z]+, ([a-zA-Z]+ [0-9]{1,2}, [0-9]{4}).*',
    r'^([a-zA-Z]+ [0-9]{1,2}, [0-9]{4}) .*',
    r'^([a-zA-Z]+ [0-9]{1,2}) @.*',
    r'^([a-zA-Z]{3}\.? [0-9]{1,2}, [0-9]{4}) .*',
    r'^([a-zA-Z]{3} [0-9]{1,2} [0-9]{4})[0-9]{1,2}:[0-9]{2}.*',
    r'^[a-zA-Z]{3}, ([0-9\/]{10}) .*',
    r'^[a-zA-Z]+, ([0-9]{1,2} [a-zA-Z]+ [0-9]{4})[— ]-?.*',
    r'^([0-9]{1,2} [a-zA-Z]{3} [0-9]{4}) .*'
]
PATS = [re.compile(pattern) for pattern in PATTERNS]


def clean_date_format(d):
    """
    Clean date in string
    e.g. 'Tuesday, October 30, 2018 - 11:30am', '02/06/2019', '1.3.18'
    to string in 'DD-MM-YYYY' format
    """
    try:
        return dateutil.parser.parse(d).strftime('%d-%m-%Y')
    except:
        d = d.replace('*', '')
        d = d.replace('-', '')
        d = d.replace('\n', ' ')
        d = d.replace('Date TBD', '')
        d = d.replace('EDT', '')
        d = d.replace('Special time:', '')
        d = d.replace('Wu & Chen Auditorium', '')
        d = re.sub(r'(\d+\:\d+\s?(?:AM|PM|am|pm|A.M.|P.M.|a.m.|p.m.))', '', d)
        d = d.replace('-', '').strip()
        if d is not '':
            for pat in PATS:
                if pat.match(d):
                    d = pat.sub(r"\1", d)
                    return dateutil.parser.parse(d).strftime('%d-%m-%Y')
            return dateutil.parser.parse(d).strftime('%d-%m-%Y')
        else:
            return ''


def clean_starttime(r):
    if '-' in r['starttime']:
        starttime = r['starttime'].split('-')[0].strip()
    else:
        starttime = r['starttime']
    return starttime


def clean_endtime(r):
    if '-' in r['starttime']:
        endtime = r['starttime'].split('-')[-1].strip()
    else:
        try:
            endtime = dateutil.parser.parse(
                r['starttime']) + timedelta(hours=1)
            endtime = endtime.strftime("%I:%M %p")
        except:
            endtime = r['endtime']
    return endtime


def find_startend_time(s):
    """
    Find starttime and endtime from a given string
    """
    starttime, endtime = '', ''
    ts = re.findall(r'(\d+\:\d+\s?(?:AM|PM|am|pm|A.M.|P.M.|a.m.|p.m.))', s)
    if len(ts) == 1:
        starttime = ts[0]
        endtime = ''
    elif len(ts) == 2:
        starttime = ts[0]
        endtime = ts[1]
    return starttime, endtime


class NoIndent:
    def __init__(self, o):
        self.o = o


class EventEncoder(json.JSONEncoder):
    """
    Class to save JSON where dictionary is stored per line

    ref: https://stackoverflow.com/questions/58327845/save-dictionary-of-list-and-key-to-json-where-one-dictionary-is-stored-per-lin
    """

    def __init__(self, *args, **kwargs):
        super(EventEncoder, self).__init__(*args, **kwargs)
        self._literal = []

    def default(self, o):
        if isinstance(o, NoIndent):
            i = len(self._literal)
            self._literal.append(json.dumps(o.o))
            return '__%d__' % i
        else:
            return super(EventEncoder, self).default(o)

    def encode(self, o):
        s = super(EventEncoder, self).encode(o)
        for i, literal in enumerate(self._literal):
            s = s.replace('"__%d__"' % i, literal)
        return s


def save_json(events_json, file_path):
    """
    Save a dictionary with key and list inside the key in the following format

    events_json = [
        {'date': '10-10-2019', 'title': 'title1', ...},
        {'date': '11-10-2019', 'title': 'title2', ...},
    ]

    where dictionary is saved per line
    """
    events_json = [NoIndent(d) for d in events_json]
    s = json.dumps(events_json, indent=2, cls=EventEncoder)
    with open(file_path, 'w') as fp:
        fp.write(s)


def stringify_children(node):
    """
    Filters and removes possible Nones in texts and tails
    ref: http://stackoverflow.com/questions/4624062/get-all-text-inside-a-tag-in-lxml
    """
    parts = ([node.text] +
             list(chain(*([c.text, c.tail] for c in node.getchildren()))) +
             [node.tail])
    return ''.join(filter(None, parts))


def parse_pdf_abstract(pdf_url):
    """
    Parse title and abstract for a given pdf_url to scientific paper
    """
    try:
        parsed_article = requests.post(
            config.GROBID_PDF_URL, files={'input': requests.get(pdf_url).content}).text
        pdf_soup = BeautifulSoup(parsed_article, 'lxml')
        title = pdf_soup.find('title')
        title = title.text if title is not None else ''
        description = pdf_soup.find('abstract')
        description = description.get_text().strip() if description is not None else ''
        if description == '':
            description = pdf_soup.find('div')
            description = description.text.strip() if description is not None else ''
        description = ' '.join(description.replace(
            'ABSTRACT', '').split(' ')[0:500])
    except:
        title, description = '', ''
    return title, description


def read_google_ics(ics_url):
    """
    Fetch events directly from Google calendar ICS file
    """
    events = []
    try:
        calendar = Calendar(unidecode(requests.get(ics_url).text))
    except:
        calendar = Calendar(
            unidecode(urlopen(ics_url).read().decode('iso-8859-1')))
    for event in calendar.events:
        if event.begin.year >= datetime.today().year:
            date = event.begin.strftime('%d-%m-%Y')
            starttime = event.begin.strftime("%I:%M %p")
            endtime = event.end.strftime("%I:%M %p")
            description = event.description
            description = BeautifulSoup(description, 'html.parser').get_text(
                '\n') if description is not None else ''
            title = event.name
            events.append({
                'title': title,
                #Speaker set later
                'date': date,
                #Location set later
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                #Owner and URL set later
            })
    return events


def fetch_json_events(base_url, json_url, owner):
    """
    Function to get data from JSON url and transform to the same format we use
    """
    events = []
    event_json = requests.get(json_url.strip()).json()
    for event in list(event_json['events'].values()):
        event = event[0]
        if event.get('ts_start') is not None:
            start_date = datetime.utcfromtimestamp(event['ts_start'])
            starttime = start_date.strftime("%I:%M %p")
        else:
            starttime = ''
        if event.get('ts_end') is not None:
            end_date = datetime.utcfromtimestamp(event['ts_end'])
            endtime = end_date.strftime("%I:%M %p")
        else:
            endtime = ''
        date = start_date.strftime('%d-%m-%Y')
        title = event.get('title', '')
        description = event.get('summary', '')
        description = BeautifulSoup(description, 'html.parser').get_text(
            '\n') if description is not None else ''
        location = event.get('location', '')
        speaker = event.get('custom_professor', '')
        speaker = BeautifulSoup(speaker, 'html.parser').get_text('\n')

        if not any([k in title.lower() for k in ['registration', 'break', 'schedule', ' tbd']]):
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': location,
                'description': description.strip(),
                'starttime': starttime,
                'endtime': endtime,
                'url': base_url,
                'owner': owner
            })
    return events
