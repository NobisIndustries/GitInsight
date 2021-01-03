import hashlib
import json
import pickle

import requests

from constants import CACHE_SERVICE_PORT
from helpers.api_helpers import b64decode, b64encode

CACHE_SERVICE_URL = f'http://127.0.0.1:{CACHE_SERVICE_PORT}'
STORE_ADDRESS = f'{CACHE_SERVICE_URL}/store'


def cache(limit=None):
    def decorator(method):
        def inner(*args, **kwargs):
            category = str(method.__name__)
            arguments_key = hashlib.sha256(pickle.dumps([args, kwargs])).hexdigest()
            url = f'{STORE_ADDRESS}/{category}/{arguments_key}'
            value_raw = requests.get(url).content
            if value_raw != b'null':
                return pickle.loads(b64decode(value_raw, as_string=False))

            value = method(*args, **kwargs)
            response = requests.post(url, data=json.dumps({'value': b64encode(pickle.dumps(value)), 'limit': limit}))
            response.raise_for_status()
            return value
        return inner
    return decorator
