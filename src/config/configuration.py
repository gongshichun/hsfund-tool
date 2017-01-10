# -*-coding=utf-8-*-
'''
@Created on 2016-12-27
@author gongsc@hsfund.com
配置信息
'''


class configuration:
    # 基金列表
    __fund_code_list = ['630001', '630009']

    # 发送邮件列表
    mail_list = 'gongsc@hsfund.com'

    # 短信列表
    sms_list = '18600344955'

    # 导出路径
    export_file_path = '../asset_export_{day}.xlsx'

    # SQL条件
    __fund_code_list_in = [x for x in __fund_code_list]
    __fund_code_list_in = ",".join(__fund_code_list_in)
    sql_parameter = {'fund_code_list_in': __fund_code_list_in}

    # SQL
    sql = '''
    SELECT 基金序号,
           基金代码,
           基金名称,
           资产单元序号,
           资产单元名称,
           拆分比例,
           昨日资产单元净资产,
           昨日资产单元份额,
           昨日资产单元单位净值,
           昨日资产单元份额 + SUM(申购赎回金额 * 拆分比例 / 100) / 昨日资产单元单位净值 AS 今日单元资产份额,
           SUM(申购赎回金额 * 拆分比例 / 100) AS 今日实际变动金额,
           SUM(申购赎回份额 * 拆分比例 / 100) AS 今日实际变动份额,
           CASE
             WHEN SUM(申购赎回金额 * 拆分比例 / 100) > 0 THEN
              '净申购'
             WHEN SUM(申购赎回金额 * 拆分比例 / 100) < 0 THEN
              '净赎回'
             WHEN SUM(申购赎回金额 * 拆分比例 / 100) = 0 THEN
              '无申赎或轧差为0'
           END 流出方向
      FROM (SELECT B.L_FUND_ID AS 基金序号,
                   F.VC_FUND_CODE AS 基金代码,
                   F.VC_FUND_NAME AS 基金名称,
                   B.L_ASSET_ID AS 资产单元序号,
                   D.VC_ASSET_NAME AS 资产单元名称,
                   NVL(B.EN_ASSET_VALUE_YESTERDAY, 0) AS 昨日资产单元净资产,
                   NVL(EN_ASSET_SHARE_YESTERDAY, 0) AS 昨日资产单元份额,
                   NVL(B.EN_ASSET_VALUE_YESTERDAY, 0) /
                   NVL(EN_ASSET_SHARE_YESTERDAY, 0) AS 昨日资产单元单位净值,
                   NVL(B.EN_RATIO, 0) AS 拆分比例,
                   NVL(EN_ASSET_VALUE, 0) AS 当日净资产,
                   CASE
                     WHEN VC_BUSIN_FLAG IN ('02', '50', '16', '73', '75', '70') THEN
                      EN_BALANCE
                     WHEN VC_BUSIN_FLAG IN ('03', '13', '74', '71') THEN
                      -EN_BALANCE
                   END AS 申购赎回金额,
                   CASE
                     WHEN VC_BUSIN_FLAG IN ('02', '50', '16', '73', '75', '70') THEN
                      EN_SHARES
                     WHEN VC_BUSIN_FLAG IN ('03', '13', '74', '71') THEN
                      -EN_SHARES
                   END AS 申购赎回份额
              FROM TASSETDAY B, TFUNDINFO F, TAPPLYREDEEM C, TASSET D
             WHERE INSTR(:fund_code_list_in, F.VC_FUND_CODE) > 0 AND F.L_FUND_ID = B.L_FUND_ID
               AND F.VC_CURRENCY_NO = B.VC_CURRENCY_NO
               AND B.L_DATE = C.L_DATE
               AND B.L_FUND_ID = C.L_FUND_ID
               AND B.L_FUND_ID = D.L_FUND_ID
               AND B.L_ASSET_ID = D.L_ASSET_ID
             ORDER BY B.EN_ASSET_VALUE_YESTERDAY)
     GROUP BY 基金序号,
              基金代码,
              基金名称,
              资产单元序号,
              资产单元名称,
              拆分比例,
              昨日资产单元净资产,
              昨日资产单元份额,
              昨日资产单元单位净值
    '''

    # 消息类型
    message_type_mail = 'mail'

    # 消息类型
    message_type_sms = 'sms'

    # 消息标题
    message_title = u'交易系统资产单位份额计算完成'

    # 消息内容
    message_context = u'交易系统资产单位份额计算完成'

    # 消息源
    message_src = u'交易系统资产单元份额计算小工具'

    # 数据URL
    data_db_url = 'oracle://trade:trade@182.168.0.63:1521/hsdb'

    # 消息中心URL
    message_db_url = 'oracle://msg:msg@182.168.0.156:1521/kukydb'

    # 日志路径
    log_path = 'D:\\log'

    # 定时执行
    day = '*'
    hour = '23'
    minute = '0'
