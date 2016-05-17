# -*-coding:utf-8-*-

from karlooper.server.application import Application
from karlooper.server.request import Request

__author__ = 'karlvorndoenitz@gmail.com'


class TestHandler(Request):
    def get(self):
        test = self.get_parameter("test")
        cookie = self.get_cookie("what1")
        result = {
            "key": "value",
            "test": test,
            "cookie": cookie
        }
        http_message = self.get_http_request_message()
        print http_message
        self.set_cookie("what", "happened")
        self.set_cookie("what1", "happened1")
        self.set_cookie("what2", "happened2")
        return self.response_as_json(result)

    def post(self):
        post_1 = self.get_parameter("post1")
        result = {
            "key": "value",
            "test": 7758521,
            "post1": post_1
        }
        self.set_cookie("what", "happened")
        return self.response_as_json(result)


class TestHandler2(Request):
    def get(self):
        result = {
            "key": "value_test_2"
        }
        return self.response_as_json(result)


handlers = {
    "/test": TestHandler,
    "/test/test2": TestHandler2
}


if __name__ == '__main__':
    application = Application(9898, handlers)
    application.run()
