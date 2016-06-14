# -*-coding:utf-8-*-
"""

introduction
first initial an object of CommandLineParser
then use the object to set some default values
end, use parse_command_line function to parse the command line


>>>from karlooper.utils.parse_command_line import CommandLineParser
>>>command_line_parser = CommandLineParser()
>>>command_line_parser.default(port=8080, debug=True, log_enable=False)
>>>command_line_parser.parse_command_line()

"""

import sys


class CommandLineParser(object):
    def __init__(self):
        self.__params_dict = dict({})

    def default(self, **kwargs):
        for param in kwargs:
            self.__params_dict[param] = kwargs[param]

    def parse_command_line(self):
        params = sys.argv[1:]
        for param in params:
            self.__params_dict[param.split("=")[0]] = param.split("=")[1]
