# -*-coding:utf-8-*-
"""

auto reload
~~~~~~~~~~~

Use this model to watch your project and reload your project when the code was modified.

Usage
=====
>>> from karlooper.autoreload import AutoReload
>>> from karlooper.web.application import Application
>>> application = Application()
>>> auto_reload = AutoReload(application)
>>> auto_reload.run()

"""

import time


class AutoReload(object):
    def __init__(self, **kwargs):
        pass

    def __check(self):
        pass

    def __application(self):
        pass

    def run(self):
        thread_obj = self.__application()
        while True:
            time.sleep(1)
            if self.__check():
                thread_obj.stop()
                thread_obj = self.__application()
