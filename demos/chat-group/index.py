# -*- coding: utf-8 -*-

import os
from karlooper.web.application import Application
from karlooper.web.request import Request
from redis_manage import RedisManage

__author__ = "karlvorndoenitz@gmail.com"


class MessageHandler(Request):
    def get(self):
        value = redis_manager.get_value()
        result = {
            "status": 0,
            "desc": "ok",
            "data": value
        }
        return self.response_as_json(result)

    def post(self):
        print self.get_http_request_message()
        from_user = self.get_parameter("from")
        new_value = self.decode_parameter_plus("value")
        redis_manager.set_value([str(from_user)+":"+new_value])
        result = {
            "status": 0,
            "desc": "ok"
        }
        return self.response_as_json(result)


class ChatController(Request):
    def get(self):
        user_list = redis_manager.get_user_list()
        user_id = 0
        if user_list:
            user_id = user_list[-1] + 1
            redis_manager.set_user_list(user_list + [user_id])
        else:
            redis_manager.set_user_list([user_id])
        return self.render("/chat-window.html", user=user_id)


handlers_mapping = {
    "/msg": MessageHandler,
    "/chat": ChatController
}

settings = {
    "template": os.getcwd() + "/template"
}


if __name__ == '__main__':
    global redis_manager
    redis_manager = RedisManage()
    application = Application(handlers_mapping, settings=settings)
    application.listen(8888)
    application.run()
