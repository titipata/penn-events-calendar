import os
import sys
import json
import re
from datetime import timedelta, datetime
from urllib.parse import urljoin
import dateutil.parser
import requests
from bs4 import BeautifulSoup, NavigableString
from dateutil import relativedelta

sys.path.append(os.path.join('..', '..'))
from scraper_util import parse_pdf_abstract, find_startend_time, read_google_ics, fetch_json_events


def fetch_events_cni(base_url='https://cni.upenn.edu/events'):
    """
    Fetch events from Computational Neuroscience Initiative (CNI)
    """
    page = requests.get(base_url)
    event_page = BeautifulSoup(page.content, 'html.parser')
    all_events = event_page.find_all('ul', attrs={'class': 'unstyled'})[1]

    events = []
    all_events = all_events.find_all('li')
    for event in all_events:
        event_id = event.find('a').attrs.get('href', '')
        event_url = urljoin(base_url, event_id)
        date = event.find('span', attrs={'class': 'date-display-single'})
        if date is not None:
            date, event_time = date.attrs.get('content').split('T')
            if '-' in event_time:
                starttime = event_time.split('-')[0]
                starttime = dateutil.parser.parse(starttime)
                endtime = (starttime + timedelta(hours=1))
                starttime, endtime = starttime.strftime(
                    "%I:%M %p"), endtime.strftime("%I:%M %p")
            else:
                starttime, endtime = '', ''
        else:
            date, starttime, endtime = '', '', ''

        location = event.find('div', attrs={'class': 'location'})
        location = location.get_text().strip() if location is not None else ''
        title = event.find('a')
        title = title.text if title is not None else ''
        speaker = event.find('a')
        speaker = speaker.text.split(':')[-1] if ':' in speaker.text else ''

        try:
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content, 'html.parser')
            description = []
            description_soup = event_soup.find_all(
                'div', attrs={'class': 'field-item even'})
            for div in description_soup:
                if div.find('strong') is None:
                    description.append(div.text)
                else:
                    description.append('\n'.join([d.text for d in div.find_all(
                        'strong')] + [p.text for p in div.find_all('p')]))
            description = ' '.join(description)
        except:
            description = ''

        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Computational Neuroscience Initiative (CNI)'
        })
    return events


def fetch_events_english_dept(base_url='https://www.english.upenn.edu/events/calendar-export/'):
    """
    Fetch events from English Department
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    event_content = page_soup.find_all('div', attrs={'class': 'view-content'})
    if len(event_content) >= 2:
        event_content = event_content[1]
        events_li = event_content.find_all('li', attrs={'class': 'row-fluid'})
        for event_li in events_li:
            try:
                title = event_li.find(
                    'div', attrs={'class': 'views-field views-field-views-conditional'})
                title = title.find(
                    'span', attrs={'class': 'field-content'}) or '' if title is not None else ''
                event_url = title.find('a')['href']
                event_url = urljoin('https://www.english.upenn.edu', event_url)
                title = title.text.strip() if title is not None else ''
                date = event_li.find('div', attrs={'month-date'})
                date = dateutil.parser.parse(
                    date.find('span').attrs['content'].split('T')[0])
                date = date.strftime("%Y-%m-%d")
                event_time = event_li.find('div', attrs={'class': 'date-time'})
                starttime = event_time.find(
                    'span', attrs={'class': 'date-display-start'})
                starttime = starttime.text.strip() if starttime is not None else ''
                endtime = event_time.find(
                    'span', attrs={'class': 'date-display-end'})
                endtime = endtime.text.strip() if endtime is not None else ''
                location = event_li.find('p', attrs={'class': 'location'})
                location = location.text.strip() if location is not None else ''

                event_soup = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                description = event_soup.find(
                    'div', attrs={'class': 'views-field views-field-nothing'})
                description = description.text.strip() if description is not None else ''

                events.append({
                    'title': title,
                    'speaker': '',
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': "English Department",
                })
            except:
                pass
    return events


def fetch_events_crim(base_url='https://crim.sas.upenn.edu'):
    """
    Fetch events from Department of Criminology (CRIM)
    """
    events = []
    page = requests.get(urljoin(base_url, '/events'))
    soup = BeautifulSoup(page.content, 'html.parser')
    events_soup = soup.find(
        'div', attrs={'class': 'item-list'}).find('ul', attrs={'class': 'unstyled'})
    if events_soup is not None:
        for a in events_soup.find_all('a'):
            event_path = a.get('href')
            event_url = urljoin(base_url, event_path)
            event_page = requests.get(event_url)
            soup = BeautifulSoup(event_page.content, 'html.parser')
            title = soup.find('div', attrs={'class': 'span-inner-wrapper'}).\
                find('h1', attrs={'class': 'page-header'}).text
            date = soup.find(
                'div', attrs={'class': 'field-date'}).find('span').text
            location = soup.find('div', attrs={'class': 'field-location'})
            location = location.text.replace('\xa0\n', ', ').strip() if location is not None else ''
            description = soup.find('div', attrs={'class': 'field-body'})
            description = description.find(
                'p').text if description is not None else ''
            try:
                dt = dateutil.parser.parse(date)
                starttime = dt.strftime('%I:%M %p')
                endtime = (dt + timedelta(hours=1)).strftime('%I:%M %p')
            except:
                starttime = ''
                endtime = ''
            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Dapartment of Criminology',
            })
    return events


def fetch_events_mec(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from Middle East Center (MEC) https://www.sas.upenn.edu/mec/events
    """
    events = []
    page = requests.get(urljoin(base_url, '/mec/events'))
    soup = BeautifulSoup(page.content, 'html.parser')
    event_urls = soup.find_all(
        'div', attrs={'class': 'frontpage-calendar-link'})
    for div in event_urls:
        event_url = urljoin(base_url, div.find('a')['href'])
        event_page = requests.get(event_url)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')
        event_details = event_soup.find('div', attrs={'class': 'node-inner'})
        date = event_details.find('div', attrs={'class': 'event_date'}).text
        title = event_details.find('div', attrs={'class': 'event_title'}).text
        try:
            description = (event_details.find(
                'div', attrs={'class': 'event_content'}).text or '').strip()
        except:
            pass
        try:
            dt = dateutil.parser.parse(date)
            starttime = dt.strftime('%I:%M %p')
            endtime = endtime = (dt + timedelta(hours=1)).strftime('%I:%M %p')
        except:
            starttime = ''
            endtime = ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Middle East Center',

        })
    return events


def fetch_events_biology(base_url='http://www.bio.upenn.edu'):
    """
    Fetch events from Department of Biology http://www.bio.upenn.edu/events/
    """
    events = []
    page = requests.get(urljoin(base_url, '/events'))
    soup = BeautifulSoup(page.content, 'html.parser')

    for event in soup.find_all('div', attrs={'class': 'events-listing'}):
        event_url = urljoin(base_url, event.find('a')['href'])
        title = event.find('a')
        title = title.text if title is not None else ''
        event_time = event.find('span', attrs={'class': 'news-date'})
        event_time = event_time.text if event_time is not None else ''
        starttime, endtime = find_startend_time(event_time)

        event_soup = BeautifulSoup(requests.get(event_url).content, 'html.parser')
        date = event_soup.find('span', attrs={'class': 'date-display-single'})
        date = date.text if date is not None else ''
        location = event_soup.find(
            'div', attrs={'class': 'field field-type-text field-field-event-location'})
        location = location.find(
            'div', attrs={'class': 'field-item odd'}).text if location is not None else ''
        description = event_soup.find('div', attrs={'class': 'events-page'})
        description = description.get_text().strip() if description is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Department of Biology'
        })
    return events


def fetch_events_economics(base_url='https://economics.sas.upenn.edu'):
    """
    Fetch events from Economics department https://economics.sas.upenn.edu/events

    Note that we still have problem with when parsing the description
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    soup = BeautifulSoup(html_page.content, 'html.parser')
    pagination = soup.find('nav', attrs={'class': 'pager-nav text-center'})
    n_pages = max([int(a['href'][-1]) for a in pagination.find_all('a')])

    # loop through all pages
    for page in range(n_pages + 1):
        all_event_url = 'https://economics.sas.upenn.edu/events?tid=All&page={}'.format(
            page)
        page = requests.get(all_event_url)
        all_event_soup = BeautifulSoup(page.content, 'html.parser')
        page_events = all_event_soup.find(
            'ul', attrs={'class': 'list-unstyled row'}).find_all('li')

        for event in page_events:
            event_url = urljoin(base_url, event.find('a')['href'])
            speaker = event.find('h3', attrs={'class': 'event-speaker'})
            speaker = speaker.get_text().strip() if speaker is not None else ''
            affiliation = event.find('h5')
            affiliation = affiliation.get_text().strip() if affiliation is not None else ''
            speaker = '{}, {}'.format(speaker, affiliation)
            try:
                start_time, end_time = event.find_all('time')
                start_time = start_time.text.strip() if start_time is not None else ''
                date, starttime = start_time.split(
                    ' - ')[0], start_time.split(' - ')[-1]
                end_time = end_time.text.strip() if end_time is not None else ''
                endtime = end_time.split(' - ')[-1]
            except:
                starttime, endtime = '', ''
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content, 'html.parser')
            title = event_soup.find('h1', attrs={'class': 'page-header'})
            title = title.text.strip() if title is not None else ''

            try:
                pdf_path = event_soup.find(
                    'a', attrs={'class': 'btn btn-lg btn-primary btn-download'})['href']
                pdf_url = urljoin('https://economics.sas.upenn.edu/', pdf_path)
                _, description = parse_pdf_abstract(pdf_url)
                description = ' '.join(description.split(' ')[0:500])
            except:
                description = ''

            location = event_soup.find(
                'p', attrs={'class': 'address'}).text.strip()
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Department of Economics'
            })
    return events


def fetch_events_math(base_url='https://www.math.upenn.edu'):
    """
    Fetch event from Department of Mathematics
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    pagination = page_soup.find(
        'div', attrs={'class': 'pagination pagination-centered'})

    n_pages = max([int(page.text)
                   for page in pagination.find_all('li') if page.text.isdigit()])

    for page in range(n_pages):
        all_event_url = 'https://www.math.upenn.edu/events/?page={}'.format(
            page)
        all_event_page = requests.get(all_event_url)
        all_event_soup = BeautifulSoup(all_event_page.content, 'html.parser')
        all_events = all_event_soup.find('div', attrs={'class': 'item-list'})

        for event in all_events.find_all('li'):
            title_ = event.find('h3')
            title = title_.text.strip() if title_ is not None else ''
            date = event.find('p', attrs={'class': 'dateline'})
            starttime, endtime = find_startend_time(date.get_text())
            date = date.text.strip() if date is not None else ''
            location = event.find_all('div')[-1].get_text()

            if title_.find('a')['href'] is not None:
                event_url = urljoin(base_url, title_.find('a')['href'])
            else:
                event_url = base_url
            if event_url is not base_url:
                event_page = requests.get(event_url)
                event_soup = BeautifulSoup(event_page.content, 'html.parser')
                speaker = event_soup.find(
                    'h4', attrs={'class': 'field-speaker-name'})
                speaker = speaker.text.strip() if speaker is not None else ''
                affil = event_soup.find(
                    'p', attrs={'class': 'field-speaker-affiliation'})
                affil = affil.text.strip() if affil is not None else ''
                speaker = '{}, {}'.format(speaker, affil)
                description = event_soup.find(
                    'div', attrs={'class': 'field-body'})
                description = description.get_text().strip() if description is not None else ''

            if not any([k == title for k in ['TBA', 'TBD']]):
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': 'Department of Mathematics (Math)',

                })
    return events


def fetch_events_philosophy(base_url='https://philosophy.sas.upenn.edu'):
    """
    Fetch event from Philosophy (Penn Arts & Science) at https://philosophy.sas.upenn.edu
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    events_list = page_soup.find(
        'div', attrs={'class': 'item-list'}).find_all('li')

    if len(events_list) > 0:
        for li in events_list:
            event_url = urljoin(base_url, li.find('a')['href'])
            title = li.find('h3').text.strip()
            date = li.find('p', attrs={'class': 'dateline'})
            date = date.text.strip() if date is not None else ''
            location = li.find('div', attrs={'class': 'location'})
            location = location.text.strip() if location is not None else ''

            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content, 'html.parser')
            event_time = event_soup.find('div', attrs={'class': 'field-date'})
            event_time = event_time.text.strip() if event_time is not None else ''
            starttime, endtime = find_startend_time(event_time)
            description = event_soup.find('div', attrs={'class': 'field-body'})
            description = description.get_text().strip() if description is not None else ''

            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Department of Philosophy'
            })
    return events


def fetch_events_classical_studies(base_url='https://www.classics.upenn.edu'):
    """
    Fetch events from Classical studies
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    events_list = page_soup.find('div', attrs={'class': 'item-list'})

    for event in events_list.find_all('li'):
        title = event.find('h3')
        event_url = title.find('a')['href']
        event_url = urljoin(base_url, event_url)
        title = title.text.strip() if title is not None else ''
        date = event.find('span', attrs={'class': 'date-display-single'})
        date = date.get_text() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        location = event.find('span', attrs={'class': 'event-location'})
        location = location.text.strip() if location is not None else ''

        event_page = requests.get(event_url)
        event_soup = BeautifulSoup(event_page.content, 'html.parser')
        if event_soup is not None:
            description = event_soup.find('div', attrs={
                                          'class': 'field-type-text-with-summary'})
            description = description.get_text().strip() if description is not None else ''
            start_time = event_soup.find(
                'span', attrs={'class': 'date-display-start'})
            end_time = event_soup.find(
                'span', attrs={'class': 'date-display-end'})

            if start_time is not None and end_time is not None:
                starttime, endtime = start_time.text.strip(), end_time.text.strip()
                starttime = starttime.split(' - ')[-1]
                endtime = endtime.split(' - ')[-1]

            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Department of Classical Studies'
            })
    return events


def fetch_events_linguistic(base_url='https://www.ling.upenn.edu'):
    """
    Fetch events from Linguistic Department
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')

    event_pane = page_soup.find('div', attrs={'class': 'view-content'})
    all_events = event_pane.find_all('div', attrs={'class': 'events-listing'})

    for event in all_events:
        title = event.find('h3', attrs={'class': 'events-title'})
        if title is not None:
            event_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            event_url = urljoin(base_url, event_url)
            title = title.text.strip() if title is not None else ''

        date_time = event.find('span', attrs={'class': 'news-date'})
        starttime, endtime = find_startend_time(date_time.text)
        date = date_time.text.replace('When:', '').strip().split('\n')[0]

        location = event.find('span', attrs={'class': 'metainfo'}).find('p')
        location = location.text.replace(
            'Where:', '').strip() if location is not None else ''

        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        description = event_soup.find('div', attrs={'class': 'body'})
        description = description.get_text() if description is not None else ''

        events.append({
            'title': ''.join(title.split(': ')[:-1]) if ': ' in title else title,
            'speaker': title.split(': ')[-1] if ': ' in title else '',
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Department of Linguistics'
        })
    return events


def fetch_events_earth_enviromental_science(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from the first page from the Earth and Environmental Science department

    Note: We might need to scrape other pages later
    """
    html_page = requests.get(urljoin(base_url, '/earth/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')

    events = []
    all_events = page_soup.find(
        'div', attrs={'class': 'item-list'}).find_all('li')
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        title = event.find('h3').text.strip()
        presenter = event.find('p', attrs={'presenter'}).text.strip(
        ) if event.find('p', attrs={'presenter'}) is not None else ''
        # event_type = event.find('h4').text if event.find('h4') is not None else ''
        location = event.find('div', attrs={'class': 'location'}).text.strip(
        ) if event.find('div', attrs={'class': 'location'}) is not None else ''
        description = ''
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        date = event_soup.find('span', attrs={'class': 'date-display-single'})
        date = date.text if date is not None else ''
        starttime, endtime = find_startend_time(date)
        events.append({
            'title': title,
            'speaker': presenter,
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Earth and Environmental Science'
        })
    return events


def fetch_events_art_history(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from Art History Department
    """
    page = requests.get(urljoin(base_url, '/arthistory/events'))
    page_soup = BeautifulSoup(page.content, 'html.parser')
    range_pages = max([int(n_page.text) for n_page in page_soup.find('div',
                                                                     attrs={'class': 'pagination pagination-centered'}).find_all('li') if n_page.text.isdigit()])
    events = []
    for n_page in range(1, range_pages):
        page = requests.get(
            (urljoin(base_url, '/arthistory/events?&page={}')).format(n_page))
        page_soup = BeautifulSoup(page.content, 'html.parser')
        all_events = page_soup.find(
            'div', attrs={'class': 'item-list'}).find_all('li')
        for event in all_events:
            event_url = urljoin(base_url, event.find('a')['href'])
            title = event.find('h3').text if event.find(
                'h3') is not None else ''
            # event_type = event.find('strong').text if event.find('strong') is not None else ''
            date = event.find('span', attrs={'class': 'date-display-single'})
            if date is not None:
                date, event_time = date.attrs.get('content').split('T')
                if '-' in event_time:
                    starttime, endtime = event_time.split('-')
                    try:
                        starttime, endtime = dateutil.parser.parse(starttime).strftime(
                            "%I:%M %p"), dateutil.parser.parse(endtime).strftime("%I:%M %p")
                    except:
                        pass
                else:
                    starttime, endtime = event_time, ''
            else:
                date, starttime, endtime = '', '', ''
            location = event.find('div', attrs={'class': 'location'})
            location = location.text.strip() if location is not None else ''
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            description = event_soup.find('div', attrs={'class': 'field-body'})
            description = description.text.strip() if description is not None else ''
            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Art History'
            })
    return events


def fetch_events_sociology(base_url='https://sociology.sas.upenn.edu'):
    """
    Fetch events Sociology department at https://sociology.sas.upenn.edu/events?page=0
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')

    pagination = page_soup.find('ul', attrs={'class': 'pagination'})
    if pagination is not None:
        range_pages = [l.text.replace('Page', '').replace('Current page', '').strip()
                       for l in pagination.find_all('li')]
        range_pages = max([int(n_page) for n_page in
                           range_pages if n_page.isdigit()])
    else:
        range_pages = 1

    for n_page in range(range_pages):
        all_events_url = urljoin(base_url, '/events?page={}'.format(n_page))
        all_events_soup = BeautifulSoup(requests.get(
            all_events_url).content, 'html.parser')
        all_events = all_events_soup.find_all(
            'div', attrs={'class': 'events-listing'})
        for event_section in all_events:
            event_url = urljoin(base_url, event_section.find(
                'a')['href']) if event_section.find('a') is not None else ''
            title = event_section.find('h3', attrs={'class': 'events-title'})
            event_url = urljoin(base_url, title.find('a')['href'] or '')
            title = title.text.strip() if title is not None else ''

            date = event_section.find('span', attrs={'class': 'news-date'})
            date = date.text.strip().replace('\nat', '') if date is not None else ''
            starttime, endtime = find_startend_time(date)
            if date is not '':
                date = date.split('\n')[0]

            if event_url is not base_url:
                event_page = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                location = event_page.find('span', attrs={'class': 'metainfo'})
                if len(location.find_all('span')) >= 2:
                    location = location.find_all('span')[-1]
                    location = location.text.replace(
                        '|', '').strip() if location is not None else ''
                else:
                    location = ''

                description = event_page.find_all(
                    'div', attrs={'class': 'body'})
                if len(description) >= 2:
                    description = description[1].get_text()
                else:
                    description = ''
            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Department of Sociology (Sociology)'
            })
    return events


def fetch_events_cceb(base_url='https://www.cceb.med.upenn.edu/events'):
    """
    Scrape events from Center for Clinical Epidemiology and Biostatistics (CCEB)
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    event_section = page_soup.find(
        'div', attrs={'class': 'region-inner region-content-inner'})

    all_events = event_section.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = event.find('a')['href']
        title = event.find('a').text.strip()
        event_id = event_url.split('/')[-1]

        # skip conferences by filtering event_id
        # seminars' event_id contain only number
        if not re.match(r'^\d{1,9}$', event_id):
            continue

        text = """https://events.med.upenn.edu/live/calendar/view/event/event_id/{}?user_tz=IT&synta
        x=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Fa
        rg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%
        2Farg%3E%3Carg%20id%3D%22hide_repeats%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_groups%22%3Efa
        lse%3C%2Farg%3E%3Carg%20id%3D%22show_tags%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22default_view%22%
        3Eday%3C%2Farg%3E%3Carg%20id%3D%22group%22%3ECenter%20for%20Clinical%20Epidemiology%20and%20Bios
        tatistics%20%28CCEB%29%3C%2Farg%3E%3C%21--start%20excluded%20groups--%3E%3C%21--%20if%20you%20ar
        e%20changing%20the%20excluded%20groups%2C%20they%20should%20also%20be%20changed%20in%20this%20fi
        le%3A%0A%09%2Fpublic_html%2Fpsom-excluded-groups.php--%3E%3Carg%20id%3D%22exclude_group%22%3EAdm
        in%3C%2Farg%3E%3Carg%20id%3D%22exclude_group%22%3ETest%20Import%3C%2Farg%3E%3Carg%20id%3D%22excl
        ude_group%22%3ELiveWhale%3C%2Farg%3E%3Carg%20id%3D%22exclude_group%22%3ETest%20Department%3C%2Fa
        rg%3E%3C%21--end%20excluded%20groups--%3E%3Carg%20id%3D%22webcal_feed_links%22%3Etrue%3C%2Farg%3
        E%3C%2Fwidget%3E""".format(event_id).replace('\n', '').replace(' ', '')
        event_json = requests.get(text).json()
        if len(event_json) != 0:
            date = BeautifulSoup(
                event_json['event']['date'], 'html.parser').text
            date = re.sub(r'((1[0-2]|0?[1-9]):([0-5][0-9])([AaPp][Mm]))',
                          '', date).replace('-', '').replace('EST', '').strip()
            starttime, endtime = BeautifulSoup(
                event_json['event']['date_time'], 'html.parser').text.split('-')
            title = event_json['event']['title']
            location = event_json['event']['location']
            description = BeautifulSoup(
                event_json['event']['description'] or '', 'html.parser').text.strip()
            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Clinical Epidemiology and Biostatistics (CCEB)'
            })
    return events


def fetch_events_dsl(base_url='http://dsl.cis.upenn.edu/seminar/'):
    """
    Scrape events from DSL seminar.
    The DSL Seminar is a weekly gathering of the research students and professors in the Distributed Systems Laboratory
    """
    page_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    events_list = page_soup.find(
        'table', attrs={'class': 'wp-block-table'}).find_all('tr')
    events = []
    for event in events_list[1::]:
        date, speaker, title = event.find_all('td')
        date = date.text.strip() if date is not None else ''
        speaker = speaker.text.strip() if speaker is not None else ''
        title = title.text.strip() if title is not None else ''
        description = title
        if date != '' and speaker != '' and title != '':
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': 'DSL Conference Room',
                'description': description,
                'starttime': '12:00 PM',
                'endtime': '1:00 PM',
                'url': base_url,
                'owner': 'Distributed Systems Laboratory (DSL)'
            })
    return events


def fetch_events_CURF(base_url='https://www.curf.upenn.edu'):
    """
    Center for Undergrad Research and Fellowship
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/curf-events')).content, 'html.parser')

    events = []
    event_table = page_soup.find(
        'table', attrs={'class': 'views-table cols-3'})
    all_events = event_table.find_all('tr')
    for event in all_events[1::]:
        title = event.find('div').text
        event_url = urljoin(base_url, event.find('a')['href'])
        date = event.find('span', attrs={'class': 'date-display-single'})
        date = date.text.strip() if date is not None else ''
        description = event.find(
            'td', attrs={'class': 'eventbody'}).text.strip()

        # scrape description directly from ``event_url``
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        location = event_soup.find(
            'div', attrs={'class': 'eventlocation'})
        location = location.text.strip() if location is not None else ''
        starttime = find_startend_time(date)[0]
        endtime = event_soup.find('span', attrs={'class': 'date-display-end'})
        endtime = endtime.text.strip() if endtime is not None else ''
        event_details = event_soup.find('div', attrs={'class': 'eventdetails'})
        if event_details is not None:
            event_description = event_details.find(
                'div', attrs={'class': 'eventdescription'})
            if event_description is not None:
                description = event_description.text.replace(
                    'Description:', '').strip()

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Center for Undergrad Research and Fellowship (CURF)',
        })
    return events


def fetch_events_upibi(base_url='http://upibi.org/events/list/?tribe_paged=1&tribe_event_display=past'):
    """
    Fetch events from Institute for Biomedical Informatics, http://upibi.org/events/

    TO DO: scrape event's description from URL, fix try and except
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    all_events = page_soup.find_all('div',
                                    attrs={'class': 'type-tribe_events'})
    events = []
    for event in all_events:
        try:
            title = event.find('h3').text.strip()
            date = event.find(
                'div', attrs={'class': 'tribe-event-schedule-details'}).text.strip()
            starttime, endtime = find_startend_time(date)
            location = event.find('div', attrs={
                                  'class': 'tribe-events-venue-details'}).text.replace('+ Google Map', '').strip()
            description = event.find('div', attrs={
                                     'class': 'tribe-events-list-event-description tribe-events-content description entry-summary'}).text.strip()
            event_url = event.find('a')['href']
            events.append({
                'title': title,
                'speaker': '',
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Institute for Biomedical Informatics (UPIBI)'
            })
        except:
            pass
    return events


def fetch_events_ldi(base_url='https://ldi.upenn.edu'):
    """
    Fetch events from Leonard & Davis Institute, https://ldi.upenn.edu
    """
    events = []
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')

    try:
        pages = page_soup.find('ul', attrs={'class': 'pager'}).find_all('li')
        n_pages = max([int(p.text) for p in pages if p.text.isdigit()])
    except:
        n_pages = 1

    for n_page in range(n_pages):
        event_page_url = urljoin(base_url, '/events?page={}'.format(n_page))
        page_soup = BeautifulSoup(requests.get(
            event_page_url).content, 'html.parser')
        all_events = page_soup.find_all('div', attrs={'class': 'views-row'})
        for event in all_events:
            if event.find('span', attrs={'class': 'date-display-single'}) is not None:
                date = event.find(
                    'span', attrs={'class': 'date-display-single'}).text.strip()
            elif event.find('span', attrs={'class': 'date-display-start'}) is not None:
                date = event.find(
                    'span', attrs={'class': 'date-display-start'}).text.strip()
            location = event.find(
                'div', attrs={'class': 'field-name-field-location'})
            location = location.text.strip() if location is not None else ''
            title = event.find('h2').text.strip() if event.find(
                'h2') is not None else ''
            subtitle = event.find(
                'div', attrs={'class': 'field-name-field-subhead'})
            title = title + ' ({})'.format(subtitle.text.strip()
                                           ) if subtitle is not None else title
            starttime = page_soup.find(
                'span', attrs={'class': 'date-display-start'}).text.strip()
            endtime = page_soup.find(
                'span', attrs={'class': 'date-display-end'}).text.strip()
            try:
                event_url = event.find('h2').find('a')['href']
                event_url = urljoin(base_url, event_url)
                event_soup = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                description = event_soup.find(
                    'div', attrs={'class': 'event-body'}).text.strip()

                speaker = event_soup.find(
                    'div', attrs={'class': 'field-name-field-persons-name'})
                speaker = speaker.text.strip() if speaker is not None else ''
                speaker_affil = event_soup.find(
                    'div', attrs={'class': 'field-name-field-title'})
                speaker_affil = speaker_affil.text.strip() if speaker_affil is not None else ''
                speaker = (speaker + ' ' + speaker_affil).strip()
            except:
                description = ''
                speaker = ''

            if title != '' and description != '':
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': 'Leonard & Davis Institute (LDI)',
                })
    return events


def fetch_events_korean_studies(base_url='https://www.sas.upenn.edu'):
    """
    Fetch events from Korean Studies
    """
    events = []
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/koreanstudies/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find('ul', attrs={'class': 'unstyled'})
    all_events = event_table.find_all('li', attrs={'class': 'row-fluid'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'page-header'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('div', attrs={'class': 'field-date'})
        date = date.text.strip() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        description = event_soup.find('div', attrs={'class': 'field-body'})
        description = description.text.strip() if description is not None else ''
        event_speaker = event_soup.find(
            'div', attrs={'class': 'fieldset-wrapper'})
        event_speaker = event_speaker.text.strip() if event_speaker is not None else ''
        events.append({
            'title': title,
            'speaker': event_speaker,
            'date': date,
            'location': '',
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Korean Studies'
        })
    return events


def fetch_events_cscc(base_url='https://cscc.sas.upenn.edu/'):
    """
    Fetch events from Penn Arts & Sciences, Center for the Study of Contemporary China

    TO DO: Fix try, except in for this function
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    all_events = page_soup.find_all('div', attrs={'class': 'events-listing'})

    for div in all_events:
        try:
            title = div.find(
                'h3', attrs={'class': 'events-title'}).text.strip()
            location = div.find('span', attrs={'class': 'news-date'})
            if location is not None and location.find('span') is not None:
                location = location.find('span').text.strip()
            else:
                location = ''
            event_time = div.find('span', attrs={
                                  'class': 'news-date'}).text.replace('\n', ' ').replace(location, '').strip()
            event_date = div.find('div', attrs={'class': 'event-date'})
            event_date = ' '.join(
                [t.text for t in event_date.find_all('time')])
            starttime, endtime = find_startend_time(event_time)
            speaker = div.find_all('h5')[-1].text
            event_url = urljoin(base_url, div.find('a')['href'])
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            description = event_soup.find(
                'div', attrs={'class': 'events-page'}).find('div', attrs={'class': 'body'})
            description = description.text.strip() if description is not None else ''
            events.append({
                'title': title,
                'speaker': speaker,
                'date': event_date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Center for the Study of Contemporary China'
            })
        except:
            pass
    return events


def fetch_events_fels(base_url='https://www.fels.upenn.edu'):
    """
    Fetch events from Fels institute of Government at University of Pennsylvania
    """
    events = []
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')
    all_events = page_soup.find('div', attrs={'class': 'view-content'})
    event_urls = [urljoin(base_url, a['href'])
                  for a in all_events.find_all('a') if a is not None]

    for event_url in event_urls:
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'id': 'page-title'}).text.strip()
        description = event_soup.find(
            'div', attrs={'class': 'field-name-body'})
        description = description.text.strip() if description is not None else ''
        description = description.replace('Event Information: ', '')
        location = event_soup.find(
            'div', attrs={'class': 'field-name-field-event-location'})
        location = location.text.replace(
            "Location Address:", '').strip() if location is not None else ''
        room = event_soup.find(
            'div', attrs={'class': 'field-name-field-event-location-name'})
        room = room.text.replace(
            'Location Name:', '').strip() if room is not None else ''
        date = event_soup.find(
            'span', attrs={'class': 'date-display-single'}).text.strip()
        starttime, endtime = find_startend_time(date)
        location = (location + ' ' + room).strip()
        speaker = event_soup.find('div', attrs={'class': 'breadcrumb-top'})
        speaker = speaker.text.replace(
            'Home\xa0 // \xa0', '').strip() if speaker is not None else ''
        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': (location + ' ' + room).strip(),
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Fels institute'
        })
    return events


def fetch_events_sciencehistory(base_url='https://www.sciencehistory.org'):
    """
    Fetch events from Science History Institute, https://www.sciencehistory.org/events
    """
    events = []
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')

    all_events = page_soup.find('div', attrs={'class': 'eventpageleft'})
    all_events = all_events.find_all('div', attrs={'class': 'views-row'})

    for event in all_events:
        title = event.find('div', attrs={'class': 'eventtitle'}).text.strip()
        date = event.find('div', attrs={'class': 'eventdate'}).text.strip()
        event_url = urljoin(base_url, event.find(
            'div', attrs={'class': 'eventtitle'}).find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        location = event_soup.find('div', attrs={'class': 'event-location'})
        location = ', '.join(
            [div.text.strip() for div in location.find_all('div') if div is not None])
        event_time = event_soup.find('div', attrs={'class': 'event-time'})
        event_time = event_time.text.strip() if event_time is not None else ''
        starttime, endtime = find_startend_time(event_time)

        descriptions = event_soup.find(
            'div', attrs={'class': 'content event_padding'})
        descriptions = descriptions.find_all('p')
        if len(descriptions) >= 5:
            descriptions = ' '.join([p.text.strip()
                                     for p in descriptions[0:5] if p is not None])
        else:
            descriptions = ' '.join([p.text.strip()
                                     for p in descriptions if p is not None])

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': descriptions,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Science History Institute'
        })
    return events


def fetch_events_HIP(base_url='https://www.impact.upenn.edu/'):
    """
    Penn Events for Center for High Impact Philanthropy
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, 'events/')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'class': 'entry-content'})
    all_events = event_table.find_all('article')
    for event in all_events:
        event_url = event.find(
            'h2', attrs={'class': 'entry-title'}).find('a')['href']
        date = [p.text for p in event.find_all('p') if '| Event' in p.text][0]
        date = date.replace('| Event', '')

        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'entry-title'})
        title = title.text.strip() if title is not None else ''

        description = event_soup.find(
            'div', attrs={'class': 'entry-content clearfix'})
        event_time = str(description.find('p')).split(
            '<br/>')[-1].replace('</p>', '') if description is not None else ''
        starttime, endtime = find_startend_time(event_time)

        if description is not None:
            description = ' '.join([i.text.strip() for i in description.find(
                'h3').next_siblings if not isinstance(i, NavigableString)])
        else:
            description = ''

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': "Center for High Impact Philanthropy"
        })
    return events


def fetch_events_italian_studies(base_url='https://www.sas.upenn.edu'):
    """
    Penn Events for Italian Studies
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/italians/center/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'class': 'view-content'})
    all_events = event_table.find_all('div', attrs={'class': 'field-content'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'title'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find(
            'span', attrs={'class': 'date-display-single'}).text.strip()

        starttime = event_soup.find(
            'div', attrs={'class': 'field field-type-datetime field-field-event-time'})
        starttime = starttime.text.replace(
            'Time:', '').strip() if starttime is not None else ''
        if starttime is '':
            starttime = event_soup.find(
                'span', attrs={'class': 'date-display-start'}).text.strip()
            endtime = event_soup.find(
                'span', attrs={'class': 'date-display-end'})
            endtime = endtime.text.strip() if endtime is not None else ''
        else:
            starttime, endtime = find_startend_time(starttime)

        page_details = [t.text.strip() for t in event_soup.find_all(
            'div', attrs={'class': 'field-items'})]
        location, speaker = '', ''
        for detail in page_details:
            if 'Speaker' in detail:
                speaker = detail.replace('Speaker:', '').strip()
            if 'Location' in detail:
                location = detail.replace('Location:', '').strip()

        description = event_soup.find(
            'div', attrs={'id': 'content-area'}).find('div', attrs={'class': 'content'})
        description = '\n'.join([t.text for t in description.find_all(
            'p')]) if description is not None else ''
        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Italian Studies'
        })
    return events


def fetch_events_CEMB(base_url='https://cemb.upenn.edu'):
    """
    Penn Events for Center for Engineering MechanoBiology
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/items/calendar/')).content, 'html.parser')

    events = []
    event_table = page_soup.find(
        'div', attrs={'class': 'gumm-layout-element event-layout-element span5'})
    all_events = event_table.find_all('div', attrs={'class': 'event-details'})
    for event in all_events:
        event_url = event.find('a')['href']
        date = event.find('li', attrs={'class': 'event-meta-date'})
        date = date.text.strip() if date is not None else ''
        location = event.find('li', attrs={'class': 'event-meta-location'})
        location = location.text.strip() if location is not None else ''

        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1')
        title = title.text.strip() if title is not None else ''
        details = event_soup.find('div', attrs={'class': 'event-details'})
        details = details.text.strip() if details is not None else ''

        starttime, endtime = '', ''
        try:
            ts = date.split('•')[-1].strip()
            ts = ts.split('–')
            if len(ts) == 1:
                starttime, endtime = ts[0], ''
            elif len(ts) == 2:
                starttime, endtime = ts[0], ts[1]
            else:
                starttime, endtime = '', ''
        except:
            pass
        starttime, endtime = starttime.strip(), endtime.strip()

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Center for Engineering MechanoBiology'
        })
    return events


def fetch_events_CEAS(base_url='https://ceas.sas.upenn.edu'):
    """
    Penn Events for Center for East Asian Studies
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')

    events = []
    all_events = page_soup.find_all('li', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'page-header'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find(
            'span', attrs={'class': 'date-display-single'})
        date = date.text.strip() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        details = event_soup.find('div', attrs={
                                  'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
        details = details.text if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Center for East Asian Studies'
        })
    return events


def fetch_events_CASI(base_url='https://casi.ssc.upenn.edu'):
    """
    Penn Events for Center for the Advanced Study of India
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find(
        'div', attrs={'class': 'view-events'})
    all_events = event_table.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        title = event.find('span', attrs={'class': 'field-content'})
        title = title.text.strip() if title is not None else ''
        speaker = event.find('div', attrs={
                                  'class': 'views-field-field-speaker-full-name'})
        speaker = speaker.text.strip() if speaker is not None else ''
        date_time = event.find('span', attrs={'class': 'date-display-single'})
        date = date_time.text.strip() if date_time is not None else ''
        starttime = date.split('-')[-1].strip()
        try:
            s = int(starttime.split(':')[0])
            if s <= 6 or s >= 12:
                starttime = starttime + ' PM'
            else:
                starttime = starttime + ' AM'
        except:
            pass

        endtime = ''
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        details = event_soup.find('div', attrs={
                                  'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
        details = details.get_text().strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': '',
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Center for the Advanced Study of India'
        })
    return events


def fetch_events_african_studies(base_url='https://africana.sas.upenn.edu'):
    """
    Penn Events for African Studies
    site available at https://africana.sas.upenn.edu/center/events
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/center/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'class': 'body-content'})
    all_events = event_table.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'page-header'})
        title = title.text.strip() if title is not None else ''
        speaker = event_soup.find('div', attrs={'class': 'field-speaker'})
        speaker = speaker.text.strip() if speaker is not None else ''
        date = event_soup.find(
            'div', attrs={'class': 'container-date-wrapper'})
        date = date.text.strip() if date is not None else ''
        event_time = event_soup.find(
            'span', attrs={'class': 'date-display-single'})
        event_time = event_time.text.strip() if event_time is not None else ''
        starttime, endtime = find_startend_time(event_time)

        details = event_soup.find('div', attrs={'class': 'field-body'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': '',
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'African Studies'
        })
    return events


def fetch_events_business_ethics(base_url='https://zicklincenter.wharton.upenn.edu'):
    """
    Penn Events for Carol and Lawrence Zicklin Center for Business Ethics Research:
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/upcoming-events/')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'class': 'post-entry'})
    all_events = event_table.find_all(
        'div', attrs={'class': 'eventrocket embedded-event post'})
    for event in all_events:
        event_url = event.find('a')['href']
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'beta'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('p', attrs={'class': 'gamma mobile-date'})
        date = date.text.strip() if date is not None else ''
        event_time = event_soup.find(
            'h3').text if event_soup.find('h3') is not None else ''
        starttime, endtime = find_startend_time(event_time)

        details = event_soup.find(
            'div', attrs={'class': 'tribe-events-content-wrapper'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Zicklincenter Center for Business Ethics'
        })
    return events


def fetch_events_law(base_url='https://www.law.upenn.edu/institutes/legalhistory/workshops-lectures.php'):
    """
    Fetch event from Penn Law School
    """
    events = []
    page_soup = BeautifulSoup(requests.get(base_url).content, 'html.parser')
    all_events = page_soup.find_all('div', attrs={'class': 'lw_events_day'})
    for event in all_events:
        event_id = ''.join([c for c in event.find('a')['href'] if c.isdigit()])
        event_url = '''
        https://www.law.upenn.edu/live/calendar/view/event/event_id/{}?user_tz=IT&syntax=%3Cwidget%20type%3D%22events_calendar%22%20priority%3D%22high%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3ELibrary%20Hours%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3ELibrary%20Event%20Private%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3ECareers%20Calendar%20ONLY%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3EDocs%20Only%20Event%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3EPending%20Event%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3EPrivate%20Event%3C%2Farg%3E%3Carg%20id%3D%22exclude_tag%22%3EOffcampus%3C%2Farg%3E%3Carg%20id%3D%22exclude_group%22%3ERegistrar%3C%2Farg%3E%3Carg%20id%3D%22exclude_group%22%3EAdmitted%20JD%3C%2Farg%3E%3Carg%20id%3D%22placeholder%22%3ESearch%20Calendar%3C%2Farg%3E%3Carg%20id%3D%22disable_timezone%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E144%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E144%3C%2Farg%3E%3Carg%20id%3D%22modular%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22default_view%22%3Eweek%3C%2Farg%3E%3C%2Fwidget%3E
        '''.strip().format(event_id)
        event_detail = requests.get(url=event_url).json()
        event_time = BeautifulSoup(
            event_detail['event']['date_time'], 'html.parser').text
        starttime, endtime = find_startend_time(event_time)
        description = BeautifulSoup(
            event_detail['event'].get('description', ''), 'html.parser')
        description = description.text.strip() if description is not None else ''
        events.append({
            'title': event_detail['event']['title'],
            'speaker': '',
            'date': event_detail['title'],
            'location': event_detail['event']['location'],
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': 'https://www.law.upenn.edu/newsevents/calendar.php#event_id/{}/view/event'.format(event_id),
            'owner': 'Law School'
        })
    return events


def fetch_events_penn_SAS(base_url='https://www.sas.upenn.edu'):
    """
    Penn Events for Penn School of Arts & Science
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events/upcoming-events')
    ).content, 'html.parser')

    events = []
    event_table = page_soup.find(
        'div', attrs={'class': 'field-basic-page-content'})
    all_events = event_table.find_all(
        'div', attrs={'class': 'flex-event-desc'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h3', attrs={'class': 'event-title'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find(
            'div', attrs={'class': 'field-event-start-date'})
        date = date.text.strip() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        location = event_soup.find('div', attrs={'class': 'event-sub-info'})
        location = location.text.strip() if location is not None else ''
        speaker = event_soup.find(
            'div', attrs={'class': 'field-event-speaker'})
        speaker = speaker.text.strip() if speaker is not None else ''
        details = event_soup.find('div', attrs={'class': 'field-event-desc'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': location,
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'School of Arts & Science (SAS)'
        })
    return events


def fetch_events_physics_astronomy(base_url='https://www.physics.upenn.edu'):
    """
    Penn Events Penn Physics and Astronomy Department
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events/')).content, 'html.parser')
    try:
        pagination = page_soup.find('ul', attrs={'class': 'pagination'})
        pagination_max = max([a.attrs.get('href')
                              for a in pagination.find_all('a')])
        pagination_max = int(pagination_max[-1])
    except:
        pagination_max = 1

    events = []
    for pagination in range(0, pagination_max):
        page_soup = BeautifulSoup(requests.get(
            urljoin(base_url, '/events/' + '?page={}'.format(pagination))).content, 'html.parser')
        all_events = page_soup.find_all(
            'div', attrs={'class': 'events-listing'})
        for event in all_events:
            event_url = urljoin(base_url, event.find('a')['href'])
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            title = event_soup.find('h3', attrs={'class': 'events-title'})
            title = title.text.strip() if title is not None else ''
            date = event_soup.find('div', attrs={'class': 'event-date'})
            date = ' '.join([d.text.strip()
                             for d in date.find_all('time') if d is not None])
            try:
                event_time = event_soup.find(
                    'span', attrs={'class': 'news-date'})
                starttime, endtime = event_time.find_all('time')
                starttime, endtime = starttime.text.strip() or '', endtime.text.strip() or ''
            except:
                starttime, endtime = '', ''
            speaker = ' '.join([h5.text.strip() if h5.text is not None else ''
                                for h5 in event.find_all('h5')]).strip()
            description = event_soup.find('p')
            description = description.text.strip() if description is not None else ''
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': '',
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Department of Physics and Astronomy'
            })
    return events



def fetch_events_music_dept(base_url='https://www.sas.upenn.edu'):
    """
    Department of Music... details does not output anything
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/music/performance/performance-calendar')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'class': 'view-content'})
    all_events = event_table.find_all('li', attrs={'class': 'group'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'title'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find(
            'div', attrs={'class': 'field field-type-date field-field-events-date'})
        date = date.text.strip() if date is not None else ''
        details = event_soup.find('div', attrs={'class': 'content'})
        details = '\n'.join([p.text.strip() for p in details.find_all(
            'p')]) if details is not None else ''
        starttime, endtime = find_startend_time(date)
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': details.strip(),
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Department of Music'
        })
    return events


def fetch_events_annenberg(base_url='https://www.asc.upenn.edu'):
    """
    Penn Events for Annenberg School of Communication
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/news-events/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'id': 'content'})
    all_events = event_table.find_all('h3', attrs={'class': 'field-content'})
    for event in all_events:
        try:
            if 'https://www.asc.upenn.edu/news-events/events/' in event.find('a')['href']:
                event_url = event.find('a')['href']
            else:
                event_url = urljoin(base_url, event.find('a')['href'])
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            title = event_soup.find('h1', attrs={'class': 'title'})
            title = title.text.strip() if title is not None else ''
            date = event_soup.find(
                'span', attrs={'class': 'date-display-single'})
            date = date.text.strip() if date is not None else ''
            starttime, endtime = find_startend_time(date)
            location = event_soup.find('div', attrs={
                                       'class': 'field field-name-field-event-location field-type-text field-label-inline clearfix'})
            location = location.text.strip() if location is not None else ''
            location = location.replace('Location:', '').strip()
            details = event_soup.find('div', attrs={
                                      'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
            details = details.text.strip() if details is not None else ''
            speaker = ''
            for kw in ['Talk: ', 'Colloquium:', 'Series:']:
                if kw in title:
                    speaker = title.split(kw)[-1]
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': location,
                'description': details,
                'url': event_url,
                'starttime': starttime,
                'endtime': endtime,
                'owner': 'Annenberg School of Communication'
            })
        except:
            pass
    return events


def fetch_events_religious_studies(base_url='https://www.sas.upenn.edu'):
    """
    Penn Events for Department of Religious Studies
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/religious_studies/news')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'id': 'content-area'})
    all_events = event_table.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'title'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('span', attrs={'class': 'date-display-single'})
        date = date.text.strip() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        location = event_soup.find(
            'div', attrs={'class': 'field field-type-text field-field-event-location'})
        location = location.text.strip() if location is not None else ''
        details = event_soup.find('div', attrs={'class': 'content'})
        details = '\n'.join([d.text for d in details.find_all(
            'p')]) if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Department of Religious Studies'
        })
    return events


def fetch_events_AHEAD(base_url='http://www.ahead-penn.org'):
    """
    Penn Events for Penn AHEAD
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/events')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'id': 'main-content'})
    all_events = event_table.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h1', attrs={'class': 'title'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('span', attrs={'class': 'date-display-single'})
        date = date.text.strip() if date is not None else ''
        starttime, endtime = find_startend_time(date)
        location = event_soup.find('div', attrs={
                                   'class': 'field field-name-field-location field-type-text field-label-hidden'})
        location = location.text.strip() if location is not None else ''
        details = event_soup.find('div', attrs={
                                  'class': 'field field-name-body field-type-text-with-summary field-label-hidden'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Penn AHEAD',
        })
    return events


def fetch_events_SPP(base_url='https://www.sp2.upenn.edu'):
    """
    Penn Events for Penn Social Policy & Practice
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/sp2-events/list/')).content, 'html.parser')

    events = []
    event_table = page_soup.find('div', attrs={'id': 'tribe-events-content'})
    all_events = event_table.find_all(
        'h2', attrs={'class': 'tribe-events-list-event-title entry-title summary'})
    for event in all_events:
        event_url = event.find('a')['href']
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('div', attrs={'class': 'events-header'})
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('h3', attrs={'class': 'date-details-top'})
        date = date.text.strip() if date is not None else ''
        time = event_soup.find('p', attrs={'class': 'event-time-detail'})
        time = time.text.strip() if time is not None else ''
        starttime, endtime = find_startend_time(time)

        details = event_soup.find('div', attrs={
                                  'class': 'tribe-events-single-event-description tribe-events-content entry-content description'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': details,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Social Policy & Practice'
        })
    return events


def fetch_events_ortner_center(base_url='http://ortnercenter.org'):
    """
    Penn Events for Ortner Center for Violence and Abuse in Relationships,
    ref: http://ortnercenter.org/updates?tag=events
    """
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, '/updates?tag=events')).content, 'html.parser')

    events = []
    event_table = page_soup.find(
        'div', attrs={'class': 'block content columnBlog--left'})
    all_events = event_table.find_all('div', attrs={'class': 'blog-title'})
    for event in all_events:
        event_url = urljoin(base_url, event.find('a')['href'])
        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        title = event_soup.find('h6')
        title = title.text.strip() if title is not None else ''
        date = event_soup.find('div', attrs={'class': 'blog-date'})
        date = date.text.strip() if date is not None else ''
        details = event_soup.find('div', attrs={'class': 'apos-content'})
        details = details.text.strip() if details is not None else ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': '',
            'description': details,
            'starttime': '',
            'endtime': '',
            'url': event_url,
            'owner': 'Ortner Center for Violence and Abuse in Relationships'
        })
    return events


def fetch_events_penn_today(base_url='https://penntoday.upenn.edu'):
    """
    Penn Today Events
    """
    events = requests.get(
        'https://penntoday.upenn.edu/events-feed?_format=json').json()
    events_list = []
    for event in events:
        events_list.append({
            # 'event_id': event['id'],
            'title': event['title'],
            'speaker': '',
            'date': event['start'],
            'location': event['location'] if event['location'] is not False else '',
            'description': BeautifulSoup(event['body'], 'html.parser').text.strip(),
            'starttime': event['starttime'],
            'endtime': event['endtime'],
            'url': urljoin(base_url, event['path']),
            'owner': 'Penn Today Events'
        })
    return events_list


def fetch_events_mins(base_url='http://go.activecalendar.com/handlers/query.ashx?tenant=UPennMINS&site=&get=eventlist&page=0&pageSize=-1&total=-1&view=list2.xslt&callback=jQuery19108584306856037709_1568648511516&_=1568648511517'):
    """
    Fetch events from Mahoney Institute for Neuroscience (MINS)
    """
    events = []
    data = requests.get(url=base_url)
    data = json.loads(data.content.decode('ascii').replace(
        'jQuery19108584306856037709_1568648511516(', '')[:-1])
    event_soup = BeautifulSoup(data['html'], 'html.parser')

    dates = []
    event_date_time = [p.text.strip() for p in event_soup.find_all('p')]
    for e in event_date_time:
        date = dateutil.parser.parse(e.split(', ')[0]).strftime('%d-%m-%Y')
        starttime, endtime = e.split(', ')[1].split('-')
        starttime, endtime = ' '.join(
            starttime.split()), ' '.join(endtime.split())
        dates.append([date, starttime, endtime])
    urls = [h4.find('a').attrs['href'] for h4 in event_soup.find_all('h4')]
    titles = [h4.find('a').attrs.get('aria-label', '') if h4.find('a') is not None else ''
              for h4 in event_soup.find_all('h4')]

    events_descriptions, locations = [], []
    for url in urls:
        event_slug = url.strip('/').split('/')[-1]
        event_url = 'http://go.activecalendar.com/handlers/query.ashx?tenant=UPennMINS&site=&get=eventdetails&route={}&view=detail.xslt'.format(
            event_slug)
        event_page = requests.get(url=event_url)
        event_detail_html = json.loads(event_page.content.decode(
            'ascii').strip('(').strip(')'))['html']
        event_soup = BeautifulSoup(event_detail_html, 'html.parser')
        event_description = event_soup.find(
            'div', attrs={'itemprop': 'description'}).text
        location = event_soup.find('span', attrs={'itemprop': 'name'}).get_text() + \
            ', ' + \
            event_soup.find(
                'span', attrs={'itemprop': 'streetAddress'}).get_text()
        events_descriptions.append(event_description)
        locations.append(location)

    for title, date, url, description, location in zip(titles, dates, urls, events_descriptions, locations):
        events.append({
            'title': title,
            'speaker': '',
            'date': date[0],
            'location': location,
            'description': description,
            'starttime': date[1],
            'endtime': date[2],
            'url': url,
            'owner': 'Mahoney Institute for Neuroscience (MINS)'
        })
    return events


def _extract_mindcore_event_detail(event):
    """
    Extract specific event for MindCORE
    """
    title = event.find('h2', attrs={'class': 'event-title'})
    title = title.text.strip() if title is not None else ''
    date = event.find('div', attrs={'class': 'event-meta-item'})
    date = date.get_text() if date is not None else ''
    description = event.find('div', attrs={'class': 'row event-inner-content'})
    description = description.text.strip() if description is not None else ''
    event_time = event.find(
        'div', attrs={'class': 'event-meta-item event-time'})
    event_time = event_time.text.strip() if event_time is not None else ''
    if '-' in event_time:
        starttime, endtime = event_time.split('-')
    else:
        starttime, endtime = event_time, ''
    event_url = event.find('a').attrs.get('href', '')
    speaker = title.split(':')[-1].strip() if ':' in title else ''

    try:
        event_detail_soup = BeautifulSoup(requests.get(event_url).content,
                                          'html.parser')
        location = event_detail_soup.find(
            'div', attrs={'class': 'event-location'})
        location = location.get_text().strip() if location is not None else ''
    except:
        location = ''

    return {
        'title': title,
        'speaker': speaker,
        'date': date,
        'location': location,
        'description': description,
        'starttime': starttime,
        'endtime': endtime,
        'url': event_url,
        'owner': 'MindCORE'
    }


def fetch_events_mindcore(base_url='http://mindcore.sas.upenn.edu/event-category/all-events/'):
    """
    Fetch events from MindCORE
    """
    events = []
    event_page = requests.get(base_url)
    event_soup = BeautifulSoup(event_page.content, 'html.parser')
    try:
        pagination = event_soup.find('ul', attrs={'class': 'pagination'})
        pagination_urls = []
        for li in pagination.find_all('li'):
            if li.find('a') is not None:
                pagination_urls.append(li.find('a').attrs.get('href'))
        pagination_max = max([int(p.split('/')[-2])
                              for p in pagination_urls if p != ''])
    except:
        pagination_max = 1

    if len(event_soup.find_all('article')) != 1:
        all_events = event_soup.find('div', attrs={'class': 'calendarp'})
        all_events = all_events.find_all('article')
        for event in all_events:
            events.append(_extract_mindcore_event_detail(event))

    if pagination_max > 1:
        for i in range(2, pagination_max + 1):
            event_url = 'http://mindcore.sas.upenn.edu/event-category/all-events/page/{}/'.format(
                i)
            event_page = requests.get(event_url)
            event_soup = BeautifulSoup(event_page.content, 'html.parser')
            if len(event_soup.find_all('article')) != 1:
                all_events = event_soup.find(
                    'div', attrs={'class': 'calendarp'})
                all_events = all_events.find_all('article')
                for event in all_events:
                    events.append(_extract_mindcore_event_detail(event))
    return events


def fetch_events_seas(base_url='https://events.seas.upenn.edu/calendar/list/'):
    """
    Fetch events from School Engineering and Applied Science (SEAS)
    """
    events = []
    for i in range(1, 4):
        try:
            event_url = urljoin(
                base_url, '?tribe_paged={}&tribe_event_display=list'.format(i))
            event_page = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            all_events = event_page.find(
                'div', attrs={'class': 'tribe-events-loop'})
            year = event_page.find(
                'h2', attrs={'class': 'tribe-events-list-separator-month'})
            year = year.text.strip() if year is not None else ''
            for event in all_events.find_all('div', attrs={'class': 'type-tribe_events'}):
                event_attrs = event.find(
                    'a', attrs={'class': 'tribe-event-url'}).attrs
                event_url = event_attrs.get('href', '')
                title = event_attrs.get('title', '')
                date = event.find(
                    'span', attrs={'class': 'tribe-event-date-start'})
                date = date.text if date is not None else ''
                starttime = find_startend_time(date)[0]
                date = date.replace(starttime, '').replace(' at ', '')
                endtime = event.find(
                    'span', attrs={'class': 'tribe-event-time'})
                endtime = endtime.text.strip() if endtime is not None else ''
                if ' ' in year:
                    date = date + ' ' + year.split(' ')[-1]
                location = event.find(
                    'div', attrs={'class': 'tribe-events-venue-details'})
                location = ' '.join(location.text.replace(
                    '+ Google Map', '').strip().split('\n')[0:2])
                description = event.find(
                    'div', attrs={'class': 'tribe-events-list-event-description'})
                description = description.text.strip() if description is not None else ''

                # get event description if available
                try:
                    event_soup = BeautifulSoup(requests.get(
                        event_url).content, 'html.parser')
                    description = event_soup.find(
                        'div', attrs={'id': 'z5_events_main_content'})
                    if description is not None:
                        description = description.text.strip()
                        description = '\n'.join(
                            [d.strip() for d in description.split('\n') if d.strip() != ''])
                    speaker = event_soup.find(
                        'div', attrs={'id': 'z5_events_speaker_info'})
                    if speaker is not None:
                        speaker = speaker.text.strip()
                        speaker = '\n'.join(
                            [d.strip() for d in speaker.split('\n') if d.strip() != ''])
                except:
                    speaker = ''

                # set owner
                owner_map = {
                    'BE ': 'Department of Bioengineering (BE)',
                    'MSE ': 'Materials Science and Engineering (MSE)',
                    'CBE ': 'Chemical and Biomolecular Engineering (CBE)',
                    'ESE ': 'Electrical and Systems Engineering (ESE)',
                    'PICS ': 'Penn Institute for Computational Science (PICS)',
                    'PSOC ': 'Physical Sciences Oncology Center (PSOC)',
                    'MEAM ': 'Mechanical Engineering and Applied Mechanics (MEAM)',
                    'CIS ': 'Computer and Information Science (CIS)'
                }
                owner = 'School of Engineering and Applied Science (SEAS)'
                for k, v in owner_map.items():
                    if k in title:
                        owner = v

                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': owner
                })
        except:
            pass
    return events


def fetch_events_vet(base_url='https://www.vet.upenn.edu/veterinary-hospitals/NBC-hospital/news-events/new-bolton-event'):
    """
    Fetch events for Veterinary Hospitals, New Bolton Center Hospital
    """
    events = []
    page_soup = BeautifulSoup(requests.get(
        urljoin(base_url, 'new-bolton-event')).content, 'html.parser')
    event_content = page_soup.find('div', attrs={'class': 'sf_cols'})
    all_events = event_content.find_all('div', attrs={'class': 'post event'})
    if len(all_events) > 0:
        for event_post in all_events:
            event_title = event_post.find('h3')
            if event_title is not None:
                title = event_title.text.strip()
                event_url = urljoin(base_url, event_title.find('a')['href'])
                date = event_post.find('time', attrs={'class': 'date'})
                date = date.text.strip() if date is not None else ''
                startend_time = event_post.find('b', attrs={'class': 'time'})
                startend_time = startend_time.text.strip() if startend_time is not None else ''
                starttime, endtime = find_startend_time(startend_time)

                try:
                    event_soup = BeautifulSoup(requests.get(
                        event_url).content, 'html.parser')
                    location = event_soup.find(
                        'div', attrs={'class': 'col-x8 post-content'}).find_all('ul')[1]
                    location = location.text.strip() if location is not None else ''
                    speaker = event_soup.find(
                        'div', attrs={'class': 'col-x12 articlebody'})
                    speaker = speaker.text.strip() if speaker is not None else ''
                    description = event_soup.find(
                        'div', attrs={'class': 'col-x12 articlebody'})
                    description = description.text.strip() if description is not None else ''
                except:
                    location, speaker, description = '', '', ''

                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': 'New Bolton Center Hospital (Veterinary Hospitals)'
                })
    return events


def fetch_events_gse(base_url='https://www.gse.upenn.edu/event'):
    """
    Fetch events for Graduate School of Education (GSE)
    """
    events = []
    date_now = datetime.today()
    date_next = date_now + relativedelta.relativedelta(months=1)
    year, month = date_now.year, date_now.month
    year_next, month_next = date_next.year, date_next.month
    for (y, m) in [(year, month), (year_next, month_next)]:
        event_extension = '?date={}-{}'.format(y, m)
        page_soup = BeautifulSoup(requests.get(
            base_url + event_extension
        ).content, 'html.parser')
        event_page = page_soup.find(
            'div', attrs={'class': 'region region-content'})
        event_content = event_page.find_all(
            'div', attrs={'class': 'view-content'})[1]
        all_events = event_content.find_all(
            'div', attrs={'class': 'views-row'})

        for event_post in all_events:
            title = event_post.find('span', attrs={'class': '_summary'})
            title = title.text.strip() if title is not None else ''
            description = event_post.find(
                'span', attrs={'class': '_description'})
            description = description.text.strip() if description is not None else ''
            date = event_post.find('span', attrs={'class': '_start'})
            date = date.text.split(' ')[0] if date is not None else ''
            speaker = event_post.find('span', attrs={'class': '_organizer'})
            speaker = speaker.text.strip() if speaker is not None else ''
            location = event_post.find(
                'div', attrs={'class': 'views-field-field-location-1'})
            location = location.text.strip() if location is not None else ''

            event_url = description.split('\n')[-1]
            try:
                event_soup = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                starttime = event_soup.find(
                    'span', attrs={'class': 'date-display-start'})
                starttime = starttime.text.strip() if starttime is not None else ''
                endtime = event_soup.find(
                    'span', attrs={'class': 'date-display-end'})
                endtime = endtime.text.strip() if endtime is not None else ''
                description = event_soup.find(
                    'div', attrs={'class': 'node-event'})
                description = description.find(
                    'div', attrs={'class': 'content'})
                description = description.find(
                    'div', attrs={'class': 'field-items'})
                description = description.text.strip() if description is not None else ''
                if starttime == '':
                    starttime = event_soup.find('span', attrs={'class': 'date-display-single'})
                    starttime = starttime.text.split('-')[-1].strip() if starttime is not None else ''
            except:
                starttime, endtime, description = '', '', ''

            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Graduate School of Education (GSE)'
            })
    return events


def fetch_events_grasp(base_url='https://www.grasp.upenn.edu'):
    """
    Fetch events from General Robotics, Automation,
    Sensing & Perception laboratory (GRASP) seminar
    """
    events = []
    event_page = requests.get(urljoin(base_url, 'events'))
    event_soup = BeautifulSoup(event_page.content, 'html.parser')

    event_panel = event_soup.find('div', attrs={'class': 'view-content'})
    all_events = event_panel.find_all('div', attrs={'class': 'views-row'})
    for event in all_events:
        title = event.find('div', attrs={'class': 'field-title'})
        title = title.text.strip() if title is not None else ''
        date = event.find(
            'div', attrs={'class': 'calendar-tile'}).attrs['content'].split('T')[0]
        event_url = urljoin(base_url, event.find('div').attrs.get('about'))
        if ':' in title:
            speaker = title.split(':')[-1]
        else:
            speaker = ''

        start_end_time = event.find(
            'span', attrs={'class': 'date-display-single'})
        if start_end_time is not None:
            starttime = start_end_time.find(
                'span', attrs={'class': 'date-display-start'})
            starttime = starttime.text.strip() if starttime is not None else ''
            endtime = start_end_time.find(
                'span', attrs={'class': 'date-display-end'})
            endtime = endtime.text.strip() if endtime is not None else ''

        event_detail_page = requests.get(event_url)
        event_detail_soup = BeautifulSoup(
            event_detail_page.content, 'html.parser')
        description = event_detail_soup.find(
            'div', attrs={'class': 'field-body'})
        description = description.text.strip() if description is not None else ''
        location = event_detail_soup.find(
            'div', attrs={'class': 'street-block'})
        location = location.text.strip() if location is not None else ''

        events.append({
            'title': title,
            'speaker': speaker,
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'General Robotics, Automation, Sensing & Perception laboratory (GRASP)'
        })
    return events


def fetch_events_wharton_stats(base_url='https://statistics.wharton.upenn.edu/research/seminars-conferences/'):
    """
    Fetch events from Wharton Statistics Seminars
    """
    events = []
    event_page = requests.get(base_url)
    event_soup = BeautifulSoup(event_page.content, 'html.parser')
    table = event_soup.find('table')
    if table is not None:
        all_events = table.find_all('tr')[1::]
        for event_tr in all_events:
            event_loc, speaker, title_desc = event_tr.find_all('td')
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title_desc.text.strip() if title_desc is not None else ''
            event_url = title_desc.find('a')
            event_url = event_url.attrs['href'] if event_url is not None else base_url

            if event_url is not base_url:
                event_soup = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                try:
                    description = event_soup.find(
                        'div', attrs={'class': 'wpb_wrapper'}).find_all('p')
                    description = ' '.join([p.text.strip()
                                            for p in description])
                except:
                    description = ''
            else:
                description = ''

            if len(event_loc.text.split('\n')) == 3:
                date, start_end_time, location = event_loc.text.split('\n')
                start_end_time = start_end_time.replace(
                    'Time: ', '').replace('*', '')
                starttime, endtime = start_end_time.split('-')
                starttime = starttime + endtime.split(' ')[-1]
                location = location.replace('Location: ', '').replace('*', '')
            events.append({
                'title': title,
                'speaker': speaker,
                'date': date,
                'location': location,
                'description': description,
                'starttime': starttime,
                'endtime': endtime,
                'url': event_url,
                'owner': 'Wharton Statistics Seminars'
            })
    return events


def fetch_events_school_design(base_url='https://www.design.upenn.edu'):
    """
    Fetch events from Weitzman School of Design

    url: https://www.design.upenn.edu/events-exhibitions
    """
    event_page = requests.get(urljoin(base_url, 'events-exhibitions'))
    event_soup = BeautifulSoup(event_page.content, 'html.parser')
    all_event_page = event_soup.find('div', attrs={'class': 'zone-content'})
    all_events = all_event_page.find_all(
        'div', attrs={'class': 'masonry-item'})

    events = []
    for event_pane in all_events:
        try:
            title = event_pane.find('h4', attrs={'class': 'field-content'})
            event_url = title.find('a').attrs.get('href')
            if event_url is not None:
                title = title.text.strip() if title is not None else ''
                event_url = urljoin(base_url, event_url)

                date = event_pane.find(
                    'span', attrs={'class': 'date-display-start'})
                if date is None:
                    date = event_pane.find(
                        'span', attrs={'class': 'date-display-single'})
                date = date.attrs['content']
                date = date.split('T')[0]

                event_page = BeautifulSoup(requests.get(
                    event_url).content, 'html.parser')
                details = event_page.find_all('h2', attrs={'class': 'odd'})
                if len(details) >= 2:
                    location = details[1]
                    location = location.text.strip() if location is not None else ''
                else:
                    location = ''

                if len(details) >= 1:
                    starttime = event_page.find_all(
                        'h2', attrs={'class': 'odd'})[0]
                    starttime, endtime = find_startend_time(
                        starttime.text.strip())
                else:
                    starttime, endtime = '', ''

                descriptions = event_page.find_all(
                    'div', attrs={'class': 'field-items'})[1:]
                description = ''
                for d in descriptions:
                    description += '\n'.join([p.text.strip()
                                              for p in d.find_all('p')])
                description = ' '.join(description.split(' ')[0:500])

                events.append({
                    'title': title,
                    'speaker': '',
                    'date': date,
                    'location': location,
                    'starttime': starttime,
                    'endtime': endtime,
                    'description': description,
                    'url': event_url,
                    'owner': 'School of Design (Weitzman)'
                })
        except:
            pass
    return events


def fetch_events_penn_museum(base_url='https://www.penn.museum/'):
    """
    Fetch events from Penn Museum, we select only lecture from https://www.penn.museum/calendar
    """
    events = []
    for start_range in range(0, 160, 20):
        all_event_url = urljoin(base_url, 'calendar/list.events/-?start={}'.format(start_range))
        event_page = requests.get(all_event_url)
        all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
        event_table = all_event_soup.find('div', attrs={'id': 'eventlist'})
        if event_table is not None:
            for event in event_table.find_all('div', attrs={'class': 'row'}):
                event_type = event.find('span', attrs={'class': 'badge dark-gray-bg'})
                event_type = event_type.text.strip() if event_type is not None else ''
                if 'lecture' in event_type.lower():
                    event_url = urljoin(base_url, event.find('a')['href'])
                    if event_url != '':
                        event_soup = BeautifulSoup(requests.get(
                            event_url).content, 'html.parser')
                        title = event_soup.find('h1')
                        subtitle = event_soup.find('h3')
                        title = title.get_text().strip() if title is not None else ''
                        subtitle = subtitle.get_text().strip() if subtitle is not None else ''
                        title = '{} {}'.format(title, subtitle)

                        date_time = event_soup.find('h2', attrs={'class': 'dark-gray'})
                        date = date_time.text.split('|')[0].strip() if date_time is not None else ''
                        time = date_time.text.split('|')[-1]
                        starttime, endtime = find_startend_time(time)
                        location = event_soup.find('div', attrs={'class': 'row mb-5'})
                        if location is not None:
                            location = location.find('div', attrs={'class': 'col-lg-3'})
                            location = location.text.replace('Location', '') if location is not None else ''
                        description = event_soup.find(
                            'div', attrs={'class': 'jev_evdt_desc'})
                        if description is not None:
                            r = description.find('script')
                            r = r.get_text() if r is not None else ''
                            description = '\n'.join(
                                [p.text.strip() for p in description.find_all('p') if p is not None]).strip()
                            description = description.replace(r, '')
                        else:
                            description = ''

                        events.append({
                            'title': title,
                            'speaker': '',
                            'date': date,
                            'location': location,
                            'description': description,
                            'starttime': starttime,
                            'endtime': endtime,
                            'url': event_url,
                            'owner': 'Penn Museum (lecture)'
                        })
    return events


def fetch_events_wharton_marketing(base_url='https://marketing.wharton.upenn.edu/events/dpcolloquia/'):
    """
    Fetch events from Wharton marketing department (Decision Processes Colloquia)
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    event_lists = all_event_soup.find_all('tr')

    date_location = all_event_soup.find_all(
        'div', attrs={'class': 'wpb_wrapper'})[2]
    date_location = '\n'.join([p.text for p in date_location.find_all('p')
                               if 'location' in p.text.lower()])
    location = ''.join([l for l in date_location.split('\n')
                        if 'location' in l.lower()]).replace('Location: ', '')
    time = ''.join([l for l in date_location.split('\n')
                    if 'time' in l.lower()])
    starttime = time.lower().replace('time:', '').split('–')[0]
    endtime = time.lower().replace('time:', '').split('–')[-1]
    endtime = find_startend_time(endtime)[0]

    for event_list in event_lists:
        if len(event_list.find_all('td')) == 3:
            try:
                pdf_url = event_list.find_next_sibling(
                    'ul').find('a').attrs['href']
            except:
                pdf_url = ''

            if pdf_url is not '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''

            date, speaker, title = event_list.find_all('td')
            date = date.text.strip() if date is not None else ''
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title.text.strip() if title is not None else ''
            if date != '' and title != 'TBD':
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': base_url,
                    'owner': 'Decision Processes Colloquia (Wharton)'
                })
    return events


def fetch_events_marketing_col(base_url='https://marketing.wharton.upenn.edu/events/marketing-colloquia-2019-2020/'):
    """
    Fetch events from Wharton Marketing Department (Marketing Colloquia)
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    all_events = all_event_soup.find_all('div', attrs={'class': 'vc_toggle'})

    date_location = all_event_soup.find_all(
        'div', attrs={'class': 'wpb_wrapper'})[0]
    date_location = '\n'.join([p.text for p in date_location.find_all('p')
                               if 'location' in p.text.lower()])
    location = ''.join([l for l in date_location.split('\n')
                        if 'location' in l.lower()]).replace('Location: ', '')
    time = ''.join([l for l in date_location.split('\n')
                    if 'time' in l.lower()])
    starttime = time.lower().replace('time:', '').split('–')[0]
    endtime = time.lower().replace('time:', '').split('–')[-1]
    endtime = find_startend_time(endtime)[0]

    for event in all_events:
        date_speaker = event.find('div', attrs={'class': 'vc_toggle_title'})
        if date_speaker is not None:
            title = date_speaker.text.strip()
            date, speaker = date_speaker.text.strip().split('~')
            speaker = speaker.replace('Speaker:', '').strip()
            pdf_url = event.find('a')['href'] if event.find(
                'a') is not None else ''
            if pdf_url != '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''
            if 'Speaker TBA' not in title:
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': base_url,
                    'owner': 'Marketing Department Colloquia (Wharton)'
                })
    return events


def fetch_events_macro_seminar(base_url='https://fnce.wharton.upenn.edu/department-information/seminars/macro-seminars/'):
    """
    Fetch events from Macro Seminar, Wharton
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    date_location = all_event_soup.find_all(
        'div', attrs={'class': 'wpb_wrapper'})[1]
    date_location = date_location.text.strip()
    location = ''.join([l for l in date_location.split('\n')
                        if 'sh-dh' in l.lower()])
    time = ''.join([l for l in date_location.split('\n')
                    if ' to ' in l.lower()])
    starttime = time.split(' ')[1] + ' ' + time.split(' ')[-1]
    endtime = time.split(' ')[-2] + ' ' + time.split(' ')[-1]
    year = date_location.split('\n')[1].split(' ')[-1]

    event_lists = all_event_soup.find_all('tr')[1:]
    for event_list in event_lists:
        if len(event_list.find_all('td')) == 3:
            date, speaker, title = event_list.find_all('td')
            pdf_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            if pdf_url != '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''
            date = date.text.strip() if date is not None else ''
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title.text.strip() if title is not None else ''
            date = date + ' ' + year
            if title.strip() is not '':
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': base_url,
                    'owner': 'Finance Department, Macro Seminar (Wharton)'
                })
    return events


def fetch_events_micro_seminar(base_url='https://fnce.wharton.upenn.edu/department-information/seminars/micro-seminars/'):
    """
    Fetch events from Micro Seminar, Wharton
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    date_location = all_event_soup.find_all(
        'div', attrs={'class': 'wpb_wrapper'})[1]
    date_location = date_location.text.strip()
    location = ''.join([l for l in date_location.split('\n')
                        if 'sh-dh' in l.lower()])
    time = ''.join([l for l in date_location.split('\n')
                    if ' to ' in l.lower()])
    starttime = time.split(' ')[1] + ' ' + time.split(' ')[-1]
    endtime = time.split(' ')[-2] + ' ' + time.split(' ')[-1]
    year = date_location.split('\n')[1].split(' ')[-1]

    event_lists = all_event_soup.find_all('tr')[1:]
    for event_list in event_lists:
        if len(event_list.find_all('td')) == 3:
            date, speaker, title = event_list.find_all('td')
            pdf_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            if pdf_url != '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''
            date = date.text.strip() if date is not None else ''
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title.text.strip() if title is not None else ''
            date = date + ' ' + year
            if title.strip() is not '':
                events.append({
                    'date': date,
                    'url': base_url,
                    'speaker': speaker,
                    'title': title,
                    'location': location,
                    'starttime': starttime,
                    'endtime': endtime,
                    'description': description,
                    'owner': 'Finance Department, Micro Seminar (Wharton)'
                })
    return events


def fetch_events_accounting_wharton(base_url='https://accounting.wharton.upenn.edu/research/workshops/'):
    """
    Fetch events from Wharton Accounting Department Workshop
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    event_lists = all_event_soup.find_all('tr')[1:]

    date_location = all_event_soup.find_all(
        'div', attrs={'class': 'wpb_wrapper'})[2]
    date_location = '\n'.join([p.text for p in date_location.find_all('p')
                               if 'location' in p.text.lower()])
    location = ''.join([l for l in date_location.split('\n')
                        if 'location' in l.lower()]).replace('Location:\xa0', '')
    time = ''.join([l for l in date_location.split('\n')
                    if 'time' in l.lower()])
    starttime = time.lower().replace('time:', '').split('–')[0]
    endtime = time.lower().replace('time:', '').split('–')[-1]
    endtime = find_startend_time(endtime)[0]

    for event_list in event_lists:
        if len(event_list.find_all('td')) == 3:

            date, speaker, title = event_list.find_all('td')
            pdf_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            if pdf_url is not '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''

            date = date.text.strip() if date is not None else ''
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title.text.strip() if title is not None else ''
            if title is not '':
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': base_url,
                    'owner': 'Accounting Department (Wharton)'
                })
    return events


def fetch_events_lgst_wharton(base_url='https://lgst.wharton.upenn.edu/department-information/seminars-conferences-2/'):
    """
    Fetch events from Wharton Legal Studies & Business Ethic Department

    **Note** that they attach PNG file instead of PDF so that we cannot scrape the data
    """
    events = []
    event_page = requests.get(base_url)
    all_event_soup = BeautifulSoup(event_page.content, 'html.parser')
    event_lists = all_event_soup.find_all('tr')[1:]

    location = '641 Jon M. Huntsman Hall '
    starttime = '12:00 PM'
    endtime = '1:00 PM'

    for event_list in event_lists:
        if len(event_list.find_all('td')) == 3:

            date, speaker, title = event_list.find_all('td')
            pdf_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            if pdf_url is not '':
                _, description = parse_pdf_abstract(pdf_url)
            else:
                description = ''

            date = date.text.strip() if date is not None else ''
            speaker = speaker.text.strip() if speaker is not None else ''
            title = title.text.strip() if title is not None else ''
            if title is not '':
                events.append({
                    'title': title,
                    'speaker': speaker,
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': base_url,
                    'owner': 'Legal Studies & Business Ethic Department (Wharton)'
                })
    return events


def fetch_events_energy_econ(base_url='https://bepp.wharton.upenn.edu/research/energy-economics-finance-seminar/'):
    """
    Fetch events from Energy Economics & Finance Seminar, Wharton
    """
    google_calendar_url = 'https://calendar.google.com/calendar/ical/p6q3dfdoaja41dencu1geh66as%40group.calendar.google.com/public/basic.ics'
    events_calendar = read_google_ics(google_calendar_url)

    events = []
    for event in events_calendar:
        # Title already set by read_google_ics()
        event['speaker'] = event['title']
        # Date already set
        event['location'] = 'Kleinman Center classroom—Fisher Fine Arts Room 306'
        #Description, starttime, and endtime already set
        event['url'] = base_url
        event['owner'] = 'Energy Economics & Finance Seminar'
        events.append(event)
    return events


def fetch_events_industrial_org(base_url='https://bepp.wharton.upenn.edu/research/industrial-organization-workshop/'):
    """
    Fetch events from Industrial Organization Seminar, Wharton
    """
    google_calendar_url = 'https://www.google.com/calendar/ical/ogllsefq4duep5dgj9dprkvjqc%40group.calendar.google.com/public/basic.ics'
    events_calendar = read_google_ics(google_calendar_url)

    events = []
    for event in events_calendar:
        # Remaining fields set by read_google_ics()
        event['speaker'] = event['title']
        event['location'] = 'The Ronald O. Perelman Center for Political Science and Economics (PCPSE); 133 South 36th Street – Room 101'
        event['url'] = base_url
        event['owner'] = 'Industrial Organization Seminar (Wharton)'
        events.append(event)
    return events


def fetch_events_applied_econ_workshop(base_url='https://bepp.wharton.upenn.edu/research/seminars-conferences/'):
    """
    Fetch events from Applied Economics Workshop, Wharton
    """
    google_calendar_url = 'https://www.google.com/calendar/ical/beppwharton%40gmail.com/public/basic.ics'
    events_calendar = read_google_ics(google_calendar_url)

    events = []
    for event in events_calendar:
        # Remaining fields set by read_google_ics()
        event['speaker'] = event['title']
        event['location'] = '265 JMHH'
        event['url'] = base_url
        event['owner'] = 'Applied Economics Workshop (Wharton)'
        events.append(event)
    return events


def fetch_events_public_policy(base_url='https://publicpolicy.wharton.upenn.edu/calendar/#!view/all'):
    """
    Fetch events from Public Policy Initiative (Wharton)
    """
    json_url = """
    https://publicpolicy.wharton.upenn.edu/live/calendar/view/all?user_tz=IT&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22thumb_width%22%3E138%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E138%3C%2Farg%3E%3Carg%20id%3D%22modular%22%3Etrue%3C%2Farg%3E%3C%2Fwidget%3E
    """.strip()
    events = fetch_json_events(
        base_url,
        json_url,
        owner='Public Policy Initiative (Wharton)'
    )
    return events


def fetch_events_nursing(base_url='https://www.nursing.upenn.edu/calendar/#!view/all'):
    """
    Fetch events from Penn Nursing
    """
    json_url = """
    https://www.nursing.upenn.edu/live/calendar/view/all?user_tz=IT&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22modular%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22show_public%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22default_view%22%3Emonth%3C%2Farg%3E%3Carg%20id%3D%22exclude_group%22%3EWeb%20Admin%3C%2Farg%3E%3C%2Fwidget%3E
    """.strip()
    events = fetch_json_events(
        base_url,
        json_url,
        owner='Nursing'
    )
    return events


def fetch_events_gcb(base_url='https://events.med.upenn.edu/gcb/#!view/all'):
    """
    Fetch events from Genomics and Computational Biology Graduate Group (GCB)
    """
    json_url = """
    https://events.med.upenn.edu/live/calendar/view/all?user_tz=IT&syntax=%3Cwidget%20type%3D%22events_calendar%22%3E%3Carg%20id%3D%22mini_cal_heat_map%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22thumb_width%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22thumb_height%22%3E200%3C%2Farg%3E%3Carg%20id%3D%22hide_repeats%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_groups%22%3Efalse%3C%2Farg%3E%3Carg%20id%3D%22show_tags%22%3Etrue%3C%2Farg%3E%3Carg%20id%3D%22default_view%22%3Eday%3C%2Farg%3E%3Carg%20id%3D%22group%22%3EGenomics%20and%20Computational%20Biology%20Graduate%20Group%20%28GCB%29%3C%2Farg%3E%3Carg%20id%3D%22group%22%3EBiomedical%20Graduate%20Studies%20%28BGS%29%3C%2Farg%3E%3Carg%20id%3D%22tag%22%3EGCB%3C%2Farg%3E%3Carg%20id%3D%22webcal_feed_links%22%3Etrue%3C%2Farg%3E%3C%2Fwidget%3E
    """.strip()
    events = fetch_json_events(
        base_url,
        json_url,
        owner='Genomics and Computational Biology Graduate Group (GCB)'
    )
    return events


def fetch_events_ppe(base_url='https://ppe.sas.upenn.edu/events'):
    """
    Fetch events from Philosophy Politics & Economics (PPE)
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    all_events = page_soup.find_all('ul', attrs={'class': 'unstyled'})[1]

    for event in all_events.find_all('li'):
        title = event.find('h3', attrs={'class': 'field-content'})
        if title is not None:
            event_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            event_url = urljoin(base_url, event_url)
            title = title.text.strip() if title is not None else ''

        date = event.find('p', attrs={'class': 'dateline'})
        date = date.text.strip() if date is not None else ''

        location = event.find('div', attrs={'class': 'location'})
        location = location.text.strip() if location is not None else ''

        if event_url is not base_url:
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            description = event_soup.find(
                'div', attrs={'class': 'field-items'})
            description = description.get_text() if description is not None else ''
            date_time = event_soup.find(
                'span', attrs={'class': 'date-display-single'})
            starttime, endtime = find_startend_time(date_time.get_text())
        else:
            description, starttime, endtime = '', '', ''
        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description.strip(),
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Philosophy Politics & Economics (PPE)'
        })
    return events


def fetch_events_perry_world(base_url='https://global.upenn.edu/perryworldhouse/events'):
    """
    Fetch events from Perry World House
    """
    events = []
    html_page = requests.get(base_url)
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    all_events = page_soup.find_all('article')

    for event in all_events:
        event_url = urljoin(base_url, event.attrs['about'])
        title = event.find('span', attrs={'class': 'events-teaser__heading'})
        title = title.text.strip() if title is not None else ''
        date_time = event.find(
            'div', attrs={'class': 'events-teaser__divider-text'})
        starttime, endtime = find_startend_time(date_time.get_text())
        date = date_time.get_text().strip().split('\n')[0].strip()

        if event_url is not base_url:
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            description = event_soup.find(
                'div', attrs={'class': 'events-details-page__content'})
            description = description.get_text().strip() if description is not None else ''
            description = ' '.join(description.split(' ')[0:500])
            location = event_soup.find(
                'div', attrs={'class': 'events-details-page__top__content__location'})
            location = location.text.strip() if location is not None else ''
        else:
            description, location = '', ''

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description.strip(),
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Perry World House'
        })
    return events


def fetch_events_psychology(base_url='https://psychology.sas.upenn.edu/calendar'):
    """
    Fetch events from Department of Psychology
    """
    events = []
    html_page = requests.get(base_url)
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    all_events = page_soup.find_all('div', attrs={'class': 'calendar'})

    for event in all_events:
        title = event.find('a')
        event_url = title['href'] if title is not None else ''
        event_url = urljoin(base_url, event_url)
        title = title.text.strip() if title is not None else ''
        date_time = event.find('span', attrs={'class': 'date-display-single'})
        starttime, endtime = find_startend_time(date_time.get_text())
        date = date_time.get_text().strip().split('\n')[0].strip()

        if event_url is not base_url:
            event_soup = BeautifulSoup(requests.get(
                event_url).content, 'html.parser')
            description = event_soup.find(
                'div', attrs={'class': 'field-name-body'})
            description = description.get_text().strip() if description is not None else ''
            description = ' '.join(description.split(' ')[0:500])
            location = event_soup.find_all(
                'div', attrs={'class': 'field-item even'})
            location = location[1] if len(location) >= 2 else ''
            location = location.text.strip() if location is not None else ''
        else:
            description, location = '', ''

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description.strip(),
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Department of Psychology (Psychology)'
        })
    return events


def fetch_events_neuro_wharton(base_url='https://neuro.wharton.upenn.edu/events/'):
    """
    Fetch events from Wharton Nueroscience Intiative
    ref: https://neuro.wharton.upenn.edu/events/
    """
    events = []
    html_page = requests.get(base_url)
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    all_events = page_soup.find('div', attrs={'class': 'tribe-events-loop'})

    for event in all_events.find_all('div', attrs={'class': 'type-tribe_events'}):
        event_url = event.find('a').attrs['href']
        title = event.find('a').attrs['title']
        date = event.find('div', attrs={'class': 'calendar-page'})
        date = date.get_text() if date is not None else ''

        event_soup = BeautifulSoup(requests.get(
            event_url).content, 'html.parser')
        date_time_loc = event_soup.find(
            'div', attrs={'class': 'tribe-events-content-header group'})
        date_time_loc = date_time_loc.find(
            'h3') if date_time_loc is not None else ''
        date_time_loc = date_time_loc.get_text().strip()
        date = date_time_loc.split('\n')[0]
        location = date_time_loc.split('\n')[-1].strip()
        starttime, endtime = find_startend_time(date)
        description = event_soup.find(
            'div', attrs={'class': 'tribe-events-content-wrapper'})
        description = description.get_text().strip() if description is not None else ''

        events.append({
            'title': title,
            'speaker': '',
            'date': date.split('|')[0],
            'location': location,
            'description': description.strip(),
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Wharton Neuroscience Initiative'
        })
    return events


def fetch_events_pspdg(base_url='https://pennsciencepolicy.squarespace.com'):
    """
    Fetch events from Penn Science Policy & Diplomacy Group (PSPDG)
    """
    events = []
    html_page = requests.get(urljoin(base_url, '/events'))
    page_soup = BeautifulSoup(html_page.content, 'html.parser')
    all_events = page_soup.find_all('article', attrs={'class': 'eventlist-event'})

    for event in all_events:
        title = event.find('h1', attrs={'class': 'eventlist-title'})
        if title is not None:
            event_url = title.find('a')['href'] if title.find(
                'a') is not None else ''
            event_url = urljoin(base_url, event_url)
            title = title.text.strip() if title is not None else ''

        date = event.find('time', attrs={'class': 'event-date'})
        date = date.text.strip() if date is not None else ''

        time = event.find('span', attrs={'class': 'event-time-12hr'})
        startend_time = time.text.strip() if time is not None else ''
        if startend_time is not '':
            starttime, endtime = find_startend_time(startend_time)
        else:
            starttime, endtime = '', ''

        location = event.find('li', attrs={'class': 'eventlist-meta-address'})
        location = location.text.replace('(map)', '').strip() if location is not None else ''

        description = event.find('div', attrs={'class': 'sqs-block-content'})
        description = description.text.strip() if description is not None else ''

        events.append({
            'title': title,
            'speaker': '',
            'date': date,
            'location': location,
            'description': description,
            'starttime': starttime,
            'endtime': endtime,
            'url': event_url,
            'owner': 'Penn Science Policy & Diplomacy Group (PSPDG)'
        })
    return events


def fetch_events_wolf_humanities(base_url='https://wolfhumanities.upenn.edu'):
    """
    Fetch events from Wolf Humanities Center
    ref: https://wolfhumanities.upenn.edu/events/current
    """
    events = []
    page_soup = BeautifulSoup(requests.get(urljoin(base_url, '/events/current')).content, 'html.parser')
    event_content = page_soup.find('ul', attrs={'class': 'media-list'})
    all_events = event_content.find_all('li', attrs={'class': 'clearfix'}) if event_content is not None else []

    if len(all_events) > 0:
        for event in all_events:
            if event.find('a') is not None:
                event_url = urljoin(base_url, event.find('a')['href'])
                event_soup = BeautifulSoup(requests.get(event_url).content, 'html.parser')
                title = event_soup.find('h1')
                title = title.text.strip() if title is not None else ''
                subtitle = event_soup.find('h2')
                subtitle = subtitle.text.strip() if subtitle is not None else ''
                if subtitle is not '':
                    title = '{}, {}'.format(title, subtitle)

                location = event_soup.find('div', attrs={'class': 'field-location'})
                location = location.text.strip() if location is not None else ''

                date_time = event_soup.find('span', attrs={'class': 'date-display-single'})
                if date_time is not None:
                    date_time = date_time.text.strip()
                    date = date_time.split('-')[0]
                    starttime, endtime = find_startend_time(date_time)
                else:
                    date_time = event_soup.find('span', attrs={'class': 'date-display-start'})
                    date = date_time.text.strip()
                    starttime, endtime = find_startend_time(date)

                description = event_soup.find('div', attrs={'class': 'field-body'})
                description = description.get_text().strip() if description is not None else ''

                events.append({
                    'title': title,
                    'speaker': '',
                    'date': date,
                    'location': location,
                    'description': description,
                    'starttime': starttime,
                    'endtime': endtime,
                    'url': event_url,
                    'owner': 'Wolf Humanities Center'
                })
    return events
