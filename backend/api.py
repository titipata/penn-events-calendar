"""
A backend service for Penn event calendar
Run the app:

    $ python api.py

This will serve on localhost:5001.

Example queries:
    - http://localhost:5001/api/v1/getevent?days=7 # return events happenning in next 7 day_args
    - http://localhost:5001/api/v1/getevent # return all events

"""
import os
import json
import dateutil.parser
from datetime import datetime, timedelta
from fetch_events import read_json, save_json

from flask import Flask
from flask_restful import Resource, Api
from flask_cors import CORS
from gevent.wsgi import WSGIServer

from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort


app = Flask(__name__)
CORS(app)
app.debug = True
api = Api(app, catch_all_404s=True)


class ShowEvent(Resource):
    """
    Return events base on days ahead
    """
    day_args = {
        'days': fields.Int(missing=None, required=False)
    }

    @use_args(day_args)
    def get(self, args):
        """
        Retrieve events from saved JSON
        """
        events = read_json('events.json')
        date_retrieve = datetime.today()
        if args['days'] is None:
            events_to_show = events
            return events_to_show
        else:
            date_retrieve += timedelta(days=args['days'])

        events_to_show = []
        for event in events:
            event_date = dateutil.parser.parse(event['date'])
            if event_date <= date_retrieve and event_date >= datetime.today():
                events_to_show.append(event)
        return events_to_show


class ShowEventDetails(Resource):
    """
    Return an event's details base on given event ID
    """
    def get(self, event_id=None):
        events = read_json('events.json')
        event = {}
        for event in events:
            if event['event_id'] == event_id:
                return event
        return event


if __name__ == '__main__':
    api.add_resource(ShowEvent, '/api/v1/getevent')
    api.add_resource(ShowEventDetails, '/api/v1/event/<int:event_id>')
    http_server = WSGIServer(('0.0.0.0', 5001), app)
    http_server.serve_forever()
