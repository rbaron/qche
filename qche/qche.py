# coding: utf-8
import cPickle as pickle
import json
import logging
import os
import sys


class BaseQche(object):
    def __init__(self, *args, **kwargs):
        self._data = self._load_or_init(*args, **kwargs)

    def _load_or_init(self, *args, **kwargs):
        raise NotImplementedError

    def _persist(self, data):
        raise NotImplementedError

    def put(self, key, value):
        self._data[self.sanitize_key(key)] = value

    def get(self, key):
        return self._data.get(self.sanitize_key(key))

    def persist(self):
        self._persist(self._data)

    @property
    def size(self):
        return len(self._data)

    def keys(self):
        return self._data.keys()

    def sanitize_key(self, key):
        """ Unfor """
        if isinstance(key, str):
            return key.decode("utf-8")
        else:
            return key

    def __contains__(self, key):
        return self.sanitize_key(key) in self._data

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, val):
        self._data[key] = val

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.persist()


class InMemoryCache(BaseQche):
    def _load_or_init(self, verbose=False):
        self.verbose = verbose

        if self.verbose:
            logging.info("Initializing new in-memory cache")
        return {}

    def _persist(self, data):
        if self.verbose:
            logging.info("Discaring in-memory-only cache.")
        pass


class FilesystemPersistedCache(BaseQche):
    @property
    def serializer(self):
        raise NotImplementedError

    def _load_or_init(self, filename, verbose=False):
        self.filename = filename
        self.verbose = verbose

        if self.verbose:
            logging.info("Initializing new filesystem persistent cache on {}".format(
                filesystem))

        if os.path.isfile(filename):
            with open(filename, "r") as f:
                val = self.serializer.load(f) or {}
        else:
            val = {}
            with open(filename, "w") as f:
                self.serializer.dump(val, f)
        return val

    def _persist(self, data):
        if self.verbose:
            logging.info("Persisting cache on filesystem at {}".format(self.filename))

        with open(self.filename, "w") as f:
            self.serializer.dump(data, f)

        if self.verbose:
            logging.info("Cache persisted.")


class JsonCache(FilesystemPersistedCache):
    @property
    def serializer(self):
        return json


class PickleCache(FilesystemPersistedCache):
    @property
    def serializer(self):
        return pickle
