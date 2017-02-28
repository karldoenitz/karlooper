# -*-encoding:utf-8-*-

from karlooper.web.request import Request
from karlooper.web.application import Application


class HelloWorldHandler(Request):
    def get(self):
        return self.http_response("<p>Hello, World!</p>")


handlers_mapping = {
    "/hello-world": HelloWorldHandler
}


if __name__ == '__main__':
    application = Application(handlers=handlers_mapping, port=8080)
    application.run()
