# -*-coding:utf-8-*-
"""

application
~~~~~~~~~~~

Use this model to initialize web application.

Usage
=====
>>> from karlooper.web import IOModel
>>> from karlooper.web.application import Application
>>> application = Application(handlers={}, settings={}, port=8080, log_conf="./config.log")
>>> application.run(io_model=IOModel.POLL)
server run on port: 8080
run with poll

>>> application = Application(handlers={}, settings={}, log_conf="./config.log")
>>> application.listen(8000)
>>> application.run(io_model=IOModel.POLL)
server run on port: 8000
run with poll

"""

import socket
import select
from karlooper.logger.logger import init_logger
from karlooper.web import IOModel
from karlooper.web.__async_core_server import EchoServer, asyncore
from karlooper.web.http_connection import HttpConnection
from karlooper.web.http_io_buffer import HttpIOBuffer
from karlooper.web.http_io_routine_pool import HttpIORoutinePool
from karlooper.http_parser.http_parser import HttpParser
from karlooper.config import get_cli_data, set_cli_data
from karlooper.config.config import SOCKET_RECEIVE_SIZE, DEFAULT_PORT, CLIENT_CONNECT_TO_SERVER_NUM
from karlooper.utils import PY3

if PY3:
    unicode = str

__author__ = 'karlvorndoenitz@gmail.com'


class Application(object):
    def __init__(self, handlers, settings=None, **kwargs):
        """

        :param handlers: handlers mapping, dict type
        :param settings: settings mapping, dict type
        :param kwargs: options

        """
        self.handlers = handlers
        set_cli_data(settings)
        set_cli_data(kwargs)
        cli_data = get_cli_data()
        self.settings = cli_data
        self.port = int(cli_data.get("port", DEFAULT_PORT))
        log_conf = self.settings.get("log_conf", None) if self.settings else kwargs.get("log_conf", None)
        self.logger = init_logger(config_path=log_conf)
        self.EOL1 = '\n\n'
        self.EOL2 = '\n\r\n'
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
            http_io_routine_pool = HttpIORoutinePool()
            events_buf = []
            while True:
                events = epoll.poll(1) + events_buf
                events_buf = []
                for fileno, event in events:
                    try:
                        if fileno == server_socket.fileno():  # if request come
                            connection, address = server_socket.accept()  # waiting income connection
                            connection.setblocking(0)  # none block
                            epoll.register(connection.fileno(), select.EPOLLIN)  # register socket read event to epoll
                            http_connection.add_connection(connection.fileno(), connection)
                            http_io_buffer.add_request(connection.fileno(), '')
                            http_io_buffer.add_response(connection.fileno(), self.response)
                        elif event & select.EPOLLIN:  # when data in os's read buffer area
                            http_parser = http_io_routine_pool.get(file_no=fileno)
                            if http_parser:
                                data = http_parser.parse()
                                if isinstance(data, str) or isinstance(data, unicode):
                                    http_io_buffer.add_response(
                                        fileno,
                                        http_io_buffer.get_response(fileno) + data
                                    )
                                    epoll.modify(fileno, select.EPOLLOUT)  # change file number to epoll out mode
                                    http_io_routine_pool.remove(fileno)
                                else:  # if coroutine
                                    http_io_routine_pool.add(fileno, http_parser)
                                    events_buf.append((fileno, event))
                            else:
                                if PY3:
                                    http_request_buffer = http_connection.get_connection(fileno).recv(
                                        SOCKET_RECEIVE_SIZE).decode("utf-8")
                                else:
                                    http_request_buffer = http_connection.get_connection(fileno).recv(
                                        SOCKET_RECEIVE_SIZE)
                                http_io_buffer.add_request(
                                    fileno,
                                    http_io_buffer.get_request(fileno) + http_request_buffer
                                )
                                if self.EOL1 in http_io_buffer.get_request(fileno) \
                                        or self.EOL2 in http_io_buffer.get_request(fileno):
                                    request_data = http_io_buffer.get_request(fileno)[:-2] \
                                        if http_io_buffer.get_request(fileno).endswith("\r\n") \
                                        else http_io_buffer.get_request(fileno)
                                    http_parser = HttpParser(
                                        request_data,
                                        self.handlers,
                                        settings=self.settings
                                    )
                                    data = http_parser.parse()
                                    if isinstance(data, str) or isinstance(data, unicode):
                                        http_io_buffer.add_response(
                                            fileno,
                                            http_io_buffer.get_response(fileno) + data
                                        )
                                        epoll.modify(fileno, select.EPOLLOUT)  # change file number to epoll out mode
                                        http_io_routine_pool.remove(fileno)
                                    else:  # if coroutine
                                        http_io_routine_pool.add(fileno, http_parser)
                                        events_buf.append((fileno, event))
                                else:
                                    http_connection.remove_connection(fileno)
                                    http_io_buffer.remove_request(fileno)
                                    http_io_buffer.remove_response(fileno)
                                    http_io_routine_pool.remove(fileno)
                                    epoll.unregister(fileno)
                        elif event & select.EPOLLOUT:  # if out mode
                            http_response_message = http_io_buffer.get_response(fileno)
                            if PY3:
                                http_response_message = http_response_message.encode('utf-8')
                            bytes_written = http_connection.get_connection(fileno).send(
                                http_response_message
                            )
                            http_io_buffer.add_response(fileno, http_io_buffer.get_response(fileno)[bytes_written:])
                            if len(http_io_buffer.get_response(fileno)) == 0:  # if file sent
                                http_connection.get_connection(fileno).shutdown(socket.SHUT_RDWR)
                                epoll.modify(fileno, select.EPOLLHUP)
                        elif event & select.EPOLLHUP:  # if message sent and file number in epoll is hup
                            epoll.unregister(fileno)  # remove file number from epoll
                            http_connection.get_connection(fileno).close()  # close connection
                            http_connection.remove_connection(fileno)  # delete connection from connections dict
                    except Exception as e:
                        self.logger.info("error in __run_epoll: %s", str(e))
                        http_connection.remove_connection(fileno)
                        http_io_buffer.remove_request(fileno)
                        http_io_buffer.remove_response(fileno)
                        http_io_routine_pool.remove(fileno)
                        self.logger.info("fileno is: %s", str(fileno))
                        epoll.close()
                        epoll = select.epoll()
                        epoll.register(server_socket.fileno(), select.EPOLLIN)
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
        http_io_buffer = HttpIOBuffer()
        http_io_routine_pool = HttpIORoutinePool()
        index = 1
        events = [
            select.kevent(server_socket.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD),
            # select.kevent(server_socket.fileno(), select.KQ_FILTER_WRITE, select.KQ_EV_DELETE),
            # select.kevent(server_socket.fileno(), select.KQ_FILTER_READ, select.KQ_EV_ADD),
            # select.kevent(server_socket.fileno(), select.KQ_FILTER_WRITE, select.KQ_EV_DELETE),
        ]
        events_buf = []
        while True:
            try:
                event_list = kq.control(events, 128, 0.0001) + events_buf
                events_buf = []
            except select.error as e:
                self.logger.error("error in __run_kqueue: %s", str(e))
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
                            if each.udata >= 1 and each.filter == select.KQ_FILTER_READ:
                                http_parser = http_io_routine_pool.get(file_no=each.udata)
                                if http_parser:
                                    data = http_parser.parse()
                                    if isinstance(data, str) or isinstance(data, unicode):
                                        http_io_routine_pool.remove(each.udata)
                                        http_io_buffer.add_response(each.udata, data)
                                        events.append(
                                            select.kevent(
                                                http_connection.get_connection(each.udata).fileno(),
                                                select.KQ_FILTER_WRITE,
                                                select.KQ_EV_ADD,
                                                udata=each.udata
                                            )
                                        )
                                        events.remove(select.kevent(
                                            http_connection.get_connection(each.udata).fileno(),
                                            select.KQ_FILTER_READ,
                                            select.KQ_EV_ADD,
                                            udata=each.udata)
                                        )
                                    else:  # if coroutine
                                        http_io_routine_pool.add(each.udata, http_parser)
                                        events_buf.append(each)
                                else:
                                    conn = http_connection.get_connection(each.udata)
                                    if PY3:
                                        request_data = conn.recv(SOCKET_RECEIVE_SIZE).decode("utf-8")
                                    else:
                                        request_data = conn.recv(SOCKET_RECEIVE_SIZE)
                                    request_data = request_data[:-2] if request_data.endswith("\r\n") else request_data
                                    http_parser = HttpParser(
                                        request_data,
                                        handlers=self.handlers,
                                        settings=self.settings
                                    )
                                    data = http_parser.parse()
                                    if isinstance(data, str) or isinstance(data, unicode):
                                        http_io_buffer.add_response(each.udata, data)
                                        events.append(
                                            select.kevent(
                                                http_connection.get_connection(each.udata).fileno(),
                                                select.KQ_FILTER_WRITE,
                                                select.KQ_EV_ADD,
                                                udata=each.udata
                                            )
                                        )
                                        events.remove(select.kevent(
                                            http_connection.get_connection(each.udata).fileno(),
                                            select.KQ_FILTER_READ,
                                            select.KQ_EV_ADD,
                                            udata=each.udata)
                                        )
                                    else:  # if coroutine
                                        http_io_routine_pool.add(each.udata, http_parser)
                                        events_buf.append(each)
                            elif each.udata >= 1 and each.filter == select.KQ_FILTER_WRITE:
                                conn = http_connection.get_connection(each.udata)
                                data = http_io_buffer.get_response(each.udata)
                                if PY3:
                                    data = data.encode('utf-8')
                                conn.send(data)
                                events.remove(select.kevent(
                                    http_connection.get_connection(each.udata).fileno(),
                                    select.KQ_FILTER_WRITE,
                                    select.KQ_EV_ADD,
                                    udata=each.udata)
                                )
                                conn.close()
                                http_connection.remove_connection(each.udata)
                        except Exception as e:
                            self.logger.info("error in __run_kqueue event list: %s", str(e))
                            self.logger.info("each filter: %s", each.filter)
                            self.__remove_event(events, each)
                            http_connection.remove_connection(each.udata)
                            http_io_buffer.remove_request(each.udata)
                            http_io_buffer.remove_response(each.udata)
                            http_io_routine_pool.remove(each.udata)
                            kq.close()
                            kq = select.kqueue()
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
            http_io_routine_pool = HttpIORoutinePool()
            events_buf = []
            while True:
                events = poll.poll(1) + events_buf
                events_buf = []
                for fileno, event in events:
                    try:
                        if fileno == server_socket.fileno():  # if request come
                            connection, address = server_socket.accept()  # waiting income connection
                            connection.setblocking(0)  # none block
                            poll.register(connection.fileno(), select.POLLIN)  # register socket read event to poll
                            http_connection.add_connection(connection.fileno(), connection)
                            http_io_buffer.add_request(connection.fileno(), '')
                            http_io_buffer.add_response(connection.fileno(), self.response)
                        elif event & select.POLLIN:  # when data in os's read buffer area
                            http_parser = http_io_routine_pool.get(file_no=fileno)
                            if http_parser:
                                data = http_parser.parse()
                                if isinstance(data, str) or isinstance(data, unicode):
                                    http_io_buffer.add_response(
                                        fileno,
                                        http_io_buffer.get_response(fileno) + data
                                    )
                                    poll.modify(fileno, select.POLLOUT)  # change file number to epoll out mode
                                    http_io_routine_pool.remove(fileno)
                                else:  # if coroutine
                                    http_io_routine_pool.add(fileno, http_parser)
                                    events_buf.append((fileno, event))
                            else:
                                if PY3:
                                    http_request_buffer = http_connection.get_connection(fileno).recv(
                                        SOCKET_RECEIVE_SIZE).decode("utf-8")
                                else:
                                    http_request_buffer = http_connection.get_connection(fileno).recv(
                                        SOCKET_RECEIVE_SIZE)
                                http_io_buffer.add_request(
                                    fileno,
                                    http_io_buffer.get_request(fileno) + http_request_buffer
                                )
                                if self.EOL1 in http_io_buffer.get_request(fileno) \
                                        or self.EOL2 in http_io_buffer.get_request(fileno):
                                    request_data = http_io_buffer.get_request(fileno)[:-2] \
                                        if http_io_buffer.get_request(fileno).endswith("\r\n") \
                                        else http_io_buffer.get_request(fileno)
                                    http_parser = HttpParser(
                                        request_data,
                                        self.handlers,
                                        settings=self.settings
                                    )
                                    data = http_parser.parse()
                                    if isinstance(data, str) or isinstance(data, unicode):
                                        http_io_buffer.add_response(
                                            fileno,
                                            http_io_buffer.get_response(fileno) + data
                                        )
                                        poll.modify(fileno, select.POLLOUT)  # change file number to epoll out mode
                                        http_io_routine_pool.remove(fileno)
                                    else:  # if coroutine
                                        http_io_routine_pool.add(fileno, http_parser)
                                        events_buf.append((fileno, event))
                                else:
                                    http_connection.remove_connection(fileno)
                                    http_io_buffer.remove_request(fileno)
                                    http_io_buffer.remove_response(fileno)
                                    http_io_routine_pool.remove(fileno)
                                    poll.unregister(fileno)
                        elif event & select.POLLOUT:  # if out mode
                            http_response_message = http_io_buffer.get_response(fileno)
                            if PY3:
                                http_response_message = http_response_message.encode('utf-8')
                            bytes_written = http_connection.get_connection(fileno).send(
                                http_response_message
                            )
                            http_io_buffer.add_response(fileno, http_io_buffer.get_response(fileno)[bytes_written:])
                            if len(http_io_buffer.get_response(fileno)) == 0:  # if file sent
                                http_connection.get_connection(fileno).shutdown(socket.SHUT_RDWR)
                                poll.modify(fileno, select.POLLHUP)
                        elif event & select.POLLHUP:  # if message sent and file number in poll is hup
                            poll.unregister(fileno)  # remove file number from poll
                            http_connection.get_connection(fileno).close()  # close connection
                            http_connection.remove_connection(fileno)  # delete connection from connections dict
                    except Exception as e:
                        self.logger.info("error in __run_poll: %s", str(e))
                        http_connection.remove_connection(fileno)
                        http_io_buffer.remove_request(fileno)
                        http_io_buffer.remove_response(fileno)
                        http_io_routine_pool.remove(fileno)
                        self.logger.info("fileno is: %s", str(fileno))
                        poll.unregister(fileno)
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

    def __remove_event(self, events, each):
        """remove event from events

        :param events: the list contain some events
        :param each: the event will be removed
        :return: None

        """
        self.logger.warning("remove event with udata: %s", str(each.udata))
        for event in events:
            if event.ident == each.ident:
                events.remove(event)
                break

    def run(self, io_model=None):
        """run the web server

        :param io_model: os io model, EPOLL 0 KQUEUE 1 POLL 2
        :return: None

        """
        print("server run on port: %d" % self.port)
        self.logger.info("server run on port: %d" % self.port)
        if io_model:
            if io_model == IOModel.EPOLL and hasattr(select, "epoll"):
                print("run with epoll")
                self.logger.info("run with epoll")
                self.__run_epoll()
            elif io_model == IOModel.KQUEUE and hasattr(select, "kqueue"):
                print("run with kqueue")
                self.logger.info("run with kqueue")
                self.__run_kqueue()
            elif io_model == IOModel.POLL and hasattr(select, "poll"):
                print("run with poll")
                self.logger.info("run with poll")
                self.__run_poll()
            elif io_model == IOModel.ASYNCIO:
                print("run with asyncore")
                self.logger.info("run with asyncore")
                self.__run_async_io()
        else:
            if hasattr(select, "epoll"):
                print("run with epoll")
                self.logger.info("run with epoll")
                self.__run_epoll()
            elif hasattr(select, "kqueue"):
                print("run with kqueue")
                self.logger.info("run with kqueue")
                self.__run_kqueue()
            elif hasattr(select, "poll"):
                print("run with poll")
                self.logger.info("run with poll")
                self.__run_poll()
            else:
                print("run with asyncore")
                self.logger.info("run with asyncore")
                self.__run_async_io()
        print("server start failed!")
        self.logger.info("server start failed!")
