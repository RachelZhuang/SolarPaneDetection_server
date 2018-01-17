# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:14:54 2016

@author: Administrator
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 26 20:01:12 2016

@author: Administrator
"""
#解压模块
import os
import tarfile
def DecompressGzip(dirpath):
    try:
        files = os.listdir(dirpath)
        print(files)
        for f in files:
            print(f)
            if f.endswith(".tar.gz"):
               f1=dirpath+'\\'+f
               print(f1)
               tar = tarfile.open(f1)#需要解压的文件
               print("正在解压")
               tar.extractall(path=dirpath)
            tar.close()
    except Exception as e:
        print ("open error: ", e)
        return
# today=time.strftime("%m.%d")
# dirpath=r'D:\Data\Landsat8\wuhan\2016\\'+today+''
# print(dirpath)
# DecompressGzip(dirpath)
# sys.exit()