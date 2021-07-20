# -*- coding: UTF-8-*-
# 规则12（近7天完成订单超30笔乘客，近7天所有订单）

import os
from numpy import *
import pandas as pd
import numpy as np
import datetime
import time
import pymysql
from sshtunnel import SSHTunnelForwarder
import warnings

warnings.filterwarnings("ignore")


def get_data(sql):
    #连接远程mysql数据库
    server = SSHTunnelForwarder(
        ('1.14.193.17', 22),  # B机器的配置
        ssh_password='SG91QDg4MjgzOTgx',
        ssh_username='root',
        remote_bind_address=('10.16.0.12', 3306)
        )
    server.start()

    conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                           port=server.local_bind_port,
                           user='root',
                           passwd='SG91QDg4MjgzOTgx',
                           db='transfer_target')

    # 创建游标对象
    cur = conn.cursor()

    # 执行sql
    cur.execute(sql)

    # 获取数据
    result = cur.fetchall()
    # 获取字段名
    columns = cur.description

    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()

    # 数据转为dataframe格式
    cols = []
    for i in columns:
        cols.append(i[0])

    org_data = pd.DataFrame(list(result), columns=cols)

    return org_data


def write2mysql(results):
    # 往数据库写入数据
    # import csv
    #连接远程mysql数据库
    server = SSHTunnelForwarder(
        ('1.14.193.17', 22),  # B机器的配置
        ssh_password='SG91QDg4MjgzOTgx',
        ssh_username='root',
        remote_bind_address=('10.16.0.12', 3306)
        )
    server.start()

    conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                           port=server.local_bind_port,
                           user='root',
                           passwd='SG91QDg4MjgzOTgx',
                           db='transfer_target')

    # 创建游标对象
    cur = conn.cursor()

    # sql写入语句
    sql = """insert ignore into clickfarm_rules12(orderSn) values(%s)"""

    # 插入数据
    cur.executemany(sql, results)

    # 必须要执行此操作才能写入到数据库
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()


if __name__ == "__main__":
    start = time.time()

    # 近7天辅助表数据
    sql1 = """
        select orderId,passengerId
        from `paid_order_assist_info` 
        where payTime >= timestamp(DATE_SUB(curdate(),interval 7 day))
        and payTime < timestamp(curdate())
        """
    # 近7天支付数据
    sql2 = """
        select orderSn,startChargeTime
        from `paid_order_day_statistics` 
        where payTimeA >= timestamp(DATE_SUB(curdate(),interval 7 day))
        and payTimeA < timestamp(curdate())
        """

    assist_data = get_data(sql1)
    paid_data = get_data(sql2)

    # 近7天下单数据
    before7day_time = datetime.datetime.strptime(
        (datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    paid_data2 = paid_data[paid_data['startChargeTime'] >= before7day_time]

    # 左关联取辅助表乘客id
    order_data = pd.merge(paid_data2, assist_data, how='left', left_on='orderSn', right_on='orderId')
    order_data = order_data[order_data['passengerId'].notnull()]

    # 近7天完成订单超30笔乘客
    passengers = order_data.groupby('passengerId')['orderSn'].count().loc[lambda x: x > 30].reset_index(name='count')

    # 近7天完成订单超30笔乘客，近7天所有订单
    result = pd.merge(order_data, passengers, how='inner')
    results = result['orderSn']

    # 结果去重写入数据库
    write2mysql(set(results))

    end = time.time()
    print("总用时：", (end - start))
