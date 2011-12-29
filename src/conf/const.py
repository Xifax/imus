# -*- coding=utf-8 -*-

name = 'imus'
version = '0.1'
developer = 'Artiom Basenko'
info = 'Scrobbler that scrobbles.'

# TODO:  Testing in progress, should select one of the hsaudio/mutagen libraries
# TODO: ... the same goes for agrh/argparse, I guess
packages = ['redis', 'hiredis', 'hsaudiotag', 'mutagen', 'argparse', 'argh']
extensions = ['mp3', 'flac', 'mp4', 'mped', 'ogg', 'aiff']

API_KEY = "0cacd3c709ef73d915ccea46dd8afda8"
API_SECRET = "cf3cf18968006517750ea2215544636d"
