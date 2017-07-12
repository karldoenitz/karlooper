# -*-coding:utf-8-*-

from karlooper.config.config import HttpStatus, HttpStatusMsg
from karlooper.template import render


class HTTPResponse(object):
    status = 0
    message = ""
    data = ""
    
    def __init__(self, **kwargs):
        self.__settings = kwargs
        
    def render(self, template_path, **kwargs):
        static_path = self.__settings.get("template", ".")
        template_path = root_path + template_path
        return render(template_path, **kwargs), HttpStatus.SUCCESS, HttpStatusMsg.SUCCESS


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
