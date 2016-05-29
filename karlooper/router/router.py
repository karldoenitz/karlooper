# -*-coding:utf-8-*-


class Router(object):
    def __init__(self, handles, url):
        self.__handlers = handles
        self.__url = url

    def get_handler(self):
        """
        :return: return a handler object
        """
        return self.__handlers.get(self.__url, None)
