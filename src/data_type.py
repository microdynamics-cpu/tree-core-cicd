#!/bin/python


class CoreInfo(object):
    def __init__(self, url: str, sid: str, flag='E'):
        self.url = url
        self.sid = sid
        self.flag = flag


class QueueInfo(object):
    def __init__(self, sid: str, date: str):
        self.sid = sid
        self.date = date
