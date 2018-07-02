import os
import requests
import json
from unidecode import unidecode
from datetime import datetime
from dateutil import parser
from lxml import etree, html

DAYS = [
    "Mon", "Tue",
    "Wed", "Thu",
    "Fri", "Sat",
    "Sun"
]


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


if __name__ == '__main__':
    """
    Saving Penn events to JSON format
    """
    URL = 'http://www.upenn.edu/calendar-export/?showndays=50'
    page = requests.get(URL)
    tree = html.fromstring(page.content)
    events = tree.findall('event')
    event_list = []
    for event in events:
        try:
            event_dict = convert_event_to_dict(event)
            event_list.append(event_dict)
        except:
            pass
    save_json(event_list, 'events.json')
