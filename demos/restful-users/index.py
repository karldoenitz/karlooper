# -*-encoding:utf-8-*-

import os
from karlooper.web.application import Application
from karlooper.web.request import Request


class UsersHandler(Request):
    def get(self):
        return self.render("/user-page.html")


class UserInfoHandler(Request):
    def post(self):
        print self.get_http_request_message()
        size = self.get_parameter("user_size", 0)
        size = int(size)
        user_list = [{"name": "name_%d" % i, "gender": "male", "age": i + 10} for i in xrange(size)]
        result = {
            "status": 0,
            "message": "OK",
            "data": user_list
        }
        return self.response_as_json(result)


url_mapping = {
    "/users": UsersHandler,
    "/user-info": UserInfoHandler
}

settings = {
    "template": os.getcwd() + "/templates",
    "static": os.getcwd() + "/templates",
    "log_enable": False,
    "debug": True
}


if __name__ == '__main__':
    application = Application(url_mapping, settings=settings, port=8080,)
    application.run()
