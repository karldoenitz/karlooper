# -*-encoding:utf-8-*-


class HttpIOBuffer(object):
    """

    This class contains seven methods:

    def add_request(self, name, value): add request to io buffer

    def add_response(self, name, value): add response to io buffer

    def get_request(self, name): get request from io buffer

    def get_response(self, name): get response from io buffer

    def remove_request(self, name): get request from io buffer

    def remove_response(self, name): get response from io buffer

    """
    def __init__(self):
        self.requests = {}
        self.responses = {}

    def add_request(self, name, value):
        """add request

        :param name: request's name
        :param value: request
        :return: None

        """
        self.requests[name] = value

    def add_response(self, name, value):
        """add response

        :param name: response's name
        :param value: response
        :return: None

        """
        self.responses[name] = value

    def get_request(self, name):
        """get request

        :param name: the name of request
        :return: request

        """
        return self.requests[name]

    def get_response(self, name):
        """get response

        :param name: the name of response
        :return: response

        """
        return self.responses[name]

    def remove_request(self, name):
        """remove request

        :param name: the name of request
        :return: None

        """
        if name in self.requests:
            del self.requests[name]

    def remove_response(self, name):
        """remove response

        :param name: the name of response
        :return: None

        """
        if name in self.responses:
            del self.responses[name]
