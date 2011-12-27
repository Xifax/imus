# -*- coding=utf-8 -*-

import json

from redis import StrictRedis

class Track:

    def __init__(self, name='',
                       album='',
                       artist='',
                       folder=''):
        self.name = name
        self.album = album
        self.artist = artist
        self.folder = folder
        colon = ':'
        self.key = colon.join([self.name, self.album, self.artist, self.folder])
        self.data = {}

    def stats(self):
        return json.dumps(self.data)

    def update_stats(self, value):
        try:
            self.data = json.loads(value)
        except ValueError:
            pass

    @staticmethod
    def from_redis(key, value):
        if key is not None:
            track = Track(key.split(':'))
            track.update_stats(value)
            return track

class Redis:

    def __init__(self, host='localhost',
                       port=6379,
                       db=0,
                       password=None):
        self.r = StrictRedis(host, port, db, password)

    def update(self, track):
        self.r.set(track.key, track.stats())

    def lookup(self, keyword):
        return self.r.keys(keyword)

    def retrieve(self, key):
        return Track.from_redis(key, self.r.get(key))
