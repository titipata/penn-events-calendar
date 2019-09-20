import hug

# enable CORS
api = hug.API(__name__)
api.http.add_middleware(hug.middleware.CORSMiddleware(api))


@hug.post("/recommendations")
def handle_post(body):
    '''
    Body is sent as JSON from the frontend with data as a value of a key 'payload':

    {
        "payload": data
    }

    The body is then passed as an argument to this function, as a dictionary.
    '''

    return body['payload']
