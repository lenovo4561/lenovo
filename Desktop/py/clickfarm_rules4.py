#!/usr/bin/env python
#-*- coding: UTF-8-*-


import os
import multiprocessing
#import csv
from numpy import *
import pandas as pd
import numpy as np
#import glob
import datetime
import time
import pymysql
#from sqlalchemy import create_engine
from sshtunnel import SSHTunnelForwarder
import warnings
warnings.filterwarnings("ignore")

#距离计算函数
def distSLC(vecA,vecB):
    #sin()和cos()以弧度未输入，将float角度数值转为弧度，即*pi/180
    #a经度
    a=sin(vecA[1]*pi/180)*sin(vecB[1]*pi/180)
    b=cos(vecA[1]*pi/180)*cos(vecB[1]*pi/180)*cos(pi*(vecB[0]-vecA[0])/180)
    return arccos(round(a+b,20))*6371.0

# def read_data(f_path,ab_li):
#     data = []
#     with open(f_path,encoding = 'utf-8') as f:
#         csv_reader = csv.reader(f)
#         for row in csv_reader:
#             data.append(row)
#         df_data = pd.DataFrame(data[1:],columns = data[0])
#         #df_data.set_index(in_cl,inplace=True)
#     return df_data.iloc[:,ab_li]
#
#
# def diff_minutes(startTime,endTime):
#     minute_diff = abs((endTime - startTime).total_seconds()/60)
#     return minute_diff


'''
参数：
item:分公司id
order_limit:限制订单数（默认3笔）
dist_limit：限制距离（默认5米）
minute_limit：限制时间（默认5分钟）
'''
def click_farm(org_data, item, order_limit=3, dist_limit=0.005):

    #order_date = org_data.loc[:, 'order_date'][0]
    # order_date=datetime.datetime.strptime(order_date,'%Y/%m/%d').strftime('%Y%m%d')

    part_data = org_data[org_data.index == item]
    part_data = part_data.reset_index(drop=False)
    part_data.set_index('time_segment', inplace=True)

    result = []
    #org_data = org_data[org_data.index == '马鞍山分公司']

    # 选取时间切片
    #print(set(part_data.index))
    for time_sp in set(part_data.index):
        #print(time_sp)
        time_data = part_data[part_data.index == time_sp].reset_index().set_index('order_id')
        # 筛选时间片订单>= 3
        if time_data.shape[0] >= order_limit:
            lens = time_data.shape[0]

            for c_id in range(lens):
                order_id = []
                for d_id in range(lens):
                    if distSLC([float(time_data.iat[c_id, 3]), float(time_data.iat[c_id, 2])],
                               [float(time_data.iat[d_id, 3]), float(time_data.iat[d_id, 2])]) < dist_limit:
                        order_id.append(time_data.index[d_id])
            # 如果起点距离小于5米单量>=3，开始计算终点距离

                if len(order_id) >= order_limit:
                    for o_in in order_id:
                        f_order_id = []
                        for p_id in order_id:
                            if distSLC([float(time_data.at[o_in, 'stopChargePoint_lon']),
                                        float(time_data.at[o_in, 'stopChargePoint_lat'])],
                                       [float(time_data.at[p_id, 'stopChargePoint_lon']),
                                        float(time_data.at[p_id, 'stopChargePoint_lat'])]) < dist_limit:
                                f_order_id.append(p_id)
                        # 终点距离小于5米单量>=3，输出
                        if len(f_order_id) >= order_limit:
                            result.append([item, time_sp, f_order_id])

    order_date = list(part_data['order_date'])[0]
    temp_order = []
    # 打印结果
    for item in result:
        for i in item[2]:
            temp_order.append((order_date, i))
    return temp_order

def get_data():
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

    #创建游标对象
    cur = conn.cursor()

    #取数sqls
    sql = """
    select concat("'",ord.orderSn) order_id,
           SUBSTRING_INDEX(REPLACE(addr.startChargePoint,CONCAT(SUBSTRING_INDEX(addr.startChargePoint,'"lat":',1),'"lat":'),''),',',1) startChargePoint_lat,
           SUBSTRING_INDEX(REPLACE(addr.startChargePoint,CONCAT(SUBSTRING_INDEX(addr.startChargePoint,'"lon":',1),'"lon":'),''),',',1) startChargePoint_lon,
           SUBSTRING_INDEX(REPLACE(addr.stopChargePoint,CONCAT(SUBSTRING_INDEX(addr.stopChargePoint,'"lat":',1),'"lat":'),''),',',1) stopChargePoint_lat,
           SUBSTRING_INDEX(REPLACE(addr.stopChargePoint,CONCAT(SUBSTRING_INDEX(addr.stopChargePoint,'"lon":',1),'"lon":'),''),',',1) stopChargePoint_lon,
           #addr.startChargePoint_lat,
           #addr.startChargePoint_lon,
           #addr.stopChargePoint_lat,
           #addr.stopChargePoint_lon,
           date(ord.createTime) order_date,
           #date(ord.payTimeA) pay_date,
           ord.companyId,
           ord.startChargeTime,
           ord.confirmChargeTime,
           #hour(ord.startChargeTime) hour_segment,
           #minute(ord.startChargeTime) minute_segment,
           12*hour(ord.startChargeTime)+floor(minute(ord.startChargeTime)/5) time_segment
    from paid_order_day_statistics ord
    left join paid_order_assist_info addr on ord.orderSn=addr.orderId
    where ord.createTime >= date_add(curdate(), interval -1 day)
    and ord.createTime < curdate()
    #limit 100
    """
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

    # 处理空值
    org_data = org_data[~org_data['startChargePoint_lat'].isin([''])]
    org_data = org_data[~org_data['startChargePoint_lon'].isin([''])]
    org_data = org_data[~org_data['stopChargePoint_lat'].isin([''])]
    org_data = org_data[~org_data['stopChargePoint_lon'].isin([''])]
    org_data.set_index('companyId', inplace=True)

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
    sql = """insert ignore into clickfarm_rules4(order_date,orderId) values(%s,%s)"""

    # 插入数据
    cur.executemany(sql, results)

    # 必须要执行此操作才能写入到数据库
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()


if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=8)  # 创建4个进程

    start = time.time()
    # 从数据库获取前一天数据
    org_data = get_data()
    t1=time.time()
    print("获取数据用时：", (t1 - start))

    res_lst = []
    # 选取分公司
    for item in set(org_data.index):
        res = pool.apply_async(click_farm,(org_data, item, ))
        res_lst.append(res)

    time.sleep(2)

    # 数据汇总
    results = []
    for r in res_lst:
        #print(r,time.time(),r.get())
        for item in r.get():
            results.append(item)

    pool.close()  # 关闭进程池，表示不能在往进程池中添加进程
    pool.join()  # 等待进程池中的所有进程执行完毕，必须在close()之后调用

    t2 = time.time()
    print("运行用时：", (t2 - t1))


    # 结果去重写入数据库
    write2mysql(set(results))


    end = time.time()
    print("总用时：", (end - start))

    print("Sub-process(es) done.")