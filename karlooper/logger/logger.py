# -*-coding:utf-8-*-

import os
import logging
import logging.config
from karlooper.config import get_cli_data


def init_logger(config_path=None):
    """get the logger object

    :param config_path: log config file
    :return: logger

    """
    cli_data = get_cli_data()
    log_enable = cli_data.get("log_enable")
    if not log_enable:
        return logging
    if isinstance(log_enable, str) and log_enable.lower() != "true":
        return logging
    path = os.path.dirname(__file__) + "/log.conf"
    config_file = config_path or path
    logging.config.fileConfig(config_file)
    logger = logging.getLogger()
    return logger
