Karlooper Web Server
====================

`Karlooper <https://github.com/karldoenitz/karlooper>`_ is a Python web framework and
asynchronous networking library, originally developed at `Coders
<https://www.androiddev.net/>`_.  By using non-blocking network I/O, Karlooper
can scale to tens of thousands of open connections, for more `click <https://github.com/karldoenitz/karlooper>`_

Hello, World!
-------------

Here is a simple "Hello, World!" example web app for Karlooper:

.. code-block:: python

    # -*-coding:utf-8-*-

    from karlooper.web.application import Application
    from karlooper.web.request import Request

    __author__ = 'karlvorndoenitz@gmail.com'


    class HelloHandler(Request):
        def get(self):
            return self.http_response("Hello, World!")

    handlers = {
        "/hello": HelloHandler
    }

    if __name__ == '__main__':
        application = Application(handlers, port=8000)
        application.run()


Documentation
-------------

Documentation and links to additional resources are available at
https://github.com/karldoenitz/karlooper