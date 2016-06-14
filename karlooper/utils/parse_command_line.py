# -*-coding:utf-8-*-

import sys


class CommandLineParser(object):
    __params_dict = dict({})

    def default(self, **kwargs):
        for param in kwargs:
            self.__params_dict[param] = kwargs[param]

    def parse_command_line(self):
        params = sys.argv[1:]
        for param in params:
            self.__params_dict[param.split("=")[0]] = param.split("=")[1]
