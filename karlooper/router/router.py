# -*-coding:utf-8-*-
from karlooper.config import get_cli_data
from karlooper.web.statics import StaticHandler


class Router(object):
    def __init__(self, handles, url):
        self.__handlers = handles
        self.__url = url
        self.__is_static_enable = get_cli_data().get("static")
        self.__is_debug = get_cli_data().get("debug")

    def get_handler(self):
        """
        :return: return a handler object
        """
        handler = self.__handlers.get(self.__url, None)
        if self.__is_debug \
                and self.__is_static_enable \
                and (str(self.__is_debug).lower() == "true") \
                and (not handler) \
                and ("/static/" in self.__url):
            handler = StaticHandler
        return handler
