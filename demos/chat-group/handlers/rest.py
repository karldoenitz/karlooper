# -*- coding: utf-8 -*-

from karlooper.config import get_global_conf
from karlooper.web.request import Request

__author__ = "karlvorndoenitz@gmail.com"


class MessageHandler(Request):
    def get(self):
        redis_manager = get_global_conf("redis")
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
        redis_manager = get_global_conf("redis")
        redis_manager.set_value([str(from_user)+":"+new_value])
        result = {
            "status": 0,
            "desc": "ok"
        }
        return self.response_as_json(result)
