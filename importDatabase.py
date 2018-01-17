# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:13:51 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
import mysql.connector
import os
#导入模块,将解压后的原始数据导入Mysql数据库

def improtMySQL(name,mxdPath,url,date,age):

    config={'host':'127.0.0.1',#默认127.0.0.1
         'user':'root',
         'password':'',
         'port':3306 ,#默认即为3306
         'database':'test',
         'charset':'utf8'#默认即为utf8
         }
    try:
      cnn=mysql.connector.connect(**config)
    except mysql.connector.Error as e:
      print('connect fails!{}'.format(e))

    cursor=cnn.cursor()
    try:
       sql_insert="insert into node_user (name,age,date,mxdPath,url) values (%s,%s,%s,%s,%s)"
       #data=('li',0,'2016-06-05','li','li')
       data=(name,age,date,mxdPath,url)
       cursor.execute(sql_insert,data)
    except mysql.connector.Error as e:
        print ('insert datas error !{}'.format(e))
    finally:
        cursor.close()
        cnn.close()


def importOneBand(FILE_NAME_BAND_1,dirPath,name,date):
    mxdPath=dirPath+"\\"+FILE_NAME_BAND_1+".mxd"
    url="http://127.0.0.1:6080/arcgis/rest/services/"+FILE_NAME_BAND_1+"/MapServer"
    age=0

    improtMySQL(name,mxdPath,url,date,age)

    mxdPath=dirPath+"\\"+FILE_NAME_BAND_1+"_1.mxd"
    url="http://127.0.0.1:6080/arcgis/rest/services/"+FILE_NAME_BAND_1+"_1/MapServer"
    age=1

    improtMySQL(name,mxdPath,url,date,age)

def importDatabase(dirPath):
    try:
        files = os.listdir(dirPath)
        print(files)
        for file in files:
            #print(f)
            FILE_NAME_BAND_SET={'_B1','_B2','_B3','_B4','_B5','_B6','_B7','_B8','_B9','_B10','_B11','_BQA'}
            if file.endswith(".txt"):
                filePath=dirPath+'\\'+file
                #print(f1)
                content=open(filePath,'r').readlines()
                name=content[13][-11:-2]
                date=content[20][-11:-1]
                FILE_NAME_BAND_1=content[44][-30:-6]
                for band in FILE_NAME_BAND_SET:
                    FILE_NAME_BAND_1= FILE_NAME_BAND_1.replace("_B1",band)
                    importOneBand(FILE_NAME_BAND_1,dirPath,name,date)
    except Exception as e:
        print ("open error: ", e)


#importDatabase("D:\\Data\\Landsat8\\wuhan\\2016\\10.03")














#importDatabase("D:\\Data\\Landsat8\\wuhan\\2016\\10.03")
