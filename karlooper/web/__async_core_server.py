# -*-coding:utf-8-*-
"""

__async_core_server
~~~~~~~~~~~~~~~~~~

introduction
use python asyncore model to implement a async http server

Usage
=====
>>> EchoServer('0.0.0.0', port=8080, handlers={}, settings={})
>>> asyncore.loop()

"""

import logging
import asyncore
import socket
from karlooper.http_parser.http_parser import HttpParser
from karlooper.config.config import SOCKET_RECEIVE_SIZE, CLIENT_CONNECT_TO_SERVER_NUM
from karlooper.utils import PY3

if PY3:
    unicode = str


class EchoHandler(asyncore.dispatcher_with_send):
    def __init__(self, async_socket, handlers, settings):
        """async echo handler based on asyncore.dispatcher_with_send

        :param async_socket: the socket object
        :param handlers: handlers mapping
        :param settings: settings config

        """
        self.logger = logging.getLogger()
        self.__handlers = handlers
        self.__settings = settings
        asyncore.dispatcher_with_send.__init__(self, sock=async_socket)

    def handle_read(self):
        try:
            if PY3:
                data = self.recv(SOCKET_RECEIVE_SIZE).decode("utf-8")
            else:
                data = self.recv(SOCKET_RECEIVE_SIZE)
            http_parser = HttpParser(data=data, handlers=self.__handlers, settings=self.__settings)
            response_data = http_parser.parse()
            while not (isinstance(response_data, str) or isinstance(response_data, unicode)):
                response_data = http_parser.parse()
            if PY3:
                response_data = response_data.encode('utf-8')
            self.send(response_data)
        except Exception as e:
            self.logger.info("echo handler error: %s" % str(e))


class EchoServer(asyncore.dispatcher):
    def __init__(self, host, port, handlers, settings):
        """async echo server based on asyncore.dispatcher

        :param host: http host
        :param port: http port
        :param handlers: handlers mapping
        :param settings: settings config

        """
        self.__handlers = handlers
        self.__settings = settings
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(CLIENT_CONNECT_TO_SERVER_NUM)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, address = pair
            EchoHandler(sock, self.__handlers, self.__settings)
