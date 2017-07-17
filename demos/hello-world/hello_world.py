# -*-encoding:utf-8-*-

from karlooper.coroutine.coroutine_pool import koroutine
from karlooper.web.request import Request
from karlooper.web.application import Application


class HelloWorldHandler(Request):
    def get(self):
        return self.http_response("<p>Hello, World!</p>")


class HelloKoroutineHandler(Request):
    @koroutine
    def get(self):
        yield self.http_response("<p>Hello, Koroutine!</p>")


handlers_mapping = {
    "/hello-world": HelloWorldHandler,
    "/hello-koroutine": HelloKoroutineHandler
}


if __name__ == '__main__':
    application = Application(handlers=handlers_mapping, port=8080)
    application.run()
