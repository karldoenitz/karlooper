# -*-encoding:utf-8-*-

from karlooper.web.request import Request


class BaseRestHandler(Request):
    def __handle(self):
        return self.process()

    def get(self):
        return self.__handle()

    def post(self):
        return self.__handle()

    def put(self):
        return self.__handle()
