import os

# Module containing scrapers for extracting data from webpages
# Every public function (i.e., those not beginning with _) should return a list
# of event dictionaries when called with no arguments.
import local.upenn.scrapers
scrapers = local.upenn.scrapers

# Module containing a list of locations (for feature generation)
import local.upenn.locations
locations = local.upenn.locations.locations

# Path to save event data (as json)
PATH_DATA = os.path.join('data', 'events.json')  # path to save events
PATH_FETCH_DATA = os.path.join('data', 'fetch_record.json')
PATH_VECTOR = os.path.join('data', 'events_vector.json')

# ElasticSearch configuration
ELASTIC_HOST = 'localhost'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'penn-events'
