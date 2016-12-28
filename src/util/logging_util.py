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

logger1 = logging.getLogger('my_logger1')
logger1.setLevel(logging.INFO)

logger2 = logging.getLogger('my_logger2')
logger2.setLevel(logging.WARNING)

logger3 = logging.getLogger('my_logger3')
logger3.setLevel(logging.ERROR)

# 路径
log_path = configuration.log_path
if not os.path.exists(log_path):
    os.makedirs(log_path)

# 创建一个handler，用于写入日志文件
info = logging.FileHandler(log_path + '\\tool-info.log')

# 创建一个handler，用于写入日志文件
warning = logging.FileHandler(log_path + '\\tool-warning.log')

# 创建一个handler，用于写入日志文件
error = logging.FileHandler(log_path + '\\tool-error.log')

# 再创建一个handler，用于输出到控制台
console = logging.StreamHandler()

# 定义handler的输出格式formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
info.setFormatter(formatter)
warning.setFormatter(formatter)
error.setFormatter(formatter)

# 给logger添加handler
logger1.addHandler(info)
logger1.addHandler(console)

logger2.addHandler(warning)
logger2.addHandler(console)

logger3.addHandler(error)
logger3.addHandler(console)


def debug(message):
    logging.debug(message)


def info(message):
    logger1.info(message)


def warning(message):
    logger2.warning(message)


def error(message):
    logger3.error(message)
