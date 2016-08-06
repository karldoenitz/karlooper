# -*-coding:utf-8-*-

__author__ = 'karlvorndoenitz@gmail.com'


RESPONSE_HEAD_MESSAGE = "HTTP/1.1 %(status)s %(status_msg)s\r\n" \
                        "Date: %(date)s\r\n" \
                        "Host: %(host)s\r\n" \
                        "Content-Length: %(content_length)s\r\n\r\n"
SOCKET_RECEIVE_SIZE = 1024 * 64
DEFAULT_PORT = 80
COOKIE_SECURITY_DEFAULT_STRING = "1qaz2wsx3"
CLIENT_CONNECT_TO_SERVER_NUM = 128

content_type = {
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "png": "image/png",
    "gif": "image/gif",
    "css": "text/css",
    "js": "text/js",
    "mp3": "audio/mpeg",
    "ogg": "audio/ogg",
    "mp4": "video/mp4"
}


class HttpStatus(object):
    SUCCESS = 200
    PARTIAL_SUCCESS = 206
    REDIRECT = 302
    RESOURCE_NOT_MODIFIED = 304
    REQUEST_FORBID = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    SERVER_ERROR = 500
    SERVER_NOT_SUPPORT = 501
    TIME_OUT = 504


class HttpStatusMsg(object):
    SUCCESS = "OK"
    PARTIAL_SUCCESS = "OK"
    REDIRECT = "Moved Temporarily"
    RESOURCE_NOT_MODIFIED = "Not Modified"
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
