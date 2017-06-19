# -*- coding: utf-8 -*-

from redis import Redis

__author__ = "karlvorndoenitz@gmail.com"


class RedisManage(object):
    def __init__(self):
        self.r = Redis(host='localhost', port=6379, db=0)

    def set_user(self, username, password):
        self.r.set(username, password, 3600*100)

    def get_user(self, username):
        return self.r.get(username)
