# -*- coding: utf-8 -*-
"""
Created on Fri Jun  3 10:50:58 2016

@author: Administrator
"""
from PIL import Image,ImageFilter
import numpy as np
import cv2
import os
def processOneImage(filePath):
    img = cv2.imread(filePath, 0)
    img = cv2.GaussianBlur(img,(3,3),0)
    canny = cv2.Canny(img, 50, 150)
    dst=img
    cv2.bitwise_not(canny,dst)
    filePath=filePath.replace(".TIF","_1.TIF")
    #im2.save(filePath)
    cv2.imwrite(filePath,dst)
def ProcessImage(dirpath):
    try:
        files = os.listdir(dirpath)
        print(files)
        for f in files:
            print(f)
            if f.endswith(".TIF"):
                filePath=dirpath+'\\'+f
                processOneImage(filePath)

    except Exception as e:
        print ("open error: ", e)
        return

# path="D:\\Data\\Landsat8\\wuhan\\2016\\10.03"
# ProcessImage(path)