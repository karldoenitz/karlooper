# -*-coding:utf-8-*-

import os

from karlooper.utils.parse_command_line import CommandLineParser
from karlooper.web.application import Application
from karlooper.web.request import Request
from .test import test_handler

__author__ = 'karlvorndoenitz@gmail.com'


class TestHandler(Request):
    def get(self):
        http_message = self.get_http_request_message()
        print(http_message)
        test = self.get_parameter("test")
        cookie = self.get_cookie("what1")
        cookie_1 = self.get_security_cookie("what")
        result = {
            "key": "value",
            "test": test,
            "cookie": cookie,
            "cookie_1": cookie_1
        }
        self.set_header({
            "what": "happened",
            "hello": "world",
            "ok": "let's go"
        })
        self.clear_header("ok")
        self.set_security_cookie("what", "happened")
        self.set_security_cookie("what", "are you")
        self.set_cookie("what1", "happened1")
        self.set_cookie("what2", "happened2")
        return self.response_as_json(result)

    def post(self):
        http_message = self.get_http_request_message()
        print(http_message)
        post_1 = self.get_parameter("post1")
        result = {
            "key": "value",
            "test": 7758521,
            "post1": post_1
        }
        self.set_cookie("what", "happened")
        return self.response_as_json(result)

    def put(self):
        self.clear_all_cookie()
        return self.response_as_json({"msg": "cookie cleared"})


class TestHandler2(Request):
    def get(self):
        result = {
            "k": "v"
        }
        return self.response_as_json(result)
        # return self.redirect("http://www.baidu.com")

    def post(self):
        print(self.get_http_request_message())
        return self.http_response("Hello World")


class Test(Request):
    def get(self):
        return self.http_response("Hello, World!")


class Hello(object):
    pass


class HelloWorld(Request):
    def before_request(self):
        print(self.get_http_request_message())

    def get(self):
        title = "你好, 世界"
        numbers = [1, 2, 3, 4, 5]
        hello = Hello()
        hello.world = "world"
        return self.render("/helloworld.html", title=title, numbers=numbers, hello=hello)

    def teardown_request(self):
        print("tear down now")


class TestPathParam(Request):
    def get(self):
        result = {
            "status": 0,
            "desc": "succeed",
            "data": {
                "id": self.get_path_param_int("id"),
                "age": self.get_path_param_int("age"),
                "token": self.get_path_param_str("token")
            }
        }
        return self.response_as_json(result)


handlers = {
    "/test": TestHandler,
    "/test/test2": TestHandler2,
    "/hello-world": Test,
    "/hello": HelloWorld,
    "/test-handler": test_handler.TestHandler1,
    "/user/{age}/{id}": TestPathParam,
    "/user/vip/{id}/{token}": TestPathParam
}


settings = {
    "template": os.getcwd() + "/template",
    "static": os.getcwd() + "/template",
    "log_enable": False,
    "debug": True
}


if __name__ == '__main__':
    CommandLineParser.default(port=9988, log_enable=False)
    CommandLineParser.parse_command_line()
    application = Application(handlers, settings)
    application.run()
