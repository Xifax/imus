# -*- coding=utf-8 -*-

import os
import json

from redis import StrictRedis

from conf.const import extensions
from media.tags import track_info

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
        # TODO: should probably use ':::' instead of double colon
        cola = u'::'
        self.key = cola.join([self.title, self.album, self.artist, self.folder])
        self.data = {'duration' : duration, 'plays' : plays,  'scrobbles' : scrobbles}

    def stats(self):
        return json.dumps(self.data)

    def update_stats(self, value):
        try:
            self.data = json.loads(value)
        except ValueError:
            pass

    def __repr__(self):
        return u"Title: %s | artist: %s | album: %s | location: %s" \
                % (self.title, self.artist, self.album, self.folder)

    @staticmethod
    def from_redis(key, value):
        if key is not None:
            track = Track.from_arguments(key.split('::'))
            track.update_stats(value)
            return track

    @staticmethod
    def from_arguments(*args):
        for arg in args:
            return Track(title=arg.pop(0),
                         album=arg.pop(0),
                         artist=arg.pop(0),
                         folder=arg.pop(0))

                         # TODO: fix this
                         #duration=arg.pop(0),
                         #plays=arg.pop(0),
                         #scrobbles=arg.pop(0))

class Redis:

    def __init__(self, host='localhost',
                       port=6379,
                       db=0,
                       password=None):
        self.r = StrictRedis(host, port, db, password)

    def update(self, track):
        self.r.set(track.key, track.stats())

    def lookup(self, keyword):
        # TODO: add option to search case-less
        return self.r.keys('*' + keyword + '*')

    def retrieve(self, key):
        return Track.from_redis(key, self.r.get(key))

class Crawler:

    def __init__(self, redis=None):
        self.r = Redis() if redis is None else redis

    def crawl(self, path):
        for(dirpath, dirnames, filenames) in os.walk(path):
            for filename in filenames:
                #print filename
                if filename[-3:] in extensions:
                    self.r.update(Track.
                                    from_arguments(
                                        track_info(os.path.join(dirpath, filename))))
