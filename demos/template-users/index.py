# -*-encoding:utf-8-*-

import os
from karlooper.web import IOModel
from karlooper.web.application import Application
from karlooper.web.request import Request


class User(object):
    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age


class UsersHandler(Request):
    def get(self):
        user_list = [User("name_%d" % i, "male(男)", i + 10) for i in range(20)]
        return self.render("/user-page.html", users=user_list)


url_mapping = {
    "/users": UsersHandler
}

settings = {
    "template": os.getcwd() + "/templates"
}


if __name__ == '__main__':
    application = Application(url_mapping, settings=settings, port=8080,)
    application.run(io_model=IOModel.POLL)
