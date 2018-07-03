import os
import json
from datetime import datetime, timedelta
from dateutil import parser
from fetch_events import read_json, save_json

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)
events = read_json('events.json') # read saved events


class ShowEvent(Resource):
    """
    Return events base on days ahead
    """
    def get(self, showndays=7):
        events_to_show = []
        for event in events:
            if parser.parse(event['date']) <= datetime.today() + timedelta(days=showndays):
                events_to_show.append(event)
        return events_to_show


class ShowEventDetails(Resource):
    """
    Return an event base on event ID
    """
    def get(self, event_id=None):
        event = {}
        for event in events:
            if int(event['event_id']) == event_id:
                return event
        return event


api.add_resource(ShowEvent, '/getevents/<int:showndays>')
api.add_resource(ShowEventDetails, '/event_id/<int:event_id>')


if __name__ == '__main__':
    app.run(debug=True)
