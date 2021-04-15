#!/usr/bin/env python
# -*- coding=utf-8 -*-

import json
import sys
import time

import ssl
from datetime import datetime

try:
    import urllib2 as httplib   # 2.x
except Exception:
    import urllib.request as httplib  # 3.x

try:
    import MySQLdb  # pip install MySQL-python
except:
    import pymysql as MySQLdb  # pip install MySQLdb

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

db = MySQLdb.connect(host="127.0.0.1", user="admin", passwd="admin", db="mydatabase")
cursor = db.cursor()

plt.rcParams['font.sans-serif'] = ['SimSun']  # 步驟一（替換sans-serif字型）
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）

cursor.execute("SELECT MAX(count) FROM watertable")
result = cursor.fetchall()

#print(result)
print(result[0][0])

if result[0][0] is None:
    countW=1
else:
    countW=result[0][0]+1

while True:
    context = ssl._create_unverified_context()

    url="https://quality.data.gov.tw/dq_download_json.php?nid=133578&md5_url=ac39a7025bb0581ceb2eec2a28199191"
    #url="https://epcs.water.gov.tw/OpenData/v1/api/values"
    req = httplib.Request(url)

    try:
        reponse = httplib.urlopen(req, context=context)
        if reponse.code==200:
            if (sys.version_info > (3, 0)):
                contents = reponse.read()
            else:
                contents = reponse.read()
            #print(contents)
            data=json.loads(contents)
            if (len(data) > 1):  # 確認是否有資料
                now = datetime.now()  # 現在時間
                current_time = now.strftime("%Y%m%d%H%M%S")  # 印出時間的格式
                print("現在時間 =", current_time)
                #with open('台灣自來水公司產水監控資料' + str(current_time) + '.json', 'w') as f:  # 處存
                #    json.dump(data, f)
    except:
        sql2 = """
                     CREATE TABLE `watertable` (
                      `id` int(12) NOT NULL,
                      `station_name` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
                      `pH_value` float NOT NULL,
                      `turbidity` float NOT NULL,
                      `residual_chlorine` float NOT NULL,
                      `datetime` datetime NOT NULL,
                      `count` int(11) NOT NULL
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;
                """
        cursor.execute(sql2)
        db.commit()
    #print(data)

    listStation_name=[]
    listPH_value=[]
    listTurbidity=[]
    listResidual_chlorine=[]
    listCount=[]

    count1=0

    for id in data:
        #station_name=data[id]['station_name']
        station_name = id['station_name']
        #station_name = station_name[0:2]
        pH_value=float(id['pH_value'])
        turbidity=float(id['turbidity'])
        residual_chlorine=float(id['residual_chlorine'])

        if station_name == "龍潭淨水場" and count1 == 0:
            station_name = "龍潭淨水場(1)"
            count1 += 1
        elif station_name == "龍潭淨水場" and count1 == 1:
            station_name = "龍潭淨水場(2)"
            count1 += 1

        listStation_name.append(station_name)
        listPH_value.append(pH_value)
        listTurbidity.append(turbidity)
        listResidual_chlorine.append(residual_chlorine)

        sql = "INSERT INTO `watertable` (`id`   , `station_name`, `pH_value`, `turbidity`, `residual_chlorine`, `datetime`, `count`) " +\
              "VALUES (NULL, '"+station_name+"', '"+id['pH_value']+"', '"+id['turbidity']+"', '"+id['residual_chlorine']+"', now() , '"+str(countW)+" ');"
        cursor.execute(sql)
    countW+=1 #第幾次寫入資料庫

    db.commit()

    plt.clf()

    plt.xticks(rotation=45)

    plt.plot(listStation_name, listPH_value, 'r-',label='pH值')
    plt.plot(listStation_name, listTurbidity, 'b-',label='濁度')
    plt.plot(listStation_name, listResidual_chlorine,'g-',label='餘氯')
    plt.title('台灣自來水公司產水監控')
    plt.legend()

    #plt.pause(60*60)

    time.sleep(60*60)  # 1h
