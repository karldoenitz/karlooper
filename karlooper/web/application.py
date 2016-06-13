# -*-coding:utf-8-*-

import socket
import select
import logging
import platform
from karlooper.web.__async_core_server import EchoServer, asyncore
from karlooper.http_parser.http_parser import HttpParser

__author__ = 'karlvorndoenitz@gmail.com'


class Application(object):
    def __init__(self, port, handlers, settings=None):
        self.port = port
        self.logger = logging
        self.EOL1 = b'\n\n'
        self.EOL2 = b'\n\r\n'
        self.response = ""
        self.settings = settings
        self.handlers = handlers

    def __run_epoll(self):
        """
        run the application use epoll
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(1)  # the number of client that connect to server
        server_socket.setblocking(0)  # set 0 not block other block
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        epoll = select.epoll()
        epoll.register(server_socket.fileno(), select.EPOLLIN)
        try:
            connections = {}
            requests = {}
            responses = {}
            while True:
                events = epoll.poll(1)
                for fileno, event in events:
                    try:
                        if fileno == server_socket.fileno():  # if request come
                            connection, address = server_socket.accept()  # waiting income connection
                            connection.setblocking(0)  # none block
                            epoll.register(connection.fileno(), select.EPOLLIN)  # register socket read event to epoll
                            connections[connection.fileno()] = connection  # add connection to connections dict
                            requests[connection.fileno()] = b''
                            responses[connection.fileno()] = self.response  # write data to responses dict
                        elif event & select.EPOLLIN:  # when data in os's read buffer area
                            requests[fileno] += connections[fileno].recv(1024)  # read data from connections
                            if self.EOL1 in requests[fileno] or self.EOL2 in requests[fileno]:  # if http message
                                request_data = requests[fileno][:-2]
                                data = HttpParser(request_data, self.handlers, settings=self.settings).parse()
                                responses[fileno] += data
                                epoll.modify(fileno, select.EPOLLOUT)  # change file number to epoll out mode
                        elif event & select.EPOLLOUT:  # if out mode
                            byteswritten = connections[fileno].send(responses[fileno])  # write to os's write buffer
                            responses[fileno] = responses[fileno][byteswritten:]  # get http response message
                            if len(responses[fileno]) == 0:  # if file sent
                                epoll.modify(fileno, 0)  # change file number to hup mode
                                connections[fileno].shutdown(socket.SHUT_RDWR)  # set socket read and write mod shutdown
                        elif event & select.EPOLLHUP:  # if message sent and file number in epoll is hup
                            epoll.unregister(fileno)  # remove file number from epoll
                            connections[fileno].close()  # close connection
                            del connections[fileno]  # delete connection from connections dict
                    except Exception, e:
                        self.logger.error(e)
                        continue
        finally:
            epoll.unregister(server_socket.fileno())
            epoll.close()
            server_socket.close()

    def __handle_connection(self, cl_socket):
        """

        :param cl_socket: client socket
        :return: None

        """
        while True:
            request_data = cl_socket.recv(1024)
            if request_data:
                data = HttpParser(request_data, handlers=self.handlers, settings=self.settings).parse()
                cl_socket.send(data)
            else:
                cl_socket.shutdown(socket.SHUT_WR)
                cl_socket.close()
                break

    def __run_kqueue(self):
        """
        run the server use kqueue
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(10)
        kq = select.kqueue()
        kevent = select.kevent(
            s.fileno(),
            filter=select.KQ_FILTER_READ,
            flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE
        )

        while True:
            revents = kq.control([kevent], 1, None)
            for event in revents:
                if event.filter == select.KQ_FILTER_READ:
                    cl, _ = s.accept()
                    self.__handle_connection(cl)

    def __run_async_io(self):
        """
        run server use asyncore
        """
        EchoServer('0.0.0.0', self.port, self.handlers, self.settings)
        asyncore.loop()

    def run(self):
        system_name = platform.system()
        if system_name == "Linux":
            self.__run_epoll()
        elif system_name == "Darwin":
            self.__run_kqueue()
        else:
            self.__run_async_io()
