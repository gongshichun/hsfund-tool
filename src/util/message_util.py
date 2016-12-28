# -*-coding=utf-8-*-
'''
@Created on 2016-12-26
@author gongsc@hsfund.com
发送信息类
'''

import os
from sqlalchemy import *
from logging_util import error
from config.configuration import *


class MessageDBConn(object):
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
            cls.engine = create_engine(configuration.message_db_url, echo=False)

            # 绑定元信息
            metadata = MetaData(cls.engine)

            cls.hs_task_msg_queue = Table('HS_TASK_MSG_QUEUE', metadata,
                                          Column('VC_MSG_TYPE', String, nullable=False),
                                          Column('VC_MSG_CONTENT', String, nullable=False),
                                          Column('VC_MSG_TITLE', String, nullable=False),
                                          Column('VC_MSG_TARGET', String, nullable=False),
                                          Column('I_ID', Integer, nullable=False),
                                          Column('VC_SEND_SRC', String, nullable=False)
                                          )
            cls.INSTANCE = super(MessageDBConn, cls).__new__(cls, *args, **kwargs)
        return cls.INSTANCE

    def get_connection(self):
        return self.engine.connect()

    def get_hs_task_msg_queue(self):
        return self.hs_task_msg_queue

    @staticmethod
    def close_connection(conn):
        if conn:
            conn.close()


# 查询SQE
def query_msg_queue_sqe():
    conn = None
    try:
        # 获取连接
        conn = MessageDBConn().get_connection()

        result = conn.execute('SELECT SEQ_MSG_QUEUE.NEXTVAL FROM DUAL')
        return result.fetchall()[0][0]

    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        MessageDBConn.close_connection(conn)

    return 0


# 插入数据
def insert_message(data):
    conn = None
    try:
        # 获取连接
        conn = MessageDBConn().get_connection()

        hs_task_msg_queue_insert = MessageDBConn().get_hs_task_msg_queue().insert()

        # 插入数据
        conn.execute(hs_task_msg_queue_insert, data)
    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        MessageDBConn.close_connection(conn)
