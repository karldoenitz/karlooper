# -*-coding:utf-8-*-

import socket
import select
from karlooper.logger.logger import init_logger
from karlooper.web.__async_core_server import EchoServer, asyncore
from karlooper.web.http_connection import HttpConnection
from karlooper.web.http_io_buffer import HttpIOBuffer
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
            http_connection = HttpConnection()
            http_io_buffer = HttpIOBuffer()
            while True:
                events = epoll.poll(1)
                for fileno, event in events:
                    try:
                        if fileno == server_socket.fileno():  # if request come
                            connection, address = server_socket.accept()  # waiting income connection
                            connection.setblocking(0)  # none block
                            epoll.register(connection.fileno(), select.EPOLLIN)  # register socket read event to epoll
                            http_connection.add_connection(connection.fileno(), connection)
                            http_io_buffer.add_request(connection.fileno(), b'')
                            http_io_buffer.add_response(connection.fileno(), self.response)
                        elif event & select.EPOLLIN:  # when data in os's read buffer area
                            http_request_buffer = http_connection.get_connection(fileno).recv(SOCKET_RECEIVE_SIZE)
                            http_io_buffer.add_request(
                                fileno,
                                http_io_buffer.get_request(fileno) + http_request_buffer
                            )
                            if self.EOL1 in http_io_buffer.get_request(fileno) \
                                    or self.EOL2 in http_io_buffer.get_request(fileno):
                                request_data = http_io_buffer.get_request(fileno)[:-2] \
                                    if http_io_buffer.get_request(fileno).endswith("\r\n") \
                                    else http_io_buffer.get_request(fileno)
                                data = HttpParser(request_data, self.handlers, settings=self.settings).parse()
                                http_io_buffer.add_response(
                                    fileno,
                                    http_io_buffer.get_response(fileno) + data
                                )
                                epoll.modify(fileno, select.EPOLLOUT)  # change file number to epoll out mode
                        elif event & select.EPOLLOUT:  # if out mode
                            bytes_written = http_connection.get_connection(fileno).send(
                                http_io_buffer.get_response(fileno)
                            )
                            http_io_buffer.add_response(fileno, http_io_buffer.get_response(fileno)[bytes_written:])
                            if len(http_io_buffer.get_response(fileno)) == 0:  # if file sent
                                epoll.modify(fileno, 0)  # change file number to hup mode
                                http_connection.get_connection(fileno).shutdown(socket.SHUT_RDWR)
                                epoll.modify(fileno, select.EPOLLHUP)
                        elif event & select.EPOLLHUP:  # if message sent and file number in epoll is hup
                            epoll.unregister(fileno)  # remove file number from epoll
                            http_connection.get_connection(fileno).close()  # close connection
                            http_connection.remove_connection(fileno)  # delete connection from connections dict
                    except Exception, e:
                        self.logger.error("error in __run_epoll", e)
                        continue
        finally:
            epoll.unregister(server_socket.fileno())
            epoll.close()
            server_socket.close()

    def __run_kqueue(self):
        """
        run server use kqueue
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(CLIENT_CONNECT_TO_SERVER_NUM)
        kq = select.kqueue()
        http_connection = HttpConnection()
        index = 1
        events = [select.kevent(server_socket.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD)]
        while True:
            try:
                event_list = kq.control(events, 1)
            except select.error as e:
                self.logger.error("error in __run_kqueue", e)
                break
            if event_list:
                for each in event_list:
                    if each.ident == server_socket.fileno():
                        index += 1
                        conn, addr = server_socket.accept()
                        http_connection.add_connection(index, conn)
                        events.append(
                            select.kevent(
                                http_connection.get_connection(index).fileno(),
                                select.KQ_FILTER_READ,
                                select.KQ_EV_ADD,
                                udata=index
                            )
                        )
                    else:
                        try:
                            if each.udata >= 1 and each.flags == select.KQ_EV_ADD \
                                    and each.filter == select.KQ_FILTER_READ:
                                conn = http_connection.get_connection(each.udata)
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
                            self.logger.error("error in __run_kqueue event list", e)
                        finally:
                            events.remove(select.kevent(
                                http_connection.get_connection(each.udata).fileno(),
                                select.KQ_FILTER_READ,
                                select.KQ_EV_ADD,
                                udata=each.udata)
                            )
                            http_connection.remove_connection(each.udata)
                            conn.close()
        server_socket.close()

    def __run_poll(self):
        """
        run server use poll, I will modify __run_poll and __run_epoll in the future
        """
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', self.port))
        server_socket.listen(CLIENT_CONNECT_TO_SERVER_NUM)  # the number of client that connect to server
        server_socket.setblocking(0)  # set 0 not block other block
        server_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        poll = select.poll()
        poll.register(server_socket.fileno(), select.POLLIN)
        try:
            http_connection = HttpConnection()
            http_io_buffer = HttpIOBuffer()
            while True:
                events = poll.poll(1)
                for fileno, event in events:
                    try:
                        if fileno == server_socket.fileno():  # if request come
                            connection, address = server_socket.accept()  # waiting income connection
                            connection.setblocking(0)  # none block
                            poll.register(connection.fileno(), select.POLLIN)  # register socket read event to poll
                            http_connection.add_connection(connection.fileno(), connection)
                            http_io_buffer.add_request(connection.fileno(), b'')
                            http_io_buffer.add_response(connection.fileno(), self.response)
                        elif event & select.POLLIN:  # when data in os's read buffer area
                            http_request_buffer = http_connection.get_connection(fileno).recv(SOCKET_RECEIVE_SIZE)
                            http_io_buffer.add_request(
                                fileno,
                                http_io_buffer.get_request(fileno) + http_request_buffer
                            )
                            if self.EOL1 in http_io_buffer.get_request(fileno) \
                                    or self.EOL2 in http_io_buffer.get_request(fileno):
                                request_data = http_io_buffer.get_request(fileno)[:-2] \
                                    if http_io_buffer.get_request(fileno).endswith("\r\n") \
                                    else http_io_buffer.get_request(fileno)
                                data = HttpParser(request_data, self.handlers, settings=self.settings).parse()
                                http_io_buffer.add_response(
                                    fileno,
                                    http_io_buffer.get_response(fileno) + data
                                )
                                poll.modify(fileno, select.POLLOUT)  # change file number to poll out mode
                        elif event & select.POLLOUT:  # if out mode
                            bytes_written = http_connection.get_connection(fileno).send(
                                http_io_buffer.get_response(fileno)
                            )
                            http_io_buffer.add_response(fileno, http_io_buffer.get_response(fileno)[bytes_written:])
                            if len(http_io_buffer.get_response(fileno)) == 0:  # if file sent
                                poll.modify(fileno, 0)  # change file number to hup mode
                                http_connection.get_connection(fileno).shutdown(socket.SHUT_RDWR)
                                poll.modify(fileno, select.POLLHUP)
                        elif event & select.POLLHUP:  # if message sent and file number in poll is hup
                            poll.unregister(fileno)  # remove file number from poll
                            http_connection.get_connection(fileno).close()  # close connection
                            http_connection.remove_connection(fileno)  # delete connection from connections dict
                    except Exception, e:
                        self.logger.error("error in __run_poll", e)
                        continue
        finally:
            poll.unregister(server_socket.fileno())
            poll.close()
            server_socket.close()

    def __run_async_io(self):
        """
        run server use asyncore
        """
        EchoServer('0.0.0.0', self.port, self.handlers, self.settings)
        asyncore.loop()

    def run(self):
        """
        run the web server
        """
        print "server run on port: %d" % self.port
        self.logger.info("server run on port: %d" % self.port)
        if hasattr(select, "epoll"):
            print "run with epoll"
            self.logger.info("run with epoll")
            self.__run_epoll()
        elif hasattr(select, "kqueue"):
            print "run with kqueue"
            self.logger.info("run with kqueue")
            self.__run_kqueue()
        elif hasattr(select, "poll"):
            print "run with poll"
            self.logger.info("run with poll")
            self.__run_poll()
        else:
            print "run with asyncore"
            self.logger.info("run with asyncore")
            self.__run_async_io()
