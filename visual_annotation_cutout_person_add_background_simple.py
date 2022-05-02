# coding:utf-8
# @Author     : HT
# @Time       : 2022/3/28 10:13
# @File       : visual_annotation.py
# @Software   : PyCharm
#无太多修改，较上版
import os
import cv2
import random
import numpy as np
from read_write_xml_detect import readXML,writeXML,append
def creat_dir(out_dir):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

image_path_1=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_bk_5'
dst_background_depth_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_depths'
dst_background_rgb_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_images'
rgb_path_1=os.path.join(image_path_1,'rgb')
depth_path_1=os.path.join(image_path_1,'depth')
anno_path_1=os.path.join(image_path_1,'annotation')
rgb_image_list_1=os.listdir(rgb_path_1)
dst_background_depth_list=os.listdir(dst_background_depth_path)

generate_dataset_num=1000
middle_the=20
cutout_the=10
def normalize_depth_image(img):
    img_max = np.max(img)
    img_min = np.min(img)
    # heatmap = np.maximum(heatmap, 0)
    img_output = (img-img_min) /(img_max-img_min)*255
    return img_output.astype(np.uint8)
def calcAndDrawHist(image, color,h_num=256):
    hist = cv2.calcHist([image], [0], None, [h_num], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256,256, 3], np.uint8)
    hpt = int(0.9 * 256)

    for h in range(h_num):
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (int(h/h_num*256), 256), (int(h/h_num*256), 256 - intensity), color)

    return histImg
def calcAndDrawHist_max_pixle_value_cutout_person(image, color,h_num=256):
    hist = cv2.calcHist([image], [0], None, [h_num], [0.0, 255.0])
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)
    histImg = np.zeros([256,256, 3], np.uint8)
    hpt = int(0.9 * 256)

    max_gray_scale_value=-1
    max_gray_scale_value_count = 0
    for h in range(h_num):
        if hist[h] >max_gray_scale_value_count and h>5:
            max_gray_scale_value_count=hist[h]
            max_gray_scale_value=h
        intensity = int(hist[h] * hpt / maxVal)
        cv2.line(histImg, (int(h/h_num*256), 256), (int(h/h_num*256), 256 - intensity), color)
    return histImg,max_gray_scale_value
for i in range(generate_dataset_num):

    random_1 = random.randint(0, len(rgb_image_list_1) - 1)
    random_rgb_1 = rgb_image_list_1[random_1]
    annotation_1 = anno_path_1 + '/' + random_rgb_1.rstrip('jpg') + 'xml'

    random_2 = random.randint(0, len(dst_background_depth_list) - 1)
    random_depth_2 =dst_background_depth_list[random_2]
    random_dst_background_depth_all_name = dst_background_depth_path+'/' + random_depth_2
    random_dst_background_rgb_all_name = dst_background_rgb_path + '/' + random_depth_2.rstrip('png')+'jpg'
    # print(random_dst_background_rgb_all_name )
    random_dst_background_depth=cv2.imread(random_dst_background_depth_all_name)
    random_dst_background_rgb = cv2.imread(random_dst_background_rgb_all_name)
    # print('random_dst_background_rgb',random_dst_background_rgb.shape)


    #读取标注框
    xmin,ymin,xmax,ymax= readXML(annotation_1)
    xmin, ymin, xmax, ymax=int(xmin),int(ymin),int(xmax),int(ymax)
    # print(args)

    rgb_image_path_1 = rgb_path_1 + '/' + random_rgb_1
    rgb_image_data_1 = cv2.imread(rgb_image_path_1)

    depth_image_path_1 = depth_path_1 + '/' + random_rgb_1
    depth_image_data_1 = cv2.imread(depth_image_path_1)
    # cv2.imshow('depth_image_data_1',depth_image_data_1)
    print('depth_image_data_1',depth_image_data_1.shape)
    # print(depth_image_data_1.shape)
    # labelimg标注的标注框的范围是从1开始计，到图像的尺寸（闭合）
    #将标注框抠出来
    depth_image_data_1_person=depth_image_data_1[ymin-1:ymax,xmin-1:xmax,0:3]
    depth_image_data_1_person_raw=depth_image_data_1[ymin - 1:ymax, xmin - 1:xmax, 0:3]
    rgb_image_data_1_person = rgb_image_data_1[ymin - 1:ymax, xmin - 1:xmax, 0:3]

    #取深度图标注框里里中间的一小框区域
    depth_image_data_1_middle = depth_image_data_1[int((ymin+ymax-2)/2)-middle_the:int((ymin+ymax-2)/2)+middle_the+1,int((xmin+xmax-2)/2)-middle_the:int((xmin+xmax-2)/2)+middle_the+1, 0:3]
    # depth_image_data_1 = depth_image_data_1[0:532, 0:775, 0:3]
    # depth_image_data_1 = depth_image_data_1[531, 774, 0:3]

    # depth_image_data_1_rect=cv2.rectangle(depth_image_data_1,(xmin,ymin),(xmax,ymax), (0,0,255), 2)
    # histimg=calcAndDrawHist(depth_image_data_1, (0,0,255),5)
    # histimg = calcAndDrawHist(depth_image_data_1_middle, (0, 0, 255), 5)
    #求深度图标注框里里中间的一小框区域的直方图和众数
    #返回直方图和最大数量的像素值
    histimg,max_gray_scale_value = calcAndDrawHist_max_pixle_value_cutout_person(depth_image_data_1_middle, (0, 0, 255))
    #二值化处理 在这个（众数-cutout_the，众数+cutout_the）这个范围内
    ret,depth_image_data_1_person_threshold=cv2.threshold(depth_image_data_1_person, max_gray_scale_value-cutout_the, 255,cv2.THRESH_BINARY)
    ret_1, depth_image_data_1_person_threshold_1 = cv2.threshold(depth_image_data_1_person,
                                                             max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)


    depth_image_data_1_person_threshold_three_chan=cv2.bitwise_and(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold_1)
    depth_image_data_1_person_threshold_sum=depth_image_data_1_person_threshold_three_chan[:,:,0:1]
    # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_OPEN,kernel=kernel1)
    # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
    #去除噪声
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
    depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_ERODE,kernel=kernel1)
    # depth_image_data_1_person_threshold_sum = cv2.GaussianBlur(depth_image_data_1_person_threshold_sum, (5, 5), 0)
    # print(depth_image_data_1_person_threshold_sum.shape)

    #对二值图进行轮廓检测，去最大面积的一个轮廓
    contours, hierarchy = cv2.findContours(depth_image_data_1_person_threshold_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    contours=sorted(contours,key=lambda c: cv2.contourArea(c), reverse=True)
    cv2.drawContours(depth_image_data_1_person_threshold_three_chan, contours, 0, (0, 0, 255), 2)
    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
    # # kernel = cv2.getStructuringElement(cv2. MORPH_ELLIPSE, (12, 12))
    # depth_image_data_1_person_threshold_sum_BLACKHAT=cv2.morphologyEx(depth_image_data_1_person_threshold_sum, cv2.MORPH_BLACKHAT, kernel)
    # ret, depth_image_data_1_person_threshold = cv2.threshold(depth_image_data_1_person_threshold,max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)
    print(max_gray_scale_value)
    # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_middle,max_gray_scale_value - cutout_the, max_gray_scale_value + cutout_the)
    # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_person, 0,255)
    # cv2.bitwise_not(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold)
    # print(ret)

    cimg = np.zeros_like(depth_image_data_1_person_threshold_three_chan)

    cv2.drawContours(cimg, contours, 0, color=(255, 255, 255), thickness=-1)

    kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    #先腐蚀后膨胀
    cimg = cv2.morphologyEx(cimg, cv2.MORPH_OPEN,kernel=kernel1)
    cimg_h,cimg_w,cimg_c=cimg.shape
    print(cimg.shape)
    random_dst_background_depth=normalize_depth_image(random_dst_background_depth)
    # cv2.imshow('random_dst_background_depth_raw', random_dst_background_depth)

    #逐像素的就行判定
    for i in range(cimg_h):
        for j in range(cimg_w):
            # if cimg[i,j,0]==0:
            #     rgb_image_data_1_person[i,j,0:3]=0
            #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
            if cimg[i, j, 0] == 255:
                random_dst_background_rgb[i, j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                random_dst_background_depth[i, j, 0:3] = depth_image_data_1_person_raw[i,j,0:3]

    # print(depth_image_data_1_person_raw)
    # print(random_dst_background_depth)


    # cv2.imshow('5', cimg)  # 将零件区域像素值设为(0, 0, 0)
    # final = cv2.bitwise_or(depth_image_data_1_person_threshold_three_chan, cimg)
    # cv2.imshow('6', final)
    # cv2.waitKey(0)

    cv2.imshow('random_dst_background_rgb', random_dst_background_rgb)
    cv2.imshow('random_dst_background_depth',random_dst_background_depth)

    # cv2.imshow('ht', rgb_image_data_1_person)
    # cv2.imshow('ht',depth_image_data_1_rect)
    # cv2.imshow('ht', depth_image_data_1_person_raw)
    # cv2.imshow('ht2', depth_image_data_1_middle)
    # cv2.imshow('ht1', histimg)
    # cv2.imshow('ht_thre', depth_image_data_1_person_threshold)
    # cv2.imshow('ht_thre_contour', depth_image_data_1_person_threshold_three_chan)
    # cv2.imshow('ht_thre_1', depth_image_data_1_person_threshold_sum)
    # cv2.imshow('ht_thre_BLACKHAT', depth_image_data_1_person_threshold_sum_BLACKHAT)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


