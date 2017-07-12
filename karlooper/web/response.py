# -*-coding:utf-8-*-
"""

response
~~~~~~~~

Use this model to customize your http response web page.

Usage
=====
>>> from karlooper.web.response import HTTPResponse404
>>> def not_found(self):
...     return "<h1>Page Not Found</h1>"
...
>>> HTTPResponse404.data = not_found

"""
from karlooper.config.config import HttpStatus, HttpStatusMsg
from karlooper.template import render


class HTTPResponse(object):
    status = 0
    message = ""
    data = ""
    
    def __init__(self, **kwargs):
        self.__settings = kwargs
        
    def render(self, template_path, **kwargs):
        """ customize your HTTPResponse web page use template

        :param template_path: template path
        :param kwargs: parameters
        :return: html formatted string

        """
        static_path = self.__settings.get("template", ".")
        template_path = static_path + template_path
        return render(template_path, **kwargs)


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
