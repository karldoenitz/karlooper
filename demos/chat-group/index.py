# -*- coding: utf-8 -*-

import os
from handlers.controllers import ChatController
from handlers.rest import MessageHandler
from karlooper.config import set_global_conf
from karlooper.web.application import Application
from redis_manage import RedisManage

__author__ = "karlvorndoenitz@gmail.com"

handlers_mapping = {
    "/msg": MessageHandler,
    "/chat": ChatController
}

settings = {
    "template": os.getcwd() + "/template"
}


if __name__ == '__main__':
    redis_manager = RedisManage()
    set_global_conf("redis", redis_manager)
    application = Application(handlers_mapping, settings=settings)
    application.listen(8888)
    application.run()
