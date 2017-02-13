# -*-coding:utf-8-*-
from karlooper.config import get_cli_data
from karlooper.web.statics import StaticHandler


class PathParam(object):
    status = False
    value = {}


class Router(object):
    def __init__(self, handles, url):
        self.__handlers = handles
        self.__url = url
        self.__is_static_enable = get_cli_data().get("static")
        self.__is_debug = get_cli_data().get("debug")

    def get_handler(self):
        """
        I will add url regex parse in the future
        :return: return a handler object
        """
        path_param = PathParam()
        handler = self.__handlers.get(self.__url, None)
        if handler is None:
            url_list = self.__handlers.keys()
            for url in url_list:
                path_param = self.get_path_param(url)
                if path_param.status:
                    handler = self.__handlers.get(url, None)
                    return handler, path_param
        if handler is None \
                and self.__is_debug \
                and self.__is_static_enable \
                and (str(self.__is_debug).lower() == "true") \
                and (not handler) \
                and ("/static/" in self.__url):
            handler = StaticHandler
        return handler, path_param

    def get_path_param(self, path):
        """ parse param in url

        :param path: url rule
        :return: a PathParam object

        """

        path_attr_list = path.split("/")
        url_attr_list = self.__url.split("/")
        path_param = PathParam()
        if len(path_attr_list) != len(url_attr_list):
            path_param.status = False
            return path_param
        for index in xrange(len(path_attr_list)):
            path_attr = path_attr_list[index]
            url_attr = url_attr_list[index]
            if ("{" not in path_attr or "}" not in path_attr) and path_attr != url_attr:
                path_param.status = False
                return path_param
            if "{" in path_attr and "}" in path_attr:
                path_value_key = path_attr.replace("{", "").replace("}", "")
                path_param.status = True
                path_param.value[path_value_key] = url_attr
        return path_param
