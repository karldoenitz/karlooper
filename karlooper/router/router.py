# -*-coding:utf-8-*-
from karlooper.config import get_cli_data
from karlooper.web.statics import StaticHandler


class Router(object):
    def __init__(self, handles, url):
        self.__handlers = handles
        self.__url = url
        self.__is_static_enable = get_cli_data().get("static")

    def get_handler(self):
        """
        :return: return a handler object
        """
        handler = self.__handlers.get(self.__url, None)
        if (not handler) and self.__is_static_enable and ("/static/" in self.__url):
            handler = StaticHandler
        return handler
