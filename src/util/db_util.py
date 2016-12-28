# -*-coding=utf-8-*-
'''
@Created on 2016-12-26
@author gongsc@hsfund.com
发送信息类
'''

import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from logging_util import error


# 创建Engine
def get_engine(url, echo):
    return create_engine(url, echo=echo)


def close_connection(conn):
    if conn:
        conn.close()


# 表实例
def __get_hs_task_msg_queue(engine):
    __metadata = MetaData(engine)

    return Table('HS_TASK_MSG_QUEUE', __metadata,
                 Column('VC_MSG_TYPE', String, nullable=False),
                 Column('VC_MSG_CONTENT', String, nullable=False),
                 Column('VC_MSG_TITLE', String, nullable=False),
                 Column('VC_MSG_TARGET', String, nullable=False),
                 Column('I_ID', Integer, nullable=False),
                 Column('VC_SEND_SRC', String, nullable=False)
                 )


# 查询资产信息
def query_asset_data(engine, sql, sql_parameter):
    try:
        # 获取连接
        conn = engine.connect()

        # 组装成DataFrame
        df = pd.read_sql(sql=sql, con=conn, params=sql_parameter)

        return df
    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        close_connection(conn)


# 查询SQE
def query_msg_queue_sqe(engine):
    conn = None
    try:
        # 获取连接
        conn = engine.connect()

        result = conn.execute('SELECT SEQ_MSG_QUEUE.NEXTVAL FROM DUAL')
        return result.fetchall()[0][0]

    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        close_connection(conn)

    return 0


# 插入数据
def insert_message(engine, data):
    conn = None
    try:
        # 获取连接
        conn = engine.connect()

        hs_task_msg_queue_insert = __get_hs_task_msg_queue(engine).insert()

        # 插入数据
        conn.execute(hs_task_msg_queue_insert, data)
    except Exception, e:
        error(e)
    finally:
        # 关闭连接
        close_connection(conn)
