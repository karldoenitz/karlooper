# -*-encoding:utf-8-*-


class HttpConnection(object):
    """

    This class contains four methods

    def __init__(self): initialize

    def add_connection(self, name, value): add connection

    def get_connection(self, name): get connection

    def remove_connection(self, name): remove connection

    """
    def __init__(self):
        self.connection = {}
        self.requests = {}
        self.responses = {}

    def add_connection(self, name, value):
        """add connection

        :param name: connection name
        :param value: connection
        :return: None

        """
        self.connection[name] = value

    def get_connection(self, name):
        """get connection

        :param name: connection name
        :return: connection

        """
        return self.connection[name]

    def remove_connection(self, name):
        """remove connection

        :param name: connection name
        :return: None

        """
        if name in self.connection:
            del self.connection[name]
