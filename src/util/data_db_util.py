# -*-coding=utf-8-*-
'''
@Created on 2016-12-26
@author gongsc@hsfund.com
数据工具类
'''

import os
import pandas as pd
from sqlalchemy import create_engine
from logging_util import error
from config.configuration import *


class DataDBConn(object):
    INSTANCE = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if not cls.INSTANCE:
            os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
            '''
            os.environ['ORACLE_HOME'] = 'd:\\dev\\instantclient_11_2\\'
            os.environ['TNS_ADMIN'] = 'd:\\dev\\instantclient_11_2\\'
            os.environ['PATH'] = os.environ['PATH'] + ';d:\\dev\\instantclient_11_2\\'
            os.environ['NLS_LANG'] = NLSLang
            '''
            cls.engine = create_engine(configuration.data_db_url, echo=False)
            cls.INSTANCE = super(DataDBConn, cls).__new__(cls, *args, **kwargs)
        return cls.INSTANCE

    def get_connection(self):
        return self.engine.connect()

    @staticmethod
    def close_connection(conn):
        if conn:
            conn.close()


# 查询数据
def query_data(sql, sql_parameter):
    try:
        # 获取连接
        conn = DataDBConn().get_connection()

        # 组装成DataFrame
        df = pd.read_sql(sql=sql, con=conn, params=sql_parameter)

        return df
    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        DataDBConn.close_connection(conn)


conn = DataDBConn().get_connection()
