import hashlib
import json
import pickle

import requests

from constants import CACHE_SERVICE_PORT
from helpers.api_helpers import b64decode, b64encode

CACHE_SERVICE_URL = f'http://127.0.0.1:{CACHE_SERVICE_PORT}'
STORE_ADDRESS = f'{CACHE_SERVICE_URL}/store'


def __is_class(value):
    return hasattr(value, '__class__')


def cache(limit=None):
    def decorator(method):
        def inner(*args, **kwargs):
            category = f'{method.__module__}.{method.__name__}'
            args_to_hash = list(args)
            if len(args_to_hash) > 0 and __is_class(args_to_hash[0]):
                args_to_hash.pop(0)  # Filter out the self argument of methods
            arguments_key = hashlib.sha256(pickle.dumps([args_to_hash, kwargs])).hexdigest()
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


def reset_cache():
    response = requests.delete(STORE_ADDRESS)
    response.raise_for_status()
