# -*-coding=utf-8-*-
'''
@Created on 2016-12-26
@author gongsc@hsfund.com
交易系统资产单元份额计算工具
'''

from util.data_db_util import query_data
from util.message_util import insert_message, query_msg_queue_sqe
from util.logging_util import info, error
from config.configuration import *
import time
from apscheduler.schedulers.blocking import BlockingScheduler
from pandas.io.excel import ExcelWriter
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# Excel写入
excel_writer = None


# 获取导入文件名
def get_export_file_path():
    export_file_path = configuration.export_file_path
    export_file_path = export_file_path.replace('{day}', time.strftime('%Y-%m-%d', time.localtime(time.time())))
    return export_file_path


# 写Excel
def write_excel(df_excel):
    df_excel.set_index(u'基金序号', inplace=True)
    sheet_name = list(df_excel[u'基金代码'])[0]
    df_excel.to_excel(excel_writer=excel_writer, sheet_name=sheet_name, encoding='utf-8')


# 发送信息
def send_message(extend_context):
    # 发送邮件通知
    data = dict(VC_MSG_TYPE=configuration.message_type_mail, VC_MSG_TITLE=configuration.message_title,
                VC_MSG_CONTENT=configuration.message_context + extend_context,
                VC_MSG_TARGET=configuration.mail_list,
                I_ID=query_msg_queue_sqe(),
                VC_SEND_SRC=configuration.message_src)
    insert_message(data)

    # 发送短信通知
    data = dict(VC_MSG_TYPE=configuration.message_type_sms, VC_MSG_TITLE=configuration.message_title,
                VC_MSG_CONTENT=configuration.message_context + extend_context,
                VC_MSG_TARGET=configuration.sms_list, I_ID=query_msg_queue_sqe(),
                VC_SEND_SRC=configuration.message_src)
    insert_message(data)


# 计算
def calc_asset():
    # 查询
    df = query_data(configuration.sql, configuration.sql_parameter)

    # 写入Excel中
    if not df.empty:
        global excel_writer
        excel_writer = ExcelWriter(path=get_export_file_path())
        df.groupby(u'基金代码').apply(write_excel)
        excel_writer.save()

    # 发送信息
    extend_context = '' if not df.empty else ',无数据处理，Excel不导出'
    send_message(extend_context=extend_context)


# 调度
def doscheduler():
    # 记录日志
    info('Calc Asset Start!')

    start = time.clock()
    try:
        calc_asset()
    except Exception, e:
        error(e)
    end = time.clock()

    # 记录日志
    info('Calc Asset Finish! Cost %ds' % (end - start))


# 主方法
if __name__ == '__main__':

    # 启动Scheduler
    scheduler = BlockingScheduler()
    # day, day_of_week, hour, minute, second等参数
    scheduler.add_job(doscheduler, 'cron', hour='18', day="*")
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit, Exception), e:
        # 记录异常日志
        error(e)
