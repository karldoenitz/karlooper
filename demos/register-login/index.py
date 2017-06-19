# -*-encoding:utf-8-*-

import os
from controllers.handlers import Login, Register, MainPage
from karlooper.web.application import Application


urls = {
    "/login": Login,
    "/register": Register,
    "/main": MainPage
}


settings = {
    "template": os.getcwd() + "/templates",
    "static": os.getcwd() + "/templates",
    "log_enable": False,
    "debug": True
}


if __name__ == '__main__':
    application = Application(handlers=urls, settings=settings)
    application.listen(8080)
    application.run()
