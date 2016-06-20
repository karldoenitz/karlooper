# -*-coding:utf-8-*-

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")

Handlers=[
    (r"/hello", MainHandler),
]

application = tornado.web.Application(Handlers)

if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()
