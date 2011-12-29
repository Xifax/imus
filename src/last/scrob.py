# -*- coding=utf-8 -*-

import pylast

from conf.const import API_KEY, API_SECRET

class Scrobbler:

    def __init__(self, login, password):
        self.login = login
        self.password = pylast.md5(password)
        self.net = pylast.LastFMNetwork(api_key = API_KEY,
                                        api_secret = API_SECRET,
                                        username = username,
                                        password_hash = password_hash)
        #TODO: should also include client id
        self.sc = pylast.Scrobbler(self.net)
        self.queue = []

    def queue(self, track):
        #TODO: should check for duplicates or not?
        self.queue.append(track)

    def scrobble(self):
        #TODO: impelement
        self.sc.scrobble_mane(self.queue)

