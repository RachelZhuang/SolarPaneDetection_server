# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:13:51 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-

from CheckDataUpdate import CheckDataUpdate
import time,urllib2,os,sys

def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
def callbackfunc(downloadedSize, totalSize):
        '''回调函数
        @blocknum: 已经下载的数据块
        @blocksize: 数据块的大小
        @totalsize: 远程文件的大小
        '''
        percent = 100.0 * downloadedSize/totalSize
        if percent > 100:
            percent = 100
        print ("%.2f%%"% percent)
def downloadChunks(url,rep,nom_fic):
        ##url为下载地址，rep为存储文件所在目录,fic为文件名
        try:
          req = urllib2.urlopen(url)
          #if downloaded file is html
          if (req.info().gettype()=='text/html'):
            print "error : file is in html and not an expected binary file"
            lignes=req.read()
            if lignes.find('Download Not Found')>0 :
                  raise TypeError
            else:
                with open("error_output.html","w") as f:
                    #f.write(lines)
                    print "result saved in ./error_output.html"
                    sys.exit(-1)
          #if file too small
          total_size = int(req.info().getheader('Content-Length').strip())
          if (total_size<50000):
             print "Error: The file is too small to be a Landsat Image"
             print url
             sys.exit(-1)
          print nom_fic,total_size
          total_size_fmt = sizeof_fmt(total_size)
                  #download
          downloaded = 0
          CHUNK = 8192
          with open(rep+'/'+nom_fic, 'wb') as fp:
            #start = time.clock()

            print('Downloading {0} ({1}):'.format(nom_fic, total_size_fmt))
            i=0
            while True:
                chunk = req.read(CHUNK)
                downloaded += len(chunk)
                #done = int(50 * downloaded / total_size)
                callbackfunc(downloaded,total_size)
                #sys.stdout.flush()
                if not chunk: break
                fp.write(chunk)
        except urllib2.HTTPError, e:
             if e.code == 500:
                  pass # File doesn't exist
             else:
                  print "HTTP Error:", e.code , url
             return False
        except urllib2.URLError, e:
            print "URL Error:",e.reason , url
            return False

        return rep,nom_fic
                ##################
def DownloadData(basepath,all_results):

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
                response=urllib2.urlopen(Request_URL)
                print("Start downloading data:\n")
                filesize=response.info().get('Content-Length')
                today=time.strftime("%m.%d")
                #today="03.01"
                path=basepath
                if not (os.path.exists(path)): #判断是否存在目录，不存在则创建。

                    os.makedirs(path)
                #os.makedirs("E:\\Data\\Landsat8\\wuhan\\2016\\"+today+"")
                local=path+'\\'+name.strip()+'.tar.gz'
                downloadChunks(Request_URL,"%s"%path,name.strip()+'.tar.gz')

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

# lat="30.5931"
# lon="114.3054"
# start="05/02/2016"
# end="05/06/2016"
# basepath='D:\Data\\'
# all_results=CheckDataUpdate(lat,lon,start,end)
# if(len(all_results)!=0):
#    DownloadData(basepath,all_results)



