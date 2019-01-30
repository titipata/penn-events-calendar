"""
A backend service for Penn event calendar
Run the app:

    $ python api.py

This will serve on localhost:5001.

Example queries:
    - http://localhost:5001/api/v1/getevent?days=7 # return events happenning in next 7 days
    - http://localhost:5001/api/v1/getevent?days=7&school=medicine-health-system # return events in next 7 days from "Medicine/Health System"
    - http://localhost:5001/api/v1/getevent?days=14&category=academic # return events in academic category
    - http://localhost:5001/api/v1/getsimilarevents/696555 # return similar events to an event with event_id "696555"
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
    input_args = {
        'days': fields.Int(missing=None, required=False),
        'school': fields.String(missing=None, required=False),
        'category': fields.String(missing=None, required=False)
    }

    @use_args(input_args)
    def get(self, args):
        """
        Retrieve events from saved JSON
        """
        events = read_json('events.json')

        # add school query, parse datetime
        events_query = []
        for event in events:
            event['school_query'] = '-'.join(event['school'].lower().replace('/', ' ').split())
            event['date_dt'] = dateutil.parser.parse(event['date'])
            events_query.append(event)

        # filter school name
        if args['school'] is not None:
            events_query = list(filter(lambda x: x['school_query'] == args['school'],
                                events_query))

        # filter date
        if args['days'] is not None:
            date_retrieve = datetime.today() + timedelta(days=args['days'])
            events_query = list(filter(lambda x: x['date_dt'] >= datetime.today() and x['date_dt'] <= date_retrieve,
                                events_query))

        # filter category
        if args['category'] is not None:
            events_query = list(filter(lambda x: x['category'].lower() == args['category'],
                                events_query))

        # remove generated keys
        for event in events_query:
            event.pop('date_dt', None)
            event.pop('school_query', None)

        return events_query


class GetSimilarEvents(Resource):
    def get(self, event_id):
        file_path = 'similar_events.json'
        if os.path.exists(file_path):
            similar_events = json.load(open(file_path, 'r'))
        else:
            similar_events = {}
        return similar_events.get(event_id, [])


api.add_resource(ShowEvent, '/api/v1/getevent')
api.add_resource(GetSimilarEvents, '/api/v1/getsimilarevents/<string:event_id>')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
