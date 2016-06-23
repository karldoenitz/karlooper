# -*-coding:utf-8-*-

__author__ = 'karlvorndoenitz@gmail.com'


RESPONSE_HEAD_MESSAGE = "HTTP/1.1 %(status)s %(status_msg)s\r\n" \
                        "Date: %(date)s\r\n" \
                        "Host: %(host)s\r\n" \
                        "Content-Length: %(content_length)s\r\n\r\n"
SOCKET_RECEIVE_SIZE = 1024
DEFAULT_PORT = 80
COOKIE_SECURITY_DEFAULT_STRING = "1qaz2wsx3"
CLIENT_CONNECT_TO_SERVER_NUM = 128


class HttpStatus(object):
    SUCCESS = 200
    PARTIAL_SUCCESS = 206
    REDIRECT = 302
    REQUEST_FORBID = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    SERVER_ERROR = 500
    SERVER_NOT_SUPPORT = 501
    TIME_OUT = 503


class HttpStatusMsg(object):
    SUCCESS = "OK"
    PARTIAL_SUCCESS = "OK"
    REDIRECT = "Moved Temporarily"
    REQUEST_FORBID = "FORBID"
    NOT_FOUND = "NOT-FOUND"
    METHOD_NOT_ALLOWED = "METHOD-NOT-ALLOWED"
    SERVER_ERROR = "SERVER-ERROR"
    SERVER_NOT_SUPPORT = "NOT-SUPPORT"
    TIME_OUT = "TIME-OUT"


class ContentType(object):
    FORM = "application/x-www-form-urlencoded"
    JSON = "application/json"
    HTML = "text/html"
    TEXT = "text/plain"
