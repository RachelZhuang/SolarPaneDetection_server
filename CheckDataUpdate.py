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
#lat="30.5931"
#lon="114.3054"
#start=time.strftime('%d/%m/%Y')
#end=time.strftime('%d/%m/%Y')
#start="05/02/2016"
#end="05/06/2016"
#basepath='D:\Data\\'

#下载模块，输入变量：lat代表北纬,lon代表东经,北纬30,东经114代表武汉,start代表起始时间，end代表截止时间，basepath代表存储路径，输入格式如示例所示
#此版本代码在python2.7环境下运行
import urllib2
import urllib
import cookielib,lxml
from bs4 import BeautifulSoup
def CheckDataUpdate(lat,lon,start,end):
    #登录的主页面
    hosturl = "https://ers.cr.usgs.gov" ##自己填写
    #post数据接收和处理的页面（我们要向这个页面发送我们构造的Post数据）
    posturl = 'https://ers.cr.usgs.gov/login/' ##从数据包中分析出，处理post请求的url

    #设置一个cookie处理器，它负责从服务器下载cookie到本地，并且在发送请求时带上本地的cookie
    cj =cookielib.LWPCookieJar()
    cookie_support =urllib2.HTTPCookieProcessor(cj)
    opener =urllib2.build_opener(cookie_support,urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    #打开登录主页面（他的目的是从页面下载cookie，这样我们在再送post数据时就有cookie了，否则发送不成功）
    h =urllib2.urlopen(hosturl)
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

    response=urllib2.urlopen(posturl)
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
    postData =urllib.urlencode(postData).encode('utf-8')

    request =urllib2.Request(posturl, postData, headers)
    #print request
    response =urllib2.urlopen(request)
    text = response.read()
    #print text

    ##成功显示登陆后的主界面##
    settings =urllib2.urlopen('http://earthexplorer.usgs.gov/')
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
    #lat="30.5931"
    #lon="114.3054"
    #start=time.strftime('%d/%m/%Y')
    #end=time.strftime('%d/%m/%Y')
    #start="05/02/2016"
    #end="05/06/2016"
    data1={'data':'{"tab":1,"destination":2,"coordinates":[{"c":"0","a":"'+lat+'","o":"'+lon+'"}],"format":"dms","dStart":"'+start+'","dEnd":"'+end+'","searchType":"Std","num":"5","months":["","0","1","2","3","4","5","6","7","8","9","10","11"],"pType":"polygon"}'}
    data_1=urllib.urlencode(data1).encode('utf-8')
    req1=urllib2.Request(url1,data_1,headers1)  #发送第一个save的post请求
    res1=urllib2.urlopen(req1)

    url2='http://earthexplorer.usgs.gov/tabs/save'
    headers2={'Content-Type':'application/x-www-form-urlencoded',
              'Host':'earthexplorer.usgs.gov',
              'Origin':'http://earthexplorer.usgs.gov',
              'Proxy-Connection':'keep-alive',
              'Referer':'http://earthexplorer.usgs.gov/',
              'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
              'X-Requested-With':'XMLHttpRequest'}
    data2={'data':'{"tab":2,"destination":4,"cList":["4923"],"selected":4923}'}
    data2=urllib.urlencode(data2).encode('utf-8')
    req2=urllib2.Request(url2,data=data2,headers=headers2)  #发送第二个save的post请求
    res2=urllib2.urlopen(req2)

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
    data3=urllib.urlencode(data3).encode('utf-8')
    req3=urllib2.Request(url3,data3,headers3)  #发送第三个index的post请求

    res=urllib2.urlopen(req3)
    searchtext=res.read()

    #下载界面
    soup=BeautifulSoup(searchtext,"lxml")
    all_results = soup.find_all(title='Show Metadata and Browse')  #查找所有的标签

    return all_results