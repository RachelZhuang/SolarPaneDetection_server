#coding=utf-8
import cv2
import numpy as np


img = cv2.imread("D:\\LC81230392016125LGN00_BQA.TIF", 0)
cv2.imshow('Canny', img)
cv2.waitKey(0)

img = cv2.GaussianBlur(img,(3,3),0)
canny = cv2.Canny(img, 50, 150)

dst=img

cv2.bitwise_not(canny,dst)

cv2.imwrite('D:\\test.TIF',dst)

