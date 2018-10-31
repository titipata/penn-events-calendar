#!/usr/bin/python
import os
import re
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
            starttimes.append(event_time.find('span[@class="date-display-start"]').text)
            endtimes.append(event_time.find('span[@class="date-display-end"]').text)
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
                "date": dateutil.parser.parse(re.sub('to \d+', '', date)).strftime("%Y-%m-%d"),
                "starttime": starttime,
                "endtime": "",
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


def fetch_event_crim(base_url='https://crim.sas.upenn.edu'):
    """
    Fetch events from Department of Criminology (CRIM)
    """
    events = []
    page = requests.get(base_url + '/events')
    soup = BeautifulSoup(page.content)
    tree = soup.find('div', attrs={'class': 'item-list'}).find('ul', attrs={'class': 'unstyled'})
    for a in tree.find_all('a'):
        event_path = a.get('href')
        event_url = base_url + event_path
        event_page = requests.get(event_url)
        soup = BeautifulSoup(event_page.content)
        title = soup.find('div', attrs={'class': 'span-inner-wrapper'}).\
            find('h1', attrs={'class': 'page-header'}).text
        date = soup.find('div', attrs={'class': 'field-date'}).find('span').text
        location = soup.find('div', attrs={'class': 'field-location'})
        location = location.find('p').text or ''
        description = soup.find('div', attrs={'class': 'field-body'}).find('p').text or ''
        events.append({
            'title': title,
            'date': date, 
            'location': location, 
            'description': description, 
            'owner': 'C'
        })
    return events


def fetch_event_mec(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from Middle East Center (MEC) https://www.sas.upenn.edu/mec/events
    """
    events = []
    page = requests.get(base_url + '/mec/events')
    soup = BeautifulSoup(page.content, 'html.parser')
    event_urls = soup.find_all('div', attrs={'class': 'frontpage-calendar-link'})
    for div in event_urls:
        event_url = base_url + div.find('a')['href']
        event_page = requests.get(event_url)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')
        event_details = event_soup.find('div', attrs={'class': 'node-inner'})
        date = event_details.find('div', attrs={'class': 'event_date'}).text
        title = event_details.find('div', attrs={'class': 'event_title'}).text
        try:
            description = (event_details.find('div', attrs={'class': 'event_content'}).text or '').strip()
        except:
            pass
        events.append({
            'title': title, 
            'date': date, 
            'description': description, 
            'owner': 'Middle East Center', 
            'url': event_url
        })
    return events


def fetch_event_biology(base_url='http://www.bio.upenn.edu'):
    """
    Fetch events from Department of Biology http://www.bio.upenn.edu/events/
    """
    events = []
    page = requests.get(base_url + '/events')
    soup = BeautifulSoup(page.content, 'html.parser')

    for a in soup.find('div', attrs={'id': 'content-area'}).find_all('a'):
        event_url = base_url + a['href']
        page = requests.get(event_url)
        event_soup = BeautifulSoup(page.content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'title'}).text or ''
        date = event_soup.find('span', attrs={'class': 'date-display-single'}).text
        location = (event_soup.find('div', attrs={'class': 'field field-type-text field-field-event-location'}).\
            find('div', attrs={'class': 'field-item odd'}).text or '').strip()
        description = event_soup.find('div', attrs={'class': 'node-inner'}).\
            find('div', attrs={'class': 'content'}).find('p').text
        events.append({
            'title': title, 
            'date': date,
            'location': location, 
            'description': description, 
            'owner': 'Department of Biology', 
            'url': event_url
        })
    return events


def fetch_event_economics(base_url='https://economics.sas.upenn.edu'):
    """
    Fetch events from Economics department https://economics.sas.upenn.edu/events
    
    Note that we still have problem with when parsing the description
    """
    events = []
    html_page = requests.get(base_url + '/events')
    soup = BeautifulSoup(html_page.content)
    pagination = soup.find('nav', attrs={'class': 'pager-nav text-center'})
    n_pages = max([int(a['href'][-1]) for a in pagination.find_all('a')])

    # loop through all pages
    for page in range(n_pages + 1):
        all_event_url = 'https://economics.sas.upenn.edu/events?tid=All&page=%s' % str(page)
        page = requests.get(all_event_url)
        all_event_soup = BeautifulSoup(page.content, 'html.parser')
        page_events = all_event_soup.find('ul', attrs={'class': 'list-unstyled row'}).find_all('li')

        for event in page_events:
            title = event.find('h4').text
            event_url = base_url + event.find('a')['href']
            start_time, end_time = event.find_all('time')
            start_time, end_time = start_time.text, end_time.text
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content)
            description = event_soup.find('div', attrs={'class': 'col-sm-8 bs-region bs-region--left'}).text.strip()
            location = event_soup.find('p', attrs={'class': 'address'}).text.strip()
            events.append({
                'title': title,
                'start_time': start_time, 
                'end_time': end_time, 
                'description': description,
                'location': location
            })
    return events


def fetch_event_math(base_url='https://www.math.upenn.edu'):
    """
    Fetch event from Math department
    """
    events = []
    html_page = requests.get(base_url + '/events')

    page_soup = BeautifulSoup(html_page.content)
    pagination = page_soup.find('div', attrs={'class': 'pagination pagination-centered'})

    n_pages = max([int(page.text) for page in pagination.find_all('li') if page.text.isdigit()])

    for page in range(n_pages):
        all_event_url = 'https://www.math.upenn.edu/events/?page=%s' % str(page)
        all_event_page = requests.get(all_event_url)
        all_event_soup = BeautifulSoup(all_event_page.content)

        event_urls = [base_url + header.find('a')['href'] for header in all_event_soup.find_all('h3') 
           if 'events' in header.find('a')['href']]

        for event_url in event_urls:
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content)
            try:
                event_detail_soup = event_soup.find('div', attrs={'class': "pull-right span9"})
                title = event_detail_soup.find('h3', attrs={'class': 'field-og-group-ref'}).find('a').text
                date = event_detail_soup.find('p', attrs={'class': 'field-date'}).text.strip()
                speaker = event_detail_soup.find('h4', attrs={'class': 'field-speaker-name'}).text.strip()
                speaker_affil = event_detail_soup.find('p', attrs={'class': 'field-speaker-affiliation'}).text.strip()
                location = event_detail_soup.find('div', attrs={'class': 'fieldset-wrapper'}).text.strip()
                description_soup = event_detail_soup.find('div', attrs={'class': 'field-body'})
                if description_soup is not None:
                    description = description_soup.text.strip()
                else:
                    description = ''
                events.append({
                    'title': title, 
                    'date': date,
                    'speaker': speaker + ', ' + speaker_affil, 
                    'location': location, 
                    'description': description
                })
            except:
                pass
    return events


if __name__ == '__main__':
    fetch_events()
    fetch_events_cni()
    fetch_events_english_dept()
    fetch_event_crim()
    fetch_event_mec()
    fetch_event_biology()
    fetch_event_economics()
    fetch_event_math()