# -*-encoding:utf-8-*-

import os
from karlooper.web.application import Application
from karlooper.web.request import Request
from karlooper.web.response import HTTPResponse404, HTTPResponse500


def not_found(self):
    # return "404 not found"  # you can make it easy
    return self.render("/customize.html", title="not found", code="404", message="Page Not Found")

HTTPResponse404.data = not_found


def server_error(self):
    # return "500 server error"  # you can make it easy
    return self.render("/customize.html", title="server error", code="500", message="Server Error, We are fixing it!")

HTTPResponse500.data = server_error


class MainPage(Request):
    def get(self):
        return self.http_response("<h1>This is Main Page!</h1>")


class ErrorPage(Request):
    def get(self):
        return self.http_response("123" + 123)


urls = {
    "/main": MainPage,
    "/error": ErrorPage
}

settings = {
    "template": os.getcwd() + "/templates",
    "static": os.getcwd() + "/templates",
    "log_enable": False,
    "debug": True
}


if __name__ == '__main__':
    application = Application(handlers=urls, settings=settings, port=8080)
    application.run()
