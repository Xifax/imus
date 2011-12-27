# -*- coding=utf-8 -*-
# NB: hsaudio breaks on tags with '/'
# TODO: also process genre?

from hsaudiotag import auto

#from db.library import Track

def track_info(path):
    #print path
    try:
        track = auto.File(path)
        return [track.title,
                     track.album,
                     track.artist,
                     #path.split('/')[:-1],
                     path,
                     track.duration]
        #return Track(track.title,
                     #track.album,
                     #track.artist,
                     #path.split('/')[-1],
                     #track.duration)
    except IOError:
        pass

def track_info_mutha(path):
    pass


