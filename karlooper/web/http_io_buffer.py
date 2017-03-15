# -*-encoding:utf-8-*-


class HttpIOBuffer(object):

    def __init__(self):
        self.requests = {}
        self.responses = {}

    def add_request(self, name, value):
        self.requests[name] = value

    def add_response(self, name, value):
        self.responses[name] = value

    def get_request(self, name):
        return self.requests[name]

    def get_response(self, name):
        return self.responses[name]

    def remove_request(self, name):
        del self.requests[name]

    def remove_response(self, name):
        del self.responses[name]
