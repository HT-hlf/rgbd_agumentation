# coding:utf-8
# @Author     : HT
# @Time       : 2022/4/2 21:35
# @File       : generate_shape_img.py
# @Software   : PyCharm

import cv2
import numpy as np
import os
def creat_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
num=416
img = np.zeros((num, num), np.uint8)
# 浅灰色背景
img.fill(255)
creat_dir('shape_img/')
filename='shape_img/'+'ht_'+str(num)+'.jpg'
cv2.imwrite(filename,img)
# cv2.imshow('img', img)
# cv2.waitKey(0)
