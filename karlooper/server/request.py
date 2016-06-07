# -*-coding:utf-8-*-

import datetime
import json
import logging

from karlooper.config.config import ContentType
from karlooper.utils.security import DES
from karlooper.template import render

__author__ = 'karlvorndoenitz@gmail.com'


class Request(object):
    def __init__(self, http_data_dict, http_message, settings):
        """

        :param http_data_dict: converted http data, dict type
        :param http_message: http message, string type

        """
        self.__http_data = http_data_dict
        self.header = "ServerName: karlooper\r\n"
        self.__http_message = http_message
        self.logger = logging
        self.cookie_dict = self.__parse_cookie()
        self.param_dict = self.__parse_param()
        self.__settings = settings

    def __parse_cookie(self):
        """

        :return: a dict contain cookie or None or error

        """
        cookie_string = self.__http_data["header"].get("cookie", "")
        if not cookie_string:
            return {}
        try:
            cookie_dict = dict((cookie.split("=")[0], cookie.split("=")[1]) for cookie in cookie_string.split("; "))
            return cookie_dict
        except Exception, e:
            raise e

    def __parse_param(self):
        """

        :return: a dict contain params

        """
        url_param = self.__http_data["url"].split("?")[1] if "?" in self.__http_data["url"] else None
        if not url_param:
            url_param_dict = {}
        else:
            url_param_dict = dict((param.split("=")[0], param.split("=")[1]) for param in url_param.split("&"))
        content_type = self.get_header("content-type")
        http_body = self.__http_data.get("body", "")
        if content_type == ContentType.FORM and http_body:
            body_param = dict((param.split("=")[0], param.split("=")[1]) for param in http_body.split("&"))
        elif content_type == ContentType.JSON and http_body:
            body_param = eval(http_body)
        else:
            body_param = {}
        param = dict(url_param_dict, **body_param)
        return param

    def get_cookie(self, key, default=None):
        """

        :param key: cookie's key
        :param default: cookie's default value
        :return: cookie's value

        """
        return self.cookie_dict.get(key, default)

    def get_security_cookie(self, key, default=None):
        """

        :param key: cookie's key
        :param default: cookie's default value
        :return: cookie's value

        """
        cookie = self.get_cookie(key)
        if not cookie:
            return default
        des = DES()
        security_key = self.__settings.get("cookie", "1qaz2wsx3")
        des.input_key(security_key)
        return des.decode(cookie)

    def get_parameter(self, key, default=None):
        """

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        return self.param_dict.get(key, default)

    def get_header(self, key, default=None):
        """

        :param key: header data's key
        :param default: default value
        :return: value

        """
        header_data = self.__http_data["header"]
        return header_data.get(key, default)

    def set_cookie(self, key, value, expires_days=1, path="/"):
        """

        :param key: cookie's key
        :param value: cookie's value
        :param expires_days: cookie's expires days
        :param path: cookie's value path
        :return: None

        """
        key = str(key)
        value = str(value)
        now_time = datetime.datetime.now()
        expires_days = now_time + datetime.timedelta(days=expires_days)
        expires_days = expires_days.strftime("%a, %d %b %Y %H:%M:%S GMT")
        cookie_string = 'Set-Cookie: %s=%s; expires=%s; Path=%s' % (key, value, expires_days, path)
        self.header += "%s\r\n" % cookie_string

    def set_security_cookie(self, key, value, expires_days=1, path="/"):
        """

        :param key: cookie's key
        :param value: cookie's value
        :param expires_days: cookie's expires days
        :param path: cookie's value path
        :return: None

        """
        des = DES()
        security_key = self.__settings.get("cookie", "1qaz2wsx3")
        des.input_key(security_key)
        security_value = des.encode(value)
        self.set_cookie(key, security_value, expires_days, path)

    def set_header(self, header_dict):
        """

        :param header_dict: http header data dict type
        :return: None

        """
        for header_key in header_dict:
            self.header += "%s: %s\r\n" % (header_key, header_dict[header_key])

    def get_response_header(self):
        """

        :return: http message's header

        """
        return "\r\n" + self.header + "\r\n"

    def response_as_json(self, data):
        """

        :param data: the response data
        :return: json data

        """
        self.set_header({"Content-Type": "application/json"})
        return json.dumps(data, ensure_ascii=False)

    def render(self, template_path, **kwargs):
        root_path = self.__settings.get("template", ".")
        template_path = root_path + template_path
        return render(template_path, **kwargs)

    def get_http_request_message(self):
        return self.__http_message

    def get(self):
        pass

    def post(self):
        pass

    def put(self):
        pass

    def head(self):
        self.logger.info(self.__http_data.get("url", ""))
        return ""

    def options(self):
        pass

    def delete(self):
        pass

    def trace(self):
        return self.__http_message.split("\r\n\r\n") if "\r\n\r\n" in self.__http_message else ""

    def connect(self):
        pass
