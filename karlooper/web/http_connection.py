# -*-encoding:utf-8-*-


class HttpConnection(object):
    def __init__(self):
        self.connection = {}
        self.requests = {}
        self.responses = {}

    def add_connection(self, name, value):
        self.connection[name] = value

    def get_connection(self, name):
        return self.connection[name]

    def remove_connection(self, name):
        del self.connection[name]
