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

    events_list = []
    for event in events:
        try:
            event_dict = convert_event_to_dict(event)
            events_list.append(event_dict)
        except:
            pass
    return events_list


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


def fetch_events_cni(base_url='https://cni.upenn.edu/events'):
    """
    Saving Computational Neuroscience Initiative to JSON format
    """
    events_list = []
    page = requests.get(base_url)
    site = html.fromstring(page.text)
    events = site.xpath('//h4/span/a[@href]/@href') # all events
    for event_id in events:
        try:
            event_url = urljoin(base_url, event_id)
            event_page = requests.get(event_url)
            event_site = html.fromstring(event_page.text)
            event_dict = extract_event_details(event_site)
            event_dict['event_id'] = event_id
            event_dict['url'] = event_url
            events_list.append(event_dict)
        except:
            pass
    return events_list


def fetch_events_english_dept(base_url='https://www.english.upenn.edu/events/calendar-export/'):
    """
    Saving English Department events to JSON format
    """
    events_list = []
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
            events_list.append(event_dict)
        except:
            pass
    return events_list


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
                'location': location, 
                'url': event_url
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
                    'description': description, 
                    'url': event_url
                })
            except:
                pass
    return events


def fetch_event_philosophy(base_url='https://philosophy.sas.upenn.edu'):
    """
    Fetch event from Philosophy (Penn Arts & Science) at https://philosophy.sas.upenn.edu
    """
    events = []
    html_page = requests.get(base_url + '/events')
    page_soup = BeautifulSoup(html_page.content)
    events_list = page_soup.find('div', attrs={'class': 'item-list'}).find_all('li')

    if len(events_list) > 0:
        for li in events_list:
            event_url = base_url + li.find('a')['href']
            title = li.find('h3').text.strip()
            date = li.find('p', attrs={'class': 'dateline'}).text
            location = li.find('div', attrs={'class': 'location'}).text

            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content)
            description = event_soup.find('div', attrs={'class': 'field-body'})
            if description is not None:
                description = description.text.strip()
            else:
                description = ''

            events.append({
                'title': title,
                'date': date, 
                'location': location, 
                'description': description, 
                'url': event_url
            })
    return events


def fetch_event_classical_studies(base_url='https://www.classics.upenn.edu'):
    """
    Fetch events from Classical studies
    """
    events = []
    html_page = requests.get(base_url + '/events')
    page_soup = BeautifulSoup(html_page.content)
    events_list = page_soup.find('div', attrs={'class': 'item-list'})

    for event_url in events_list.find_all('a'):
        event_url = base_url + event_url['href']
        event_page = requests.get(event_url)
        event_soup = BeautifulSoup(event_page.content)
        title = event_soup.find('h1', attrs={'class': 'page-header'}).text
        date = event_soup.find('span', attrs={'class': 'date-display-single'}).text
        if event_soup.find('p', attrs={'class': 'MsoNormal'}) is not None:
            location = event_soup.find('p', attrs={'class': 'MsoNormal'}).text
        elif event_soup.find('p').text is not None:
            location = event_soup.find('p').text
        else:
            location = ''
        description = event_soup.find('div', attrs={'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
        if description is not None:
            description = description.text
        else:
            description = ''
        events.append({
            'title': title,
            'date': date, 
            'location': location, 
            'description': description, 
            'url': event_url
        })
    return events


def fetch_event_linguistic(base_url='https://www.ling.upenn.edu'):
    """
    Fetch events from Linguistic Department
    """
    events = []
    html_page = requests.get(base_url + '/events')
    page_soup = BeautifulSoup(html_page.content)
    for event in page_soup.find('div', attrs={'class': 'view-content'}).find_all('li'):
        if event.find('a') is not None:
            event_url = base_url + event.find('a')['href']
            title = event.find('h3').text.strip()
            date = event.find('span', attrs={'class': 'date-display-single'})
            if date is not None:
                date = date.text
            location = event.find('div', attrs={'class': 'where-label'})
            if location is not None:
                location = location.text.replace('Where:', '').strip()
            else:
                location = ''
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content)
            description = event_soup.find('div', attrs={'id': 'content-area'}).find('div', attrs={'class': 'content'}).text.strip()
            date = event_soup.find('span', attrs={'class': 'date-display-single'})
            if date is not None:
                date = date.text.strip()
            else:
                date = ''

            events.append({
                'title': title,
                'date': date, 
                'location': location, 
                'description': description, 
                'url': event_url
            })
    return events


def fetch_event_earth_enviromental_science(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from the first page from the Earth and Environmental Science department

    Note: We might need to scrape other pages later
    """
    html_page = requests.get(base_url + '/earth/events')
    page_soup = BeautifulSoup(html_page.content)

    events = []
    all_events = page_soup.find('div', attrs={'class': 'item-list'}).find_all('li')
    for event in all_events:
        event_url = base_url + event.find('a')['href']
        title = event.find('h3').text.strip()
        presenter = event.find('p', attrs={'presenter'}).text.strip() if event.find('p', attrs={'presenter'}) is not None else ''
        event_type = event.find('h4').text if event.find('h4') is not None else ''
        date = event.find('p', attrs={'class': 'dateline'}).text
        location = event.find('div', attrs={'class': 'location'}).text.strip() if event.find('div', attrs={'class': 'location'}) is not None else ''
        description = ''
        events.append({
            'title': title,
            'date': date,
            'location': location,
            'description': description,
            'presenter': presenter,
            'event_type': event_type,
            'url': event_url
        })
    return events


def fetch_event_arthistory(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from Art History Department
    """
    page = requests.get(base_url + '/arthistory/events')
    page_soup = BeautifulSoup(page.content, 'html.parser')
    range_pages = max([int(n_page.text) for n_page in page_soup.find('div', 
                                                                     attrs={'class': 'pagination pagination-centered'}).find_all('li') if n_page.text.isdigit()])

    events = []
    for n_page in range(1, range_pages):
        page = requests.get((base_url + '/arthistory/events?&page={}').format(n_page))
        page_soup = BeautifulSoup(page.content, 'html.parser')
        all_events = page_soup.find('section', attrs={'class': 'main-content is-sidebar'}).find_all('li')
        for event in all_events:
            event_url = base_url + event.find('a')['href']
            title = event.find('h3').text if event.find('h3') is not None else ''
            event_type = event.find('strong').text if event.find('strong') is not None else ''
            date = event.find('p', attrs={'class': 'dateline'}).text if event.find('p', attrs={'class': 'dateline'}) is not None else ''
            location = event.find('div', attrs={'class': 'location'}).text if event.find('div', attrs={'class': 'location'}) is not None else ''
            event_soup = BeautifulSoup(requests.get(event_url).content, 'html.parser')
            description = event_soup.find('div', attrs={'class': 'field-body'})
            if description is not None:
                description = description.text.strip()
            else:
                description = ''
            events.append({
                'title': title,
                'date': date,
                'location': location,
                'description': description,
                'event_type': event_type,
                'url': event_url
            })
    return events


def fetch_event_sociology(base_url='https://sociology.sas.upenn.edu'):
    """
    Fetch events Sociology department at https://sociology.sas.upenn.edu/events?page=0
    """
    events = []
    html_page = requests.get(base_url + '/events')
    page_soup = BeautifulSoup(html_page.content)

    range_pages = max([int(n_page.text) for n_page in 
                       page_soup.find('div', attrs={'class': 'item-list'}).find_all('li') if n_page.text.isdigit()])

    for n_page in range(range_pages):
        all_events_url = base_url + '/events?page={}'.format(n_page)
        all_events_soup = BeautifulSoup(requests.get(all_events_url).content)
        all_events = all_events_soup.find('div', attrs={'id': 'content'}).find_all('li')
        for event_section in all_events:
            event_url = base_url + event_section.find('a')['href'] if event_section.find('a') is not None else ''
            title = event_section.find('a')
            title = title.text.strip() if title is not None else ''

            date = event_section.find('p', attrs={'class': 'dateline'})
            date = date.text.strip() if date is not None else ''

            location = event_section.find('p', attrs={'class': 'location'})
            location = location.text.strip() if location is not None else ''

            if len(event_url) != 0:
                event_page = BeautifulSoup(requests.get(event_url).content)
                description = event_page.find('div', attrs={'class': 'content'})
                description = description.text.strip() if description is not None else ''
                subtitle = event_page.find('div', attrs={'class': 'field-items'})
                subtitle = subtitle.text.strip() if subtitle is not None else ''
            events.append({
                'title': title,
                'subtitle': subtitle,
                'date': date,
                'location': location,
                'description': description,
                'url': event_url
            })
    return events


def fetch_event_cceb(base_url='https://www.cceb.med.upenn.edu/events'):
    """
    Scrape events from Center for Clinical Epidemiology and Biostatistics (CCEB)
    
    TO DO: attemp to scrape https://events.med.upenn.edu/cceb/#!view/event/event_id/698917 
    still does not work
    """
    html_page = requests.get(base_url + '/events')
    page_soup = BeautifulSoup(html_page.content)
    event_section = page_soup.find('div', attrs={'class': 'region-inner region-content-inner'})

    all_events = event_section.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = event.find('a')['href']
        title = event.find('a').text.strip()
        if 'events.med' in event_url:
            event_soup = BeautifulSoup(requests.get(event_url).content)
        events.append({
            'title': title, 
            'url': event_url
        })
    return events


def fetch_event_CIS(base_url="http://www.cis.upenn.edu/about-cis/events/index.php"):
    """
    Fetch events from CIS department. Scrape this site is a little tricky
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content)
    title, date, description, speaker = '', '', '', ''
    for tr in page_soup.find_all('tr'):
        if tr.find('img') is not None:
            events.append({
                'date': date,
                'title': title,
                'description': description,
                'speaker': speaker,
                'url': base_url
            })
            title, date, description = '', '', ''
        else:
            if tr.find('div', attrs={'class': 'CollapsiblePanelContent'}) is not None:
                description = tr.find('div', attrs={'class': 'CollapsiblePanelContent'}).text.strip()
            if tr.find('div', attrs={'class': 'CollapsiblePanelContent'}) is None:
                event_header = tr.find('td')
                if event_header is not None:
                    date = tr.find('strong').text.strip() if tr.find('strong') is not None else ''
                    title = ' '.join(tr.text.replace(date, '').strip().split())             
    return events


def fetch_event_dsl(base_url='http://dsl.cis.upenn.edu/seminar/'):
    """
    Scrape events from DSL seminar.
    The DSL Seminar is a weekly gathering of the research students and professors in the Distributed Systems Laboratory
    """
    page_soup = BeautifulSoup(requests.get(base_url).content)
    events_list = page_soup.find('table').find_all('tr')
    events = []
    for event in events_list[1::]:
        date = event.find('td', attrs={'class': 'ms-grid5-left'}).text
        speaker = event.find('td', attrs={'class': 'ms-grid5-even'}).text
        description = event.find_all('td', attrs={'class': 'ms-grid5-even'})[-1].text.strip()
        if 'Abstract' in description:
            title = description.split('Abstract')[0].strip()
            description = ' '.join(description.split('Abstract')[1::]).strip()
            description = ' '.join(description.split())
        else:
            title = description
            description = description
        events.append({
            'title': title, 
            'description': description, 
            'date': date, 
            'url': base_url, 
            'speaker': speaker,
        })
    return events


def fetch_event_CURF(base_url='https://www.curf.upenn.edu'):
    """
    Center for Undergrad Research and Fellowship
    """
    page_soup = BeautifulSoup(requests.get(base_url + '/curf-events').content)

    events = []
    event_table = page_soup.find('table', attrs={'class': 'views-table cols-3'})
    all_events = event_table.find_all('tr')
    for event in all_events[1::]:
        title = event.find('div').text
        event_url = base_url + event.find('a')['href']
        date = event.find('span', attrs={'class': 'date-display-single'}).text
        description = event.find('td', attrs={'class': 'eventbody'}).text.strip()
        
        # scrape description directly from ``event_url``
        event_soup = BeautifulSoup(requests.get(event_url).content)
        event_details = event_soup.find('div', attrs={'class': 'eventdetails'})
        if event_details is not None:
            event_description = event_details.find('div', attrs={'class': 'eventdescription'})
            if event_description is not None:
                description = event_description.text.replace('Description:', '').strip()
        
        events.append({
            'title': title, 
            'description': description,
            'url': event_url, 
            'date': date
        })
    return events


def fetch_event_upibi(base_url='http://upibi.org/events/'):
    """
    Fetch events from Institute for Biomedical Informatics, http://upibi.org/events/
    
    TO DO: scrape event's description from URL, fix try and except
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content)
    all_events = page_soup.find_all('div', 
                                    attrs={'class': 'type-tribe_events'})
    events = []
    for event in all_events:
        try:
            title = event.find('h3').text.strip()
            date = event.find('div', attrs={'class': 'tribe-event-schedule-details'}).text.strip()
            location = event.find('div', attrs={'class': 'tribe-events-venue-details'}).text.replace('+ Google Map', '').strip()
            description = event.find('div', attrs={'class': 'tribe-events-list-event-description tribe-events-content description entry-summary'}).text.strip()
            event_url = event.find('a')['href']
            events.append({
                'title': title, 
                'description': description,
                'url': event_url, 
                'date': date, 
                'location': location
            })
        except:
            pass
    return events


def fetch_event_ldi(base_url='https://ldi.upenn.edu'):
    """
    Fetch events from Leonard & Davis Institute, https://ldi.upenn.edu
    
    """

    events = []
    page_soup = BeautifulSoup(requests.get(base_url + '/events').content)

    try:
        pages = page_soup.find('ul', attrs={'class': 'pager'}).find_all('li')
        n_pages = max([int(p.text) for p in pages if p.text.isdigit()])
    except:
        n_pages = 1

    for n_page in range(n_pages):
        event_page_url = base_url + '/events?page={}'.format(n_page) 
        page_soup = BeautifulSoup(requests.get(event_page_url).content)
        all_events = page_soup.find_all('div', attrs={'class': 'views-row'})
        for event in all_events:
            if event.find('span', attrs={'class': 'date-display-single'}) is not None:
                date = event.find('span', attrs={'class': 'date-display-single'}).text.strip()
            elif event.find('span', attrs={'class': 'date-display-start'}) is not None:
                date = event.find('span', attrs={'class': 'date-display-start'}).text.strip()
            location = event.find('div', attrs={'class': 'field-name-field-location'})
            location = location.text.strip() if location is not None else ''
            title = event.find('h2').text.strip() if event.find('h2') is not None else ''
            subtitle = event.find('div', attrs={'class': 'field-name-field-subhead'})
            title = title + ' ({})'.format(subtitle.text.strip()) if subtitle is not None else title

            try:
                event_url = event.find('h2').find('a')['href'] 
                event_url = base_url + event_url
                event_soup = BeautifulSoup(requests.get(event_url).content)
                description = event_soup.find('div', attrs={'class': 'event-body'}).text.strip()
                
                speaker = event_soup.find('div', attrs={'class': 'field-name-field-persons-name'})
                speaker = speaker.text.strip() if speaker is not None else ''
                speaker_affil = event_soup.find('div', attrs={'class': 'field-name-field-title'})
                speaker_affil = speaker_affil.text.strip() if speaker_affil is not None else ''
                speaker = (speaker + ' ' + speaker_affil).strip()
            except:
                description = ''
                speaker = ''

            events.append({
                'title': title, 
                'description': description,
                'date': date,
                'location': location, 
                'speaker': speaker,
                'url': event_url
            })
    return events


if __name__ == '__main__':
    events = []
    events.append(fetch_events())
    events.append(fetch_events_cni())
    events.append(fetch_events_english_dept())
    events.append(fetch_event_crim())
    events.append(fetch_event_mec())
    events.append(fetch_event_biology())
    events.append(fetch_event_economics())
    events.append(fetch_event_math())
    events.append(fetch_event_philosophy())
    events.append(fetch_event_linguistic())
    events.append(fetch_event_earth_enviromental_science())
    events.append(fetch_event_arthistory())
    events.append(fetch_event_sociology())