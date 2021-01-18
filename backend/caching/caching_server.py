import sys
from collections import defaultdict
from dataclasses import dataclass
from typing import Any

from fastapi import FastAPI
from pydantic.main import BaseModel

from helpers.logging_helpers import init_logging

app = FastAPI()
init_logging(app)


@dataclass
class Entry:
    last_accessed_id: int
    payload: Any


class Store:
    """Implements a key-value store with lru characteristics for caching. Normally you would use
       Redis for stuff like this, but I don't want to install and integrate a whole other service for the
       small amounts of data that need to be cached. So the python homebrew variant it is."""

    MAX_INT = sys.maxsize

    def __init__(self):
        self._store = defaultdict(dict)
        self._id_counter = 0

    def reset(self):
        self._store = defaultdict(dict)
        self._id_counter = 0

    def __get_incrementing_id(self):
        self._id_counter += 1
        return self._id_counter

    def set_value(self, category, key, value, limit=None):
        entries = self._store[category]
        entries[key] = Entry(self.__get_incrementing_id(), value)

        if limit and len(entries) > limit:
            del entries[self.__get_key_with_oldest_id(entries)]

    def __get_key_with_oldest_id(self, entries):
        min_id = self.MAX_INT
        min_id_key = None

        for key, entry in entries.items():
            entry_id = entry.last_accessed_id
            if entry_id < min_id:
                min_id = entry_id
                min_id_key = key
        return min_id_key

    def get_value(self, category, key):
        if category in self._store:
            entries = self._store[category]
            if key in entries:
                entry = entries[key]
                entry.last_accessed_id = self.__get_incrementing_id()
                return entry.payload
        return None


store = Store()


class Value(BaseModel):
    value: str
    limit: int


@app.get('/store/{category}/{key}')
def get_value(category: str, key: str):
    return store.get_value(category, key)


@app.post('/store/{category}/{key}')
def set_value(category: str, key: str, payload: Value):
    store.set_value(category, key, payload.value, payload.limit)


@app.delete('/store')
def reset():
    store.reset()
