"""
A backend service for Penn event calendar
Run the app:

    $ python api.py

This will serve on localhost:5000.

Example queries:
    - http://localhost:5000/api/v1/getevent?days=7 # return events happenning in next 7 day_args
    - http://localhost:5000/api/v1/getevent # return all events

"""
import os
import json
import dateutil.parser
from datetime import datetime, timedelta
from fetch_events import read_json, save_json

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort


app = Flask(__name__)
CORS(app)
api = Api(app, catch_all_404s=True)
events = read_json('events.json') # read saved events


class ShowEvent(Resource):
    """
    Return events base on days ahead
    """
    day_args = {
        'days': fields.Int(missing=None, required=False)
    }

    @use_args(day_args)
    def get(self, args):
        """Retrieve events from saved JSON"""
        date_retrieve = datetime.today()
        if args['days'] is None:
            events_to_show = events
            return events_to_show
        else:
            date_retrieve += timedelta(days=args['days'])

        events_to_show = []
        for event in events:
            if dateutil.parser.parse(event['date']) <= date_retrieve:
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


if __name__ == '__main__':
    api.add_resource(ShowEvent, '/api/v1/getevent')
    api.add_resource(ShowEventDetails, '/event_id/<int:event_id>')
    app.run(debug=True)
