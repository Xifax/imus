# -*- coding=utf-8 -*-

import os

from hsaudiotag import auto

from db.library import Track

def track_info(path):
    if os.path.exists(path):
        track = auto.File(path)
        return Track(track.title,
                     track.album,
                     track.artist,
                     path.split('/')[-1],
                     track.duration)

def track_info_mutha(path):
    pass


