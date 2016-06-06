# -*-coding:utf-8-*-

from karlooper.server.request import Request


class TestHandler1(Request):
    def get(self):
        self.set_cookie(key="hello", value="test")
        self.set_security_cookie(key="world", value="test2")
        result = {"value": "Hello, World!"}
        return self.response_as_json(result)
