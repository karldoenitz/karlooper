# -*-coding:utf-8-*-
"""

config
~~~~~~
store global config data

Usage
=====
>>> set_cli_data({"port": 8080})
>>> data = get_cli_data()

"""


__CLI_DATA = dict({})
__GLOBAL_CONF_DATA = dict({})


def set_cli_data(data):
    """ set global config data

    :param data: a dict contain global config data
    :return: None

    """
    global __CLI_DATA
    if not data:
        return
    for key in data:
        __CLI_DATA[key] = data[key]


def get_cli_data():
    """ get data from command line client

    :return: None

    """
    global __CLI_DATA
    return __CLI_DATA


def set_global_conf(key, data):
    """ set global config data
    
    :param key: global data's key
    :param data: global data
    :return: None
    
    """
    global __GLOBAL_CONF_DATA
    if not data:
        return
    __GLOBAL_CONF_DATA[key] = data


def get_global_conf(key):
    """ get data from global config
    
    :param key: the data's key
    :return: the data
    
    """
    global __GLOBAL_CONF_DATA
    return __GLOBAL_CONF_DATA[key]

