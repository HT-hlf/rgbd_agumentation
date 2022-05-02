# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/16 14:06
# @File       : cat_four_image.py
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
image_path_2=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_bk_6'
image_path_3=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_bk_7'
image_path_4=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_m_4'

data_aug_save_path=r'test'
data_aug_rgb_save_path=os.path.join(data_aug_save_path,'rgb')
creat_dir(data_aug_rgb_save_path)
data_aug_annotation_save_path=os.path.join(data_aug_save_path,'annotation')
creat_dir(data_aug_annotation_save_path)

rgb_path_1=os.path.join(image_path_1,'rgb')
anno_path_1=os.path.join(image_path_1,'annotation')
rgb_image_list_1=os.listdir(rgb_path_1)
rgb_path_2=os.path.join(image_path_2,'rgb')
anno_path_2=os.path.join(image_path_2,'annotation')
rgb_image_list_2=os.listdir(rgb_path_2)
rgb_path_3=os.path.join(image_path_3,'rgb')
anno_path_3=os.path.join(image_path_3,'annotation')
rgb_image_list_3=os.listdir(rgb_path_3)
rgb_path_4=os.path.join(image_path_4,'rgb')
anno_path_4=os.path.join(image_path_4,'annotation')
rgb_image_list_4=os.listdir(rgb_path_4)

generate_dataset_num=1000
for i in range(generate_dataset_num):
    data_aug_image_name='data_aug_link_4_' + str(i) + '.jpg'
    data_aug_image=data_aug_rgb_save_path+'/'+data_aug_image_name
    data_aug_annotation = data_aug_annotation_save_path + '/' + 'data_aug_link_4_' + str(i) + '.xml'

    random_1=random.randint(0,len(rgb_image_list_1)-1)
    random_rgb_1=rgb_image_list_1[random_1]
    annotation_1=anno_path_1+'/' + random_rgb_1.rstrip('jpg')+'xml'
    args=readXML(annotation_1)
    # print(args)
    # '775', '532'
    writeXML(data_aug_annotation, 'rgb', data_aug_image_name,
             data_aug_image, '1550', '1064', '3',
             'person',*args)
    rgb_image_path_1 = rgb_path_1 + '/' + random_rgb_1
    rgb_image_data_1 = cv2.imread(rgb_image_path_1)

    random_2 = random.randint(0, len(rgb_image_list_2) - 1)
    random_rgb_2 = rgb_image_list_2[random_2]
    annotation_2 = anno_path_2 + '/' + random_rgb_2.rstrip('jpg') + 'xml'
    (xmin,ymin,xmax,ymax) = readXML(annotation_2)
    args=(xmin,str(int(ymin)+532),xmax,str(int(ymax)+532))
    # print(args)
    append(data_aug_annotation, 'person', False,*args)
    rgb_image_path_2 = rgb_path_2 + '/' + random_rgb_2
    rgb_image_data_2 = cv2.imread(rgb_image_path_2)

    random_3 = random.randint(0, len(rgb_image_list_3) - 1)
    random_rgb_3 = rgb_image_list_3[random_3]
    annotation_3 = anno_path_3 + '/' + random_rgb_3.rstrip('jpg') + 'xml'
    (xmin,ymin,xmax,ymax) = readXML(annotation_3)
    args=(str(int(xmin)+775), ymin, str(int(xmax)+775), ymax)
    # print(args)
    append(data_aug_annotation, 'person',False, *args)
    rgb_image_path_3 = rgb_path_3 + '/' + random_rgb_3
    rgb_image_data_3 = cv2.imread(rgb_image_path_3)

    random_4 = random.randint(0, len(rgb_image_list_4) - 1)
    random_rgb_4 = rgb_image_list_4[random_4]
    annotation_4 = anno_path_4 + '/' + random_rgb_4.rstrip('jpg') + 'xml'
    (xmin,ymin,xmax,ymax) = readXML(annotation_4)
    args=(str(int(xmin)+775), str(int(ymin)+532), str(int(xmax)+775), str(int(ymax)+532))
    # print(args)
    append(data_aug_annotation,'person',True, *args)
    rgb_image_path_4 = rgb_path_4 + '/' + random_rgb_4
    rgb_image_data_4 = cv2.imread(rgb_image_path_4)

    img_v_1 = np.vstack((rgb_image_data_1, rgb_image_data_2))
    img_v_2 = np.vstack((rgb_image_data_3, rgb_image_data_4))
    img_sum = np.hstack((img_v_1, img_v_2))
    print(img_sum.shape)
    cv2.imwrite(data_aug_image, img_sum)
    # cv2.imshow('ht', img_sum)
    # cv2.imshow('ht', img_v_1)
    # cv2.waitKey(1)



# for rgb_image in rgb_image_list:
#     rgb_image_path = rgb_path + '/' + rgb_image
#     rgb_image_data=cv2.imread(rgb_image_path)
#     cv2.imshow('ht',rgb_image_data)
#     cv2.waitKey(0)