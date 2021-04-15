#!/usr/bin/env
# -*- coding: utf-8 -*-    

import pymysql as MySQLdb             #  pip install MySQLdb

import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

plt.rcParams['font.sans-serif'] = ['SimSun']  # 步驟一（替換sans-serif字型）
plt.rcParams['axes.unicode_minus'] = False  # 步驟二（解決座標軸負數的負號顯示問題）

db = MySQLdb.connect(host="127.0.0.1", user="admin", passwd="admin", db="mydatabase")
cursor = db.cursor()

import matplotlib.pyplot as plt

def funPH(plotStyle='r-',num=0):
    listId=[]           #ID
    listName=[]         #名稱
    listPh=[]           #PH
    listTurbidity=[]    #濁度
    listRc=[]           #餘氯
    listDatetime=[]     #時間

    cursor.execute("SELECT MAX(count) FROM watertable")
    result = cursor.fetchall()

    countNum= result[0][0]
    t1=countNum-num

    sql2 = "SELECT * FROM `watertable` where count="+str(t1) # 不准用SQL的 max() ,不能用　order by
    cursor.execute(sql2)
    result = cursor.fetchall()

    for record in result:
        print(" id:",record[0]," 淨水場名稱:",record[1],"  pH值:" ,record[2],"  濁度:" ,record[3],
              "  餘氯:" ,record[4]," 時間:" ,record[5],)
        listId.append(int(record[0]))
        listName.append(record[1])
        listPh.append(record[2])
        listTurbidity.append(record[3])
        listRc.append(record[4])
        listDatetime.append(record[5])

    plt.xticks(rotation=270)

    plt.plot(listName,listPh, plotStyle,label=str(record[5]))

funPH(plotStyle='r-',num=20)
funPH(plotStyle='b-',num=10)
funPH(plotStyle='g-',num=0)
plt.title('title')
plt.legend()
plt.show()

