# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 10:50:58 2016

@author: Administrator
"""
from CheckDataUpdate import CheckDataUpdate
from DownloadData import DownloadData
from DecompressGzip import DecompressGzip
from ProcessImage import ProcessImage
from createMxdDocument import createMxdDocument
from publishHelper import Publish
from importDatabase import importDatabase
import time,os
import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

lat="30.5931"
lon="114.3054"
# start="05/02/2016"
# end="05/06/2016"
# #basepath='D:\\Data\\Landsat8\\wuhan\\2016\\'+time.strftime('%Y-%m-%d-%H-%I-%M-%S',time.localtime(time.time()))
#
#connection_file_path=basepath
#mxdfolder=basepath
#wrkspc=basepath
serverName="localhost"
userName="admin"
password="jack121"
#
# SECONDS_PER_DAY = 24 * 60 * 60
def main():
    try:
        start=time.strftime('%m/%d/%Y',time.localtime(time.time()-86400))
        end=time.strftime('%m/%d/%Y',time.localtime(time.time()))
        all_results=CheckDataUpdate(lat,lon,start,end)
        if len(all_results)==0:
            print "No data Update"
        else:
          basepath='D:\\Data\\Landsat8\\wuhan\\2016\\'+time.strftime('%Y.%m.%d',time.localtime(time.time()))
          DownloadData(basepath,all_results)
          DecompressGzip(basepath)
          ProcessImage(basepath)
          createMxdDocument(r"D:\ly\hb\123456.mxd",basepath)
          Publish(basepath,userName,password,serverName,basepath)
          importDatabase(basepath)
          #basepath='D:\\Data\\Landsat8\\wuhan\\2016\\'+time.strftime('%Y-%m-%d-%H-%I-%M',time.localtime(time.time()))
          #os.makedirs(basepath)
    except Exception as e:
        print ("open error: ", e)

scheduler = BlockingScheduler()
scheduler.add_job(main, "cron", second="*/86400")

try:
    scheduler.start()
except (KeyboardInterrupt, SystemExit):
    scheduler.shutdown()








