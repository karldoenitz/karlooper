# -*-encoding:utf-8-*-

import functools
from karlooper.web.request import Request
from redis_manage import RedisManage


def is_login(method):
    @functools.wraps(method)
    def _wrap(self, *args, **kwargs):
        if not self.get_security_cookie("user_id"):
            return self.redirect("/login")
        return method(self, *args, **kwargs)
    return _wrap


class BaseRestHandler(Request):
    def __handle(self):
        return self.process()

    def get(self):
        return self.__handle()

    def post(self):
        return self.__handle()

    def put(self):
        return self.__handle()
