# -*-coding:utf-8-*-
"""

parse_command_line
~~~~~~~~~~~~~~~~~~

introduction
first initial an object of CommandLineParser
then use the object to set some default values
end, use parse_command_line function to parse the command line

Usage
=====
>>> from karlooper.utils.parse_command_line import CommandLineParser
>>> CommandLineParser.default(port=8080, debug=True, log_enable=False)
>>> CommandLineParser.parse_command_line()

"""

import sys
from karlooper.config import set_cli_data


message = """
Usage: python index.py [name]=[value]
           (to execute a python file)
where options include:
    help: for help
    port: set port that the server to listen
    is_debug: True or False, set True to enable debug
    log_enable: True or False, set True to enable log
    cookie: cookie's security key
"""


class CommandLineParser(object):
    """

    Two methods:

    def default(**kwargs):  set default arguments

    def parse_command_line():  parse the command line to get arguments

    """
    @staticmethod
    def default(**kwargs):
        set_cli_data(kwargs)

    @staticmethod
    def parse_command_line():
        params = sys.argv[1:]
        __params_dict = dict({})
        if "help" in params:
            print message
            sys.exit(0)
        for param in params:
            __params_dict[param.split("=")[0]] = param.split("=")[1]
        set_cli_data(data=__params_dict)
