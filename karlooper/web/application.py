# -*-coding:utf-8-*-

import socket
import select
import platform
from karlooper.logger.logger import init_logger
from karlooper.web.__async_core_server import EchoServer, asyncore
from karlooper.http_parser.http_parser import HttpParser
from karlooper.config import get_cli_data, set_cli_data
from karlooper.config.config import SOCKET_RECEIVE_SIZE, DEFAULT_PORT, CLIENT_CONNECT_TO_SERVER_NUM

__author__ = 'karlvorndoenitz@gmail.com'


class Application(object):
    def __init__(self, handlers, settings=None, **kwargs):
        """

        :param handlers: handlers mapping, dict type
        :param settings: settings mapping, dict type
        :param kwargs: options

        """
        self.settings = settings
        self.handlers = handlers
        set_cli_data(self.settings)
        set_cli_data(kwargs)
        cli_data = get_cli_data()
        self.port = int(cli_data.get("port", DEFAULT_PORT))
        self.logger = init_logger()
        self.EOL1 = b'\n\n'
        self.EOL2 = b'\n\r\n'
        self.response = ""

    def listen(self, port):
        """listen port

        :param port: port that application listened
        :return: None

        """
        self.port = int(port)

    def __run_epoll(self):
        """
        run the application use epoll
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(CLIENT_CONNECT_TO_SERVER_NUM)  # the number of client that connect to server
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
                            requests[fileno] += connections[fileno].recv(SOCKET_RECEIVE_SIZE)
                            if self.EOL1 in requests[fileno] or self.EOL2 in requests[fileno]:  # if http message
                                request_data = requests[fileno][:-2] \
                                    if requests[fileno].endswith("\r\n") else requests[fileno]
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
            try:
                request_data = cl_socket.recv(SOCKET_RECEIVE_SIZE)
                if request_data:
                    request_data = request_data[:-2] if request_data.endswith("\r\n") else request_data
                    data = HttpParser(request_data, handlers=self.handlers, settings=self.settings).parse()
                    cl_socket.send(data)
                else:
                    cl_socket.shutdown(socket.SHUT_WR)
                    cl_socket.close()
                    break
            except Exception, e:
                self.logger.error(e)

    def __run_kqueue(self):
        """
        run the server use kqueue
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(("0.0.0.0", self.port))
        s.listen(CLIENT_CONNECT_TO_SERVER_NUM)
        kq = select.kqueue()
        kevent = select.kevent(
            s.fileno(),
            filter=select.KQ_FILTER_READ,
            flags=select.KQ_EV_ADD | select.KQ_EV_ENABLE
        )

        while True:
            receive_events = kq.control([kevent], 1, None)
            for event in receive_events:
                if event.filter == select.KQ_FILTER_READ:
                    cl, _ = s.accept()
                    self.__handle_connection(cl)

    def __run_async_io(self):
        """
        run server use asyncore
        """
        EchoServer('0.0.0.0', self.port, self.handlers, self.settings)
        asyncore.loop()

    def __kqueue_mode(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(CLIENT_CONNECT_TO_SERVER_NUM)
        kq = select.kqueue()
        conn_list = {}
        index = 1
        events = [select.kevent(server_socket.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)]
        while True:
            try:
                eventlist = kq.control(events, 1)
            except select.error as e:
                break
            if eventlist:
                for each in eventlist:
                    if each.ident == server_socket.fileno():
                        conn, addr = server_socket.accept()
                        conn_list[index] = conn
                        events.append(
                            select.kevent(
                                conn_list[index].fileno(),
                                select.KQ_FILTER_READ,
                                select.KQ_EV_ADD,
                                udata=index
                            )
                        )
                        index += 1
                    else:
                        try:
                            if each.udata >= 1 and each.flags == select.KQ_EV_ADD \
                                    and each.filter == select.KQ_FILTER_READ:
                                conn = conn_list[each.udata]
                                request_data = conn.recv(SOCKET_RECEIVE_SIZE)
                                if request_data:
                                    request_data = request_data[:-2] if request_data.endswith("\r\n") else request_data
                                    data = HttpParser(
                                        request_data,
                                        handlers=self.handlers,
                                        settings=self.settings
                                    ).parse()
                                    conn.send(data)
                                else:
                                    conn.close()
                        except Exception, e:
                            self.logger.error(e)
                        finally:
                            conn.close()
        server_socket.close()

    def run(self):
        """
        run the web server
        """
        print "server run on port: %d" % self.port
        self.logger.info("server run on port: %d" % self.port)
        system_name = platform.system()
        kernel_version = platform.release()
        if system_name == "Linux" and kernel_version >= "2.5.44":
            self.__run_epoll()
        elif system_name == "Darwin" and kernel_version >= "13.0.0":
            # self.__run_kqueue()
            self.__kqueue_mode()
        else:
            self.__run_async_io()
