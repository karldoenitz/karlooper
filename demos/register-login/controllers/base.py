# -*-encoding:utf-8-*-

import functools
from karlooper.web.request import Request
from redis_manage import RedisManage


def is_login(method):
    @functools.wraps(method)
    def _wrap(self, *args, **kwargs):
        print(self.get_http_request_message())
        if not self.get_security_cookie("user_id"):
            return self.redirect("/login")
        return method(self, *args, **kwargs)
    return _wrap


class Status(object):
    SUCCESS = (0, "OK")
    USER_EXIST = (1, "user is existed")
    USER_NOT_EXIST = (2, "user is not existed")
    PSW_ERR = (3, "password error")


class BaseRestHandler(Request):
    redis_manager = RedisManage()

    def __handle(self):
        return self.process()

    def get(self):
        return self.__handle()

    def post(self):
        return self.__handle()

    def put(self):
        return self.__handle()

    def result(self, status, **kwargs):
        result = {
            "status": status[0],
            "message": status[1],
            "data": kwargs
        }
        return self.response_as_json(result)
