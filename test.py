# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/30 21:04
# @File       : test.py
# @Software   : PyCharm
import cv2

image_raw_path='test/image_raw.jpg'
image_dst_path='test/image_dst.jpg'
image_raw=cv2.imread(image_raw_path)
print(image_raw.shape)
image_dst=cv2.imread(image_dst_path,0)
print(image_dst.shape)