import os
import json
from datetime import datetime, timedelta
from dateutil import parser

from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


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
events = read_json('events.json')


class ShowEvent(Resource):
    def get(self, showndays=7):
        events_to_show = []
        for event in events:
            if parser.parse(event['date']) <= datetime.today() + timedelta(days=showndays):
                events_to_show.append(event)
        return events_to_show


api.add_resource(ShowEvent, '/showndays/<int:showndays>')

if __name__ == '__main__':
    app.run(debug=True)
