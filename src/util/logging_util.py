# -*-coding=utf-8-*-
'''
@Created on 2016-12-26
@author gongsc@hsfund.com
日志工具
'''

import logging
from config.configuration import *
import os

'''
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename='hsfund_tool_asset.log',
                    filemode='a')
'''


class LoggingFactory(object):
    INSTANCE = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.INSTANCE:
            __logger_info = logging.getLogger('logger_info')
            __logger_info.setLevel(logging.INFO)

            __logger_warning = logging.getLogger('logger_warning')
            __logger_warning.setLevel(logging.WARNING)

            __logger_error = logging.getLogger('logger_error')
            __logger_error.setLevel(logging.ERROR)

            # 路径
            __log_path = configuration.log_path
            if not os.path.exists(__log_path):
                os.makedirs(__log_path)

            # 创建一个handler，用于写入日志文件
            __info_handler = logging.FileHandler(__log_path + '\\tool-info.log')

            # 创建一个handler，用于写入日志文件
            __warning_handler = logging.FileHandler(__log_path + '\\tool-warning.log')

            # 创建一个handler，用于写入日志文件
            __error_handler = logging.FileHandler(__log_path + '\\tool-error.log')

            # 再创建一个handler，用于输出到控制台
            __console = logging.StreamHandler()

            # 定义handler的输出格式formatter
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            __info_handler.setFormatter(formatter)
            __warning_handler.setFormatter(formatter)
            __error_handler.setFormatter(formatter)

            # 给logger添加handler
            __logger_info.addHandler(__info_handler)
            __logger_info.addHandler(__console)

            __logger_warning.addHandler(__warning_handler)
            __logger_warning.addHandler(__console)

            __logger_error.addHandler(__error_handler)
            __logger_error.addHandler(__console)

            cls.__logger_info = __logger_info
            cls.__logger_warning = __logger_warning
            cls.__logger_error = __logger_error
            cls.INSTANCE = super(LoggingFactory, cls).__new__(cls, *args, **kwargs)
        return cls.INSTANCE

    def get_logger_info(self):
        return self.__logger_info

    def get_logger_warning(self):
        return self.__logger_warning

    def get_logger_error(self):
        return self.__logger_error


def debug(message):
    logging.debug(message)


def info(message):
    LoggingFactory().get_logger_info().info(message)


def warning(message):
    LoggingFactory().get_logger_warning().warning(message)


def error(message):
    LoggingFactory().get_logger_error().error(message)
