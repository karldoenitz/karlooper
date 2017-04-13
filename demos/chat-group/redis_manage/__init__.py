# -*- coding: utf-8 -*-

from redis import Redis

__author__ = "karlvorndoenitz@gmail.com"


class RedisManage(object):
    def __init__(self):
        self.r = Redis(host='localhost', port=6379, db=0)

    def set_value(self, value):
        old_value = self.r.get("chat_group_message")
        if old_value:
            value = eval(old_value)[-10:] + value
        self.r.set("chat_group_message", value, 3600*100)

    def get_value(self):
        chat_msg = self.r.get("chat_group_message")
        if chat_msg:
            return eval(chat_msg)
        return []

    def get_user_list(self):
        user_list = self.r.get("users")
        if user_list:
            return eval(user_list)

    def set_user_list(self, user_id_list):
        self.r.set("users", user_id_list)
