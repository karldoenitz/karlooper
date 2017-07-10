# -*-coding:utf-8-*-

from karlooper.config.config import HttpStatus, HttpStatusMsg


class HTTPResponse(object):
    status = 0
    message = ""
    data = ""


class HTTPResponse404(HTTPResponse):
    status = HttpStatus.NOT_FOUND
    message = HttpStatusMsg.NOT_FOUND

    def data(self):
        return str(self.status)


class HTTPResponse405(HTTPResponse):
    status = HttpStatus.METHOD_NOT_ALLOWED
    message = HttpStatusMsg.METHOD_NOT_ALLOWED

    def data(self):
        return str(self.status)


class HTTPResponse500(HTTPResponse):
    status = HttpStatus.SERVER_ERROR
    message = HttpStatusMsg.SERVER_ERROR

    def data(self):
        return ""
