# -*- coding=utf-8 -*-

name = 'imus'
version = '0.1'
developer = 'Artiom Basenko'
info = 'Scrobble that scrobbles.'
# TODO:  Testing in progress, should select one of the hsaudio/mutagen libraries
packages = ['redis', 'hiredis', 'hsaudiotag', 'mutagen']
extensions = ['mp3', 'flac', 'mp4', 'mped', 'ogg', 'aiff']
