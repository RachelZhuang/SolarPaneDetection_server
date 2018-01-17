# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:13:51 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 25 14:09:18 2016

@author: Administrator
"""
import urllib.request
import urllib.parse
import http.cookiejar
from bs4 import BeautifulSoup
import mysql.connector
import ssl
import time
import sys
import os,lxml

def AutoDownload_landsat8():
    #登录的主页面
    #ssl._create_default_https_context = ssl._create_unverified_context
    hosturl = "https://ers.cr.usgs.gov" ##自己填写
    #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
    posturl = 'https://ers.cr.usgs.gov/login/' ##从数据包中分析出，处理post请求的url

    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj =http.cookiejar.LWPCookieJar()
    cookie_support = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(cookie_support, urllib.request.HTTPHandler)
    urllib.request.install_opener(opener)
    #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
    h = urllib.request.urlopen(hosturl)
    #构造header，一般header至少要包含一下两项。这两项是从抓到的包里分析得出的。
    #headers = {'Content-Type':'application/x-www-form-urlencoded',
    #           'Origin':'https://ers.cr.usgs.gov',
    #           'Host':'ers.cr.usgs.gov',
    #           'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
    #           'Referer' : 'https://ers.cr.usgs.gov/login/'}
    ##构造Post数据，他也是从抓大的包里分析得出的。
    #postData = {'username':'xiaopianzz@gmail.com',
    #            'password':'x199311728',
    #            '__ncforminfo':'_XYklWQUbeIUyVBMFqXtyifk8wFjl6JDXHUnJEtTNk9NaaaqQHLCgJ0j6mV8T_qJsX9T5GIXPsduJsPzrkH5z6zp2N6D8cPQXB33LDPiMG0='
    #            }

    response=urllib.request.urlopen(posturl)
    pageContent=response.read().decode('utf-8')
    page=lxml.etree.HTML(pageContent)
    csrf_token=page.xpath('//input[@id="csrf_token"]/@value')[0]
    _ncforminfo=page.xpath('//input[@name="__ncforminfo"]/@value')[0]



    headers = {'Content-Type':'application/x-www-form-urlencoded',
                       'Origin':'https://ers.cr.usgs.gov',
                       'Host':'ers.cr.usgs.gov',
                       'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
                       'Referer' : 'https://ers.cr.usgs.gov/login/'}


    postData={'username':'jams_hui',
                'password':'zxc2399717',
                'csrf_token':csrf_token,
                '_ncforminfo':_ncforminfo,
    }
    postData = urllib.parse.urlencode(postData).encode('utf-8')

    request = urllib.request.Request(posturl, postData, headers)
    #print request
    response = urllib.request.urlopen(request)
    text = response.read()
    #print text

    ##成功显示登陆后的主界面##
    settings = urllib.request.urlopen('http://earthexplorer.usgs.gov/')
    #print settings.read().decode('utf-8')

    #发送搜索请求
    url1='http://earthexplorer.usgs.gov/tabs/save'
    headers1={'Content-Type':'application/x-www-form-urlencoded',
              'Host':'earthexplorer.usgs.gov',
              'Origin':'http://earthexplorer.usgs.gov',
              'Proxy-Connection':'keep-alive',
              'Referer':'http://earthexplorer.usgs.gov/',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
              'X-Requested-With':'XMLHttpRequest'}
        #    lat=GUI.on_pushButton_ok_clicked()
        #    lon=GUI.on_pushButton_ok_clicked()
        #    start=GUI.on_pushButton_ok_clicked()
        #    end=GUI.on_pushButton_ok_clicked()
    lat="30.5931"
    lon="114.3054"
    #start=time.strftime('%d/%m/%Y')
    #end=time.strftime('%d/%m/%Y')
    start="05/02/2016"
    end="05/06/2016"
    data1={'data':'{"tab":1,"destination":2,"coordinates":[{"c":"0","a":"'+lat+'","o":"'+lon+'"}],"format":"dms","dStart":"'+start+'","dEnd":"'+end+'","searchType":"Std","num":"5","months":["","0","1","2","3","4","5","6","7","8","9","10","11"],"pType":"polygon"}'}
    data_1=urllib.parse.urlencode(data1).encode('utf-8')
    req1=urllib.request.Request(url1,data_1,headers1)  #发送第一个save的post请求
    res1=urllib.request.urlopen(req1)

    url2='http://earthexplorer.usgs.gov/tabs/save'
    headers2={'Content-Type':'application/x-www-form-urlencoded',
              'Host':'earthexplorer.usgs.gov',
              'Origin':'http://earthexplorer.usgs.gov',
              'Proxy-Connection':'keep-alive',
              'Referer':'http://earthexplorer.usgs.gov/',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
              'X-Requested-With':'XMLHttpRequest'}
    data2={'data':'{"tab":2,"destination":4,"cList":["4923"],"selected":4923}'}
    data2=urllib.parse.urlencode(data2).encode('utf-8')
    req2=urllib.request.Request(url2,data=data2,headers=headers2)  #发送第二个save的post请求
    res2=urllib.request.urlopen(req2)

    url3='http://earthexplorer.usgs.gov/result/index'
    headers3={'Content-Type':'application/x-www-form-urlencoded',
              'Host':'earthexplorer.usgs.gov',
              'Origin':'http://earthexplorer.usgs.gov',
              'Proxy-Connection':'keep-alive',
              'Referer':'http://earthexplorer.usgs.gov/',
              #'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
              'X-Requested-With':'XMLHttpRequest'}
    data3={'collectionId':'4923'}
    data3=urllib.parse.urlencode(data3).encode('utf-8')
    req3=urllib.request.Request(url3,data3,headers3)  #发送第三个index的post请求

    res=urllib.request.urlopen(req3)
    searchtext=res.read()


    #下载界面
    #soup=BeautifulSoup(searchtext,"lxml")
    #all_results = soup.find_all(title='Show Metadata and Browse')  #查找所有的标签
    #i=0
    #file_sum=0
    #path='E:\Data\Landsat8'
    #for result in all_results:  #查找标签结果为三个文件名，三个None，所以奇数号的结果才是我们需要的结果
    #    i=i+1
    #    if i==1:
    #    #       print(result.string)
    #        name=result.string
    #        wo=name.strip()
    ##               print(wo)  #文件名的前后有很多空格，name.strip()的作用就是消除字符串里的空格
    ##        self.textBrowser.append(wo)
    #        Request_URL='http://earthexplorer.usgs.gov/download/4923/'+wo+'/STANDARD/EE'
    #        response=urllib.request.urlopen(Request_URL)
    ##       file_size=int(response.info().get('Content-Length',0))
    #        print('a')
    #        filesize=response.info().get('Content-Length')
    #        print('b')
    ##                print(file_size)
    ##                file_sum+=file_size
    #
    #        config={'host':'127.0.0.1',#默认127.0.0.1
    #                'user':'root',
    #                'password':'x199311728',
    #                'port':3306 ,#默认即为3306
    #                'database':'data_206',
    #                'charset':'utf8'#默认即为utf8
    #                }
    #        try:
    #            cnn=mysql.connector.connect(**config)
    #        except mysql.connector.Error as e:
    #            print('connect fails!{}'.format(e))
    #
    #        cursor=cnn.cursor()
    #        sql_insert="insert into data (filename, filedate,savepath,size) values ('"+wo+"', '"+start+"','"+path+"','"+filesize+"')"
    #        print('c')
    #        cursor.execute(sql_insert)
    #        print('d')
    #        cursor.close()
    #        print(1)
    #        cnn.close()
    #        print(2)
    ##                print(file_sum)
    ##                file_size=int(meta.getheaders("Content-Length")[0])
    ##                file_size=meta.getheader('Content-Length')
    ##                self.textBrowser.append(file_size)
    #        data_download=response.read()
    #        print('e')
    #        f=open('E:\Data\Landsat8\\'+name.strip()+'.tar.gz','wb')
    #        print('f')
    #        f.write(data_download)
    #        print('g')
    #        f.close()
    #    else:
    #        i=0
    def callbackfunc(blocknum, blocksize, totalsize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        print ("%.2f%%"% percent)
    #下载界面
    soup=BeautifulSoup(searchtext,"lxml")
    all_results = soup.find_all(title='Show Metadata and Browse')  #查找所有的标签
    if all_results==[]:
        print("No data update")
    else:
        i=0
        for result in all_results:  #查找标签结果为三个文件名，三个None，所以奇数号的结果才是我们需要的结果
            i=i+1
            if i==1:
                #        print(result.string)
                name=result.string
                #        print name.strip()  #文件名的前后有很多空格，name.strip()的作用就是消除字符串里的空格
                Request_URL='http://earthexplorer.usgs.gov/download/4923/'+name.strip()+'/STANDARD/EE'
                response=urllib.request.urlopen(Request_URL)
                print("Start downloading data:\n")
                filesize=response.info().get('Content-Length')
                today=time.strftime("%m.%d")
                #today="03.01"
                path='D:\Data\Landsat8\wuhan\\2016\\'+today+''
                if not (os.path.exists(path)): #判断是否存在目录，不存在则创建。

                    os.makedirs("D:\\Data\\Landsat8\\wuhan\\2016\\"+today+"")
                #os.makedirs("E:\\Data\\Landsat8\\wuhan\\2016\\"+today+"")
                local=''+path+'\\'+name.strip()+'.tar.gz'
                urllib.request.urlretrieve(Request_URL, local, callbackfunc)
    #            config={'host':'127.0.0.1',#默认127.0.0.1
    #                    'user':'root',
    #                    'password':'123456789',
    #                    'port':3306 ,#默认即为3306
    #                    'database':'data_206',
    #                    'charset':'utf8'#默认即为utf8
    #                    }
    #            try:
    #                cnn=mysql.connector.connect(**config)
    #            except mysql.connector.Error as e:
    #                print('connect fails!{}'.format(e))
    #
    #            cursor=cnn.cursor()
    #            #path='E:\Data\Landsat8\wuhan'
    #            sql_insert="insert into data (filename, filedate,savepath,size) values ('"+name.strip()+"', '"+start+"','"+path.replace("\\", "\\\\")+"','"+filesize+"')"
    #            cursor.execute(sql_insert)
    #            cursor.close()
    #            cnn.close()
                #        response=urllib2.urlopen(Request_URL)
                #        data=response.read()
                #        f=open('D:\Data\Landsat8\\'+name.strip()+'.tar.gz','wb')
                #        f.write(data)
                #        f.close()
            else:
                i=0
        print ("Download completed!")
   # dirpath=r'E:\Data\Landsat8\wuhan\\2016\\'+today+''
AutoDownload_landsat8()
if __name__=="__main__":
     sys.exit()

