# -*-coding:utf-8-*-
"""

store global config data

>>>set_cli_data({"port": 8080})
>>>data = get_cli_data()

"""


__CLI_DATA = dict({})


def set_cli_data(data):
    global __CLI_DATA
    __CLI_DATA = data


def get_cli_data():
    global __CLI_DATA
    return __CLI_DATA
