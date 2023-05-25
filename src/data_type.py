#!/bin/python


class CoreInfo(object):
    def __init__(self, bran: str, url: str, sid: str):
        self.bran = bran
        self.url = url
        self.sid = sid


class CoreQueue(object):
    def __init__(self):
        self.val_list = []
        self.id_list = []
