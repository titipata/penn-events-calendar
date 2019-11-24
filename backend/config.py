import os

# Module containing scrapers for extracting data from webpages
# Every public function (i.e., those not beginning with _) should return a list
# of event dictionaries when called with no arguments.
import backend.local.upenn.scrapers as scrapers

# Module containing a list of locations (for feature generation)
from backend.local.upenn.locations import locations

# Path to save event data (as json)
PATH_DATA = os.path.join('data', 'events.json')  # path to save events
PATH_FETCH_DATA = os.path.join('data', 'fetch_record.json')
PATH_VECTOR = os.path.join('data', 'events_vector.json')

# GROBID stuff for parsing PDFs
GROBID_URL = 'http://localhost:8070'
GROBID_PDF_URL = '{}/api/processFulltextDocument'.format(GROBID_URL)

# ElasticSearch configuration
ELASTIC_HOST = 'localhost'
ELASTIC_PORT = 9200
ELASTIC_INDEX = 'penn-events'
