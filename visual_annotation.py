# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/28 10:13
# @File       : visual_annotation.py
# @Software   : PyCharm

import os
import cv2
import random
import numpy as np
from read_write_xml_detect import readXML,writeXML,append
def creat_dir(out_dir):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

image_path_1=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_bk_5'

rgb_path_1=os.path.join(image_path_1,'rgb')
depth_path_1=os.path.join(image_path_1,'depth')
anno_path_1=os.path.join(image_path_1,'annotation')
rgb_image_list_1=os.listdir(rgb_path_1)

generate_dataset_num=1000
for i in range(generate_dataset_num):
    random_1 = random.randint(0, len(rgb_image_list_1) - 1)
    random_rgb_1 = rgb_image_list_1[random_1]
    annotation_1 = anno_path_1 + '/' + random_rgb_1.rstrip('jpg') + 'xml'
    args = readXML(annotation_1)
    # print(args)

    rgb_image_path_1 = rgb_path_1 + '/' + random_rgb_1
    rgb_image_data_1 = cv2.imread(rgb_image_path_1)

    depth_image_path_1 = depth_path_1 + '/' + random_rgb_1
    depth_image_data_1 = cv2.imread(depth_image_path_1)

    depth_image_data_1_rect=cv2.rectangle(depth_image_data_1,(int(args[0]),int(args[1])),(int(args[2]),int(args[3])), (0,0,255), 2)
    
    cv2.imshow('ht',depth_image_data_1_rect)
    cv2.waitKey(0)


