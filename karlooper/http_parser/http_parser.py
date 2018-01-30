# -*-coding:utf-8-*-

import datetime
import logging
from karlooper.escape import utf8
from karlooper.router.router import Router
from karlooper.config.config import ContentType, RESPONSE_HEAD_MESSAGE
from karlooper.web.response import HTTPResponse404, HTTPResponse500

__author__ = 'karlvorndoenitz@gmail.com'


class HttpParser(object):
    def __init__(self, data, handlers, settings=None):
        """

        :param data: the request data from socket
        :param settings: url settings

        """
        self.logger = logging.getLogger()
        self.response_header = RESPONSE_HEAD_MESSAGE
        self.data = data
        self.settings = settings if settings else {}
        self.handlers = handlers
        self.host = self.settings.get("host", "Karlooper")

    def parse(self):
        return self.__parse_data()

    def __parse_data(self):
        """

        parse http request data to dict and get handler's response data

        :return: http response data

        """
        http_message = self.data.split("\r\n\r\n")
        http_request_head = http_message[0]
        http_request_line = http_request_head.split("\r\n")[0].split(" ")
        http_method = http_request_line[0].lower()
        http_url = http_request_line[1]
        http_version = http_request_line[2]
        http_head_list = http_request_head.split("\r\n")[1:]
        if "" in http_head_list:
            http_head_list.remove("")
        header = dict((header.split(": ")[0].lower(), header.split(": ")[1]) for header in http_head_list)
        http_body = http_message[1] if len(http_message) > 1 else None
        http_message_dict = dict({})
        http_message_dict["url"] = http_url
        http_message_dict["method"] = http_method
        http_message_dict["version"] = http_version
        http_message_dict["header"] = header
        http_message_dict["body"] = http_body
        now = datetime.datetime.now()
        now_time = now.strftime("%a, %d %b %Y %H:%M:%S GMT")
        status = dict({})
        status["date"] = now_time
        status["host"] = self.host
        url = http_url.split("?")[0]
        handler = Router(self.handlers, url).get_handler()
        path_param = handler[1]
        handler = handler[0]
        if not handler:
            data = HTTPResponse404(**self.settings).data()
            status["status"] = HTTPResponse404.status
            status["content_type"] = ContentType.HTML
            status["content_length"] = len(utf8(data))
            status["status_msg"] = HTTPResponse404.message
        else:
            try:
                handler_init = handler(http_message_dict, self.data, self.settings)
                if path_param.status:
                    handler_init.set_path_param(path_param.value)
                handler_init.before_request()
                pro_function = getattr(handler_init, http_method)
                data = pro_function()
                if isinstance(data, type):
                    return data
                try:
                    handler_init_k = data[-1]
                    http_response_header = handler_init_k.get_response_header()
                except Exception as e:
                    self.logger.info("static handler response: %s", str(e))
                    http_response_header = handler_init.get_response_header()
                self.response_header = self.response_header.replace("\r\n\r\n", http_response_header)
                status["status"] = data[1]
                status["status_msg"] = data[2]
                data = data[0]
                handler_init.teardown_request()
            except Exception as e:
                status["status"] = HTTPResponse500.status
                status["status_msg"] = HTTPResponse500.message
                data = HTTPResponse500(**self.settings).data() or str(e)
            status["content_length"] = len(utf8(data))
        response_data = self.response_header % status + data
        return response_data
