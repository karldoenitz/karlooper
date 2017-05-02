# -*- coding: utf-8 -*-

from karlooper.config import get_global_conf
from karlooper.web.request import Request

__author__ = "karlvorndoenitz@gmail.com"


class ChatController(Request):
    def get(self):
        redis_manager = get_global_conf("redis")
        user_list = redis_manager.get_user_list()
        user_id = 0
        if user_list:
            user_id = user_list[-1] + 1
            redis_manager.set_user_list(user_list + [user_id])
        else:
            redis_manager.set_user_list([user_id])
        return self.render("/chat-window.html", user=user_id)
