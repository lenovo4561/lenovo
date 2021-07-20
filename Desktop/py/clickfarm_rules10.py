# -*- coding: UTF-8-*-
# 规则10（近7天完成订单超30笔设备，近7天所有正常设备号订单）

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
    #连接mysql数据库
    conn = pymysql.connect(host='10.16.0.12', user='root', password='SG91QDg4MjgzOTgx', port=3306,
                           db='transfer_target', charset='utf8')

    #创建游标对象
    cur = conn.cursor()

    #执行sql
    cur.execute(sql)

    #获取数据
    result = cur.fetchall()
    #获取字段名
    columns = cur.description

    #关闭游标
    cur.close()
    #关闭连接
    conn.close()

    #数据转为dataframe格式
    cols=[]
    for i in columns:
        cols.append(i[0])

    org_data = pd.DataFrame(list(result),columns=cols)

    return org_data

def get_remote_data(mysqlip,sql):
    #连接远程mysql数据库

    server = SSHTunnelForwarder(
        ('1.14.193.17', 22),  # B机器的配置
        ssh_password='SG91QDg4MjgzOTgx',
        ssh_username='root',
        remote_bind_address=(mysqlip, 3306)
        )
    server.start()

    conn = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                           port=server.local_bind_port,
                           user='imageuser',
                           passwd='A8DAOa7dava4f_a1TA5',
                           db='usercenter')

    #创建游标对象
    cur = conn.cursor()

    #执行sql
    cur.execute(sql)

    #获取数据
    result = cur.fetchall()
    #获取字段名
    columns = cur.description

    #关闭游标
    cur.close()
    #关闭连接
    conn.close()
    server.close()

    #数据转为dataframe格式
    cols=[]
    for i in columns:
        cols.append(i[0])

    org_data = pd.DataFrame(list(result),columns=cols)

    return org_data


def write2mysql(results):
    # 往数据库写入数据
    #import csv

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

    #sql写入语句
    sql = """insert ignore into clickfarm_rules10(orderSn) values(%s)"""

    # 插入数据
    cur.executemany(sql, results)

    # 必须要执行此操作才能写入到数据库
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()


def extract_data():
    # 近7天辅助表数据
    sql1 = """
        select orderId,passengerId,orderDeviceId
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
    # 近10天登录数据
    sql3 = """
        select uid,deviceId,platform,softVersion,lastLoginTime
        from login
        where lastLoginTime>= timestamp(DATE_SUB(curdate(),interval 10 day))
        """

    assist_data = get_data(sql1)
    paid_data = get_data(sql2)
    login_data1 = get_remote_data(mysqlip='172.19.202.7', sql=sql3)
    login_data2 = get_remote_data(mysqlip='172.19.202.9', sql=sql3)

    return (assist_data,paid_data,login_data1,login_data2)

def clickfarm_rules10(assist_data,paid_data,login_data1,login_data2):
    # 近7天下单数据
    before7day_time = datetime.datetime.strptime((datetime.date.today() - datetime.timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    paid_data2 = paid_data[paid_data['startChargeTime'] >= before7day_time]

    # 左关联取辅助表乘客id，设备id
    order_data = pd.merge(paid_data2, assist_data, how='left', left_on='orderSn', right_on='orderId')
    order_data = order_data[order_data['passengerId'].notnull()]

    # 合并登录数据
    login_data = pd.concat([login_data1,login_data2],axis=0,ignore_index=True)

    # app登录数据（4.9.6版本之后）
    login_data_app = login_data[login_data['platform'].isin([1, 2])]
    login_data_app['softVersion'].replace('\\.*', '', regex=True, inplace=True)
    login_data_app['softVersion'] = login_data_app['softVersion'].astype('int64')
    login_data_appnew = login_data_app[login_data_app['softVersion'] >= 496]

    # 非app登录数据（小程序）
    login_data_notapp = login_data[~login_data['platform'].isin([1,2])]

    # 合并整理后的登录数据
    login_data_new = pd.concat([login_data_appnew, login_data_notapp], axis=0, ignore_index=True)

    # 有使用正常设备号的乘客id，设备id
    login_passengers = login_data_new[['uid', 'deviceId']].drop_duplicates()

    # 取有使用正常设备号乘客和设备对应的订单
    order_data_cond = pd.merge(order_data, login_passengers, how='inner', left_on=['passengerId', 'orderDeviceId'],
                               right_on=['uid', 'deviceId'])[['orderSn', 'passengerId', 'orderDeviceId']]

    # 近7天同一设备完成支付超30单
    devices = order_data_cond.groupby('orderDeviceId')['orderSn'].count().loc[lambda x: x > 30].reset_index(name='count')

    # 近7天完成订单超30笔设备，近7天所有正常设备号订单
    results = pd.merge(order_data_cond, devices, how='inner')['orderSn']

    return results


if __name__ == "__main__":
    start = time.time()

    # 获取订单辅助数据，支付数据，登录数据
    assist_data, paid_data, login_data1, login_data2 = extract_data()

    # 规则10（近7天完成订单超30笔设备，近7天所有正常设备号订单）
    results = clickfarm_rules10(assist_data, paid_data, login_data1, login_data2)

    # 结果去重写入数据库
    write2mysql(set(results))

    end = time.time()
    print("总用时：", (end - start))



