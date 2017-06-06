# -*-coding:utf-8-*-

import datetime
import json
import logging
from urllib import unquote, unquote_plus

from karlooper.utils.http_utils import get_http_content_type
from karlooper.config.config import ContentType, COOKIE_SECURITY_DEFAULT_STRING, HttpStatus, HttpStatusMsg
from karlooper.escape import utf8
from karlooper.utils.encrypt import StrEncryption
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
        self.logger = logging.getLogger()
        self.cookie_dict = self.__parse_cookie()
        self.param_dict = self.__parse_param()
        self.__settings = settings
        self.__response_cookie = {}
        self.__response_header = {}
        self.__path_param = {}

    def __parse_cookie(self):
        """parse cookie string to cookie dict

        :return: a dict contain cookie or None or error

        """
        cookie_string = self.__http_data["header"].get("cookie", "")
        if not cookie_string:
            return {}
        try:
            cookie_dict = dict((cookie.split("=")[0], cookie.split("=", 1)[1]) for cookie in cookie_string.split("; "))
            return cookie_dict
        except Exception, e:
            raise e

    def __parse_param(self):
        """parse http message to get the param dict

        :return: a dict contain params

        """
        url_param = self.__http_data["url"].split("?")[1] if "?" in self.__http_data["url"] else None
        if not url_param:
            url_param_dict = {}
        else:
            url_param_dict = dict((param.split("=")[0], param.split("=")[1]) for param in url_param.split("&"))
        content_type = self.get_header("content-type")
        content_type = get_http_content_type(content_type)
        http_body = self.__http_data.get("body", "")
        if content_type == ContentType.FORM and http_body:
            body_param = dict((param.split("=")[0], param.split("=")[1]) for param in http_body.split("&"))
        elif content_type == ContentType.JSON and http_body:
            try:
                body_param = json.loads(http_body)
            except Exception, e:
                self.logger.warning("parse json error: %s" % str(e))
                body_param = eval(http_body)
        else:
            body_param = {}
        param = dict(url_param_dict, **body_param)
        return param

    def set_path_param(self, path_param_dict):
        """ set the param in url

        :param path_param_dict: param parsed from url
        :return: None

        """
        self.__path_param = path_param_dict

    def get_path_param(self, key, default=None):
        """ get param in url with key

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        return self.__path_param.get(key, default)

    def get_path_param_int(self, key, default=None):
        """ get param's int value in url with key

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        value = self.__path_param.get(key, default)
        if value is None:
            return None
        return int(value)

    def get_path_param_str(self, key, default=None):
        """ get param's str value in url with key

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        value = self.__path_param.get(key, default)
        if value is None:
            return None
        return str(value)

    def get_path_param_boolean(self, key, default=None):
        """ get param's boolean value in url with key

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        value = self.__path_param.get(key, default)
        if value is None:
            return None
        return bool(value)

    def get_path_param_float(self, key, default=None):
        """ get param's float value in url with key

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        value = self.__path_param.get(key, default)
        if value is None:
            return None
        return float(value)

    def get_cookie(self, key, default=None):
        """get cookie's value with defined key

        :param key: cookie's key
        :param default: cookie's default value
        :return: cookie's value

        """
        return self.cookie_dict.get(key, default)

    def get_security_cookie(self, key, default=None):
        """get security cookie's value with decode

        :param key: cookie's key
        :param default: cookie's default value
        :return: cookie's value

        """
        cookie = self.get_cookie(key)
        if not cookie:
            return default
        des = StrEncryption()
        security_key = self.__settings.get("cookie", COOKIE_SECURITY_DEFAULT_STRING)
        des.input_key(security_key)
        return des.decode(cookie)

    def get_parameter(self, key, default=None):
        """get parameter's value with the given key,
        this method can get value in http body or url,
        content-type support: application/json and application/x-www-form-urlencoded

        :param key: param's key
        :param default: param's default value
        :return: param's value

        """
        return self.param_dict.get(key, default)

    def decode_parameter(self, key, default=None):
        """decode parameter with defined key

        :param key: value's key
        :param default: default value
        :return: decoded parameter

        """
        parameter = self.get_parameter(key)
        if not parameter:
            return default
        return unquote(parameter)

    def decode_parameter_plus(self, key, default=None):
        """decode parameter with defined key, include decode plus symbol to space

        :param key: value's key
        :param default: default value
        :return: decoded parameter

        """
        parameter = self.get_parameter(key)
        if not parameter:
            return default
        return unquote_plus(parameter)

    def get_header(self, key, default=None):
        """get http header's value with defined key

        :param key: header data's key
        :param default: default value
        :return: value

        """
        header_data = self.__http_data["header"]
        return header_data.get(key, default)

    def __parse_cookie_dict_to_string(self):
        for cookie in self.__response_cookie.values():
            if cookie.get("domain"):
                cookie_format = 'Set-Cookie: %(key)s=%(value)s; expires=%(expires)s; Path=%(path)s; Domain=%(domain)s'
            else:
                cookie_format = 'Set-Cookie: %(key)s=%(value)s; expires=%(expires)s; Path=%(path)s'
            cookie_string = cookie_format % cookie
            self.header += "%s\r\n" % cookie_string

    def generate_expire_date(self, expires_days):
        """get expire date

        :param expires_days: expires days, int type
        :return: http expires days, string type

        """
        now_time = datetime.datetime.now()
        expires_time = now_time + datetime.timedelta(days=expires_days)
        expires_time = expires_time.strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.logger.info(expires_time)
        return expires_time

    def get_now_time(self):
        now_time = datetime.datetime.now().strftime("%a, %d %b %Y %H:%M:%S GMT")
        self.logger.info(now_time)
        return now_time

    def get_request_url(self):
        """get request url

        :return: request url

        """
        return self.__http_data.get("url", "")

    def set_cookie(self, key, value, expires_days=1, path="/", domain=None):
        """set cookie's value

        :param key: cookie's key
        :param value: cookie's value
        :param expires_days: cookie's expires days
        :param path: cookie's value path
        :param domain: cookie's domain
        :return: None

        """
        key = str(key)
        value = str(value)
        expires_days = self.generate_expire_date(expires_days)
        cookie_dict = {
            "key": key,
            "value": value,
            "expires": expires_days,
            "path": path,
            "domain": domain
        }
        if domain:
            cookie_dict["Domain"] = domain
        self.__response_cookie[key] = cookie_dict

    def set_security_cookie(self, key, value, expires_days=1, path="/", domain=None):
        """set security cookie's value

        :param key: cookie's key
        :param value: cookie's value
        :param expires_days: cookie's expires days
        :param path: cookie's value path
        :param domain: cookie's domain
        :return: None

        """
        des = StrEncryption()
        security_key = self.__settings.get("cookie", COOKIE_SECURITY_DEFAULT_STRING)
        des.input_key(security_key)
        security_value = des.encode(value)
        self.set_cookie(key, security_value, expires_days, path, domain)

    def clear_cookie(self, key, path="/", domain=None):
        """clear cookie with defined key

        :param key: clear cookie by key
        :param path: cookie's path
        :param domain: cookie's domain
        :return: None

        """
        self.set_cookie(key, "", 0, path, domain)

    def clear_all_cookie(self, path="/", domain=None):
        """clear all cookie

        :param path: cookie's path
        :param domain: cookie's domain
        :return: None

        """
        for key in self.cookie_dict:
            self.clear_cookie(key, path, domain)

    def __parse_header_dict_to_string(self):
        for header_key in self.__response_header:
            self.header += "%s: %s\r\n" % (header_key, self.__response_header[header_key])

    def set_header(self, header_dict):
        """set header data in http message

        :param header_dict: http header data dict type
        :return: None

        """
        for header_key in header_dict:
            self.__response_header[header_key] = header_dict[header_key]

    def clear_header(self, name):
        """clear headers' data in http response message

        :param name: header's name
        :return:

        """
        self.__response_header.pop(name)

    def get_response_header(self):
        """get http response header

        :return: http message's header

        """
        self.__parse_header_dict_to_string()
        self.__parse_cookie_dict_to_string()
        return "\r\n" + self.header + "\r\n"

    def response_as_json(self, data):
        """decorate data to http json data

        :param data: the response data
        :return: json data

        """
        self.set_header({"Content-Type": "application/json"})
        response = json.dumps(data, ensure_ascii=False)
        return utf8(response), HttpStatus.SUCCESS, HttpStatusMsg.SUCCESS

    def http_response(self, data):
        """decorate data to http response data

        :param data: http response data
        :return: a tuple contains http message, status, status message

        """
        self.logger.info("response data:", data)
        return data, HttpStatus.SUCCESS, HttpStatusMsg.SUCCESS

    def render(self, template_path, **kwargs):
        """render a template

        :param template_path: template's relative path
        :param kwargs: params used in template
        :return: a tuple contains http message, status, status message

        """
        root_path = self.__settings.get("template", ".")
        template_path = root_path + template_path
        return render(template_path, **kwargs), HttpStatus.SUCCESS, HttpStatusMsg.SUCCESS

    def redirect(self, url, status=HttpStatus.REDIRECT):
        """redirect to defined url

        :param url: redirect url
        :param status: http status
        :return: a tuple contains http message, status, status message

        """
        self.set_header({
            "Location": url,
        })
        return "", status, HttpStatusMsg.REDIRECT

    def get_http_request_message(self):
        """get request message

        :return: self http message

        """
        return self.__http_message

    def get(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def post(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def put(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def head(self):
        self.logger.info(self.__http_data.get("url", ""))
        return ""

    def options(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def delete(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def trace(self):
        return self.__http_message.split("\r\n\r\n") if "\r\n\r\n" in self.__http_message else ""

    def connect(self):
        self.logger.error(HttpStatusMsg.METHOD_NOT_ALLOWED)
        return "405", HttpStatus.METHOD_NOT_ALLOWED, HttpStatusMsg.METHOD_NOT_ALLOWED

    def before_request(self):
        pass

    def teardown_request(self):
        pass
