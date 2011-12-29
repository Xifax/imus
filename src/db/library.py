# -*- coding=utf-8 -*-

import os
import json
from collections import defaultdict

from redis import StrictRedis

from conf.const import extensions
from media.tags import track_info

class Track:
    """
    To represent audio-track abstraction.
    May be stored in Redis (crude keys/namespaces!).
    """

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
        #try:
        self.key = cola.join([self.title.decode('utf-8'),
                            self.album.decode('utf-8'),
                            self.artist.decode('utf-8'),
                            self.folder.decode('utf-8'),
                            ])
        #except Exception:
            #self.key = cola.join([self.title, self.album, self.artist, self.folder])

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
                % (self.title.decode('utf-8'),
                   self.artist.decode('utf-8'),
                   self.album.decode('utf-8'),
                   self.folder.decode('utf-8'))

    def info(self):
        #try:
        return u"%s ( %s ) : %s" \
                % (self.artist.decode('utf-8'),
                   self.album.decode('utf-8'),
                   self.title.decode('utf-8'))
        #except Exception:
            #return u"%s ( %s ) : %s" \
                #% (self.artist, self.album, self.title)

                #% (self.artist, self.album, self.title)

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

    @staticmethod
    def structure(tracks):
        """
        Should structure list of tracks as:
            { folder : { artist_A : { ablum_A : { track_A,
                                                  track_B,
                                                 ... },
                                      album_B : { ... },
                                      ...  },
                         artist_B : { ... },
                        ... },
            }
        """
        # Let's start with artists (folders should be left for better times)
        artists = defaultdict(list)
        for track in tracks:
            # Composing list of similar artists
            # TODO: impelement filter function to get tracks list OR use lists comprehension
            artists[track.title].append(
                                    {track.album :
                                        [t.title for t in tracks if t.album == track.album]
                                    })
        return artists


class Redis:
    """
    To store and query local/remote Redis server.
    """

    def __init__(self, host='localhost',
                       port=6379,
                       db=0,
                       password=None):
        self.r = StrictRedis(host, port, db, password)

    def __del__(self):
        del(self.r)

    def update(self, track):
        self.r.set(track.key, track.stats())

    def lookup(self, keyword):
        # TODO: add option for caseless search
        return self.r.keys('*' + keyword + '*')

    def retrieve(self, key):
        if isinstance(key, list):
            return self.get_all(key)
        return Track.from_redis(key, self.r.get(key))

    def get_all(self, keys):
        tracks = []
        for key in keys:
            tracks.append(Track.from_redis(key, self.r.get(key)))
        return tracks

class Crawler:
    """
    To crawl on specified folders and yield metadata from media files.
    """

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
