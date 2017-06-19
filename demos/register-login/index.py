# -*-encoding:utf-8-*-

import os
from controllers.handlers import Login, Register, MainPage
from controllers.rest import LoginRestHandler, RegisterRestHandler
from karlooper.web.application import Application


urls = {
    "/login": Login,
    "/register": Register,
    "/main": MainPage,
    "/rest/login": LoginRestHandler,
    "/rest/register": RegisterRestHandler
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
