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


class GetEvent(Resource):
    """
    Return events base on days ahead
    """
    input_args = {
        'days': fields.Int(missing=None, required=False),
        'owner': fields.String(missing=None, required=False)
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
            event['owner_query'] = '-'.join(event['owner'].lower().replace('/', ' ').split())
            if event['date_dt'].strip() != '':
                event['date_dt'] = dateutil.parser.parse(event['date_dt'])
            else:
                event['date_dt'] = datetime.today()
            events_query.append(event)

        # filter days
        if args['days'] is not None:
            date_retrieve = datetime.today() + timedelta(days=args['days'])
            events_query = list(filter(lambda x: x['date_dt'] >= datetime.today() and x['date_dt'] <= date_retrieve,
                                events_query))

        # filter owners
        if args['owner'] is not None:
            events_query = list(filter(lambda x: x['owner'].lower() == args['owner'],
                                events_query))
        
        for event in events_query:
            event['date_dt'] = event['date_dt'].strftime("%A, %d %B")

        return events_query


api.add_resource(GetEvent, '/api/v1/getevent')


if __name__ == '__main__':
    app.run(port=5001, debug=True)
