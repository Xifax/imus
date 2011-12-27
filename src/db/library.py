# -*- coding=utf-8 -*-

import json

from redis import StrictRedis

class Track:

    def __init__(self, title='',
                       album='',
                       artist='',
                       folder='',
                       duration=0,
                       plays=0,
                       scrobbles=0):
        self.title = title
        self.album = album
        self.artist = artist
        self.folder = folder
        colon = ':'
        self.key = colon.join([self.title, self.album, self.artist, self.folder])
        self.data = {'duration' : duration, 'plays' : plays,  'scrobbles' : scrobbles}

    def stats(self):
        return json.dumps(self.data)

    def update_stats(self, value):
        try:
            self.data = json.loads(value)
        except ValueError:
            pass

    def __repr__(self):
        return "Title: %s | artist: %s | album: %s | location: %s" \
                % (self.title, self.artist, self.album, self.folder)

    @staticmethod
    def from_redis(key, value):
        if key is not None:
            track = Track.arguments(key.split(':'))
            track.update_stats(value)
            return track

    @staticmethod
    def arguments(*args):
        for arg in args:
            return Track(arg.pop(0), arg.pop(0), arg.pop(0), arg.pop(0))

class Redis:

    def __init__(self, host='localhost',
                       port=6379,
                       db=0,
                       password=None):
        self.r = StrictRedis(host, port, db, password)

    def update(self, track):
        self.r.set(track.key, track.stats())

    def lookup(self, keyword):
        return self.r.keys('*' + keyword + '*')

    def retrieve(self, key):
        return Track.from_redis(key, self.r.get(key))

class Crawler:

    def __init__(self):
        pass

    def crawl(self, folder):
        pass
