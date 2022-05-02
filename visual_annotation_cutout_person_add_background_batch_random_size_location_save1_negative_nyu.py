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
import shutil
def creat_dir(out_dir):
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)


# raw_root_path=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime - for_aug'
raw_root_path=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime - for_aug_useful'
raw_root_list=os.listdir(raw_root_path)

dst_background_depth_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_depths_useful'
dst_background_rgb_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_images_useful'

dst_background_depth_list=os.listdir(dst_background_depth_path)

negative_root_path=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime - for_aug-negative_roadway_useful\1'
rgb_negative_root_path=r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime - for_aug-negative_light_useful\1'


save_path=r'G:\lab_collect_dataset\background_aug_negative2\RGBD_background_aug_nyu'
generate_dataset_num=1000
middle_the=20
cutout_the=10
# def move_file(src_path, dst_path, file):
#     try:
#         # cmd = 'chmod -R +x ' + src_path
#         # os.popen(cmd)
#         f_src = os.path.join(src_path, file)
#         if not os.path.exists(dst_path):
#             os.mkdir(dst_path)
#         f_dst = os.path.join(dst_path, file)
#         shutil.move(f_src, f_dst)
#     except Exception as e:
#         print('move_file ERROR: ', e)
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

rgb_path_1_n = os.path.join(negative_root_path, 'rgb')
depth_path_1_n = os.path.join(negative_root_path, 'depth')
anno_path_1_n = os.path.join(negative_root_path, 'annotation')
rgb_path_1_n_list=os.listdir(rgb_path_1_n)

rgb_rgb_path_1_n = os.path.join(rgb_negative_root_path, 'rgb')
rgb_depth_path_1_n = os.path.join(rgb_negative_root_path, 'depth')
rgb_anno_path_1_n = os.path.join(rgb_negative_root_path, 'annotation')
rgb_rgb_path_1_n_list=os.listdir(rgb_rgb_path_1_n)

for raw_root_element in raw_root_list:
    rgb_path_1 = os.path.join(raw_root_path, raw_root_element, 'rgb')
    depth_path_1 = os.path.join(raw_root_path, raw_root_element, 'depth')
    anno_path_1 = os.path.join(raw_root_path, raw_root_element, 'annotation')

    save_rgb_path = os.path.join(save_path, 'rgb')
    save_depth_path = os.path.join(save_path,  'depth')
    save_anno_path= os.path.join(save_path, 'annotation')
    creat_dir(save_rgb_path)
    creat_dir(save_depth_path)
    creat_dir(save_anno_path)

    # image_path_1 = r'G:\lab_collect_dataset\recordData_process_annotation_light_daytime\RGBD_bk_5'
    # rgb_path_1 = os.path.join(image_path_1, 'rgb')
    # depth_path_1 = os.path.join(image_path_1, 'depth')
    # anno_path_1 = os.path.join(image_path_1, 'annotation')
    rgb_image_list_1 = os.listdir(rgb_path_1)
    for i in range(len(rgb_image_list_1)):
        random_rgb_1 = rgb_image_list_1[i]
        annotation_1 = anno_path_1 + '/' + random_rgb_1.rstrip('jpg') + 'xml'

        random_2 = random.randint(0, len(dst_background_depth_list) - 1)
        random_depth_2 =dst_background_depth_list[random_2]
        random_dst_background_depth_all_name = dst_background_depth_path+'/' + random_depth_2
        random_dst_background_rgb_all_name = dst_background_rgb_path + '/' + random_depth_2.rstrip('png')+'jpg'
        # print(random_dst_background_rgb_all_name )

        save_rgb_path_f = save_rgb_path+'/'+'bg_aug_'+random_rgb_1.rstrip('.jpg')+random_depth_2.rstrip('.png')+'.jpg'
        save_depth_path_f = save_depth_path+'/'+'bg_aug_'+random_rgb_1.rstrip('.jpg')+random_depth_2.rstrip('.png')+'.jpg'
        save_anno_name='bg_aug_'+random_rgb_1.rstrip('.jpg')  + random_depth_2.rstrip('.png') + '.xml'
        save_anno_path_f = save_anno_path+'/'+save_anno_name

        random_dst_background_depth=cv2.imread(random_dst_background_depth_all_name)
        random_dst_background_rgb = cv2.imread(random_dst_background_rgb_all_name)
        print('random_dst_background_rgb',random_dst_background_rgb.shape)
        background_shape_h,background_shape_w,_=random_dst_background_rgb.shape



        xmin,ymin,xmax,ymax= readXML(annotation_1)
        xmin, ymin, xmax, ymax=int(xmin),int(ymin),int(xmax),int(ymax)
        # print(args)

        rgb_image_path_1 = rgb_path_1 + '/' + random_rgb_1
        rgb_image_data_1 = cv2.imread(rgb_image_path_1)

        depth_image_path_1 = depth_path_1 + '/' + random_rgb_1
        depth_image_data_1 = cv2.imread(depth_image_path_1)
        # cv2.imshow('depth_image_data_1',depth_image_data_1)
        # print('depth_image_data_1',depth_image_data_1.shape)
        # print(depth_image_data_1.shape)
        # labelimg标注的标注框的范围是从1开始计，到图像的尺寸（闭合）
        depth_image_data_1_person=depth_image_data_1[ymin-1:ymax,xmin-1:xmax,0:3]
        depth_image_data_1_person_raw=depth_image_data_1[ymin - 1:ymax, xmin - 1:xmax, 0:3]
        rgb_image_data_1_person = rgb_image_data_1[ymin - 1:ymax, xmin - 1:xmax, 0:3]

        depth_image_data_1_middle = depth_image_data_1[int((ymin+ymax-2)/2)-middle_the:int((ymin+ymax-2)/2)+middle_the+1,int((xmin+xmax-2)/2)-middle_the:int((xmin+xmax-2)/2)+middle_the+1, 0:3]
        # depth_image_data_1 = depth_image_data_1[0:532, 0:775, 0:3]
        # depth_image_data_1 = depth_image_data_1[531, 774, 0:3]

        # depth_image_data_1_rect=cv2.rectangle(depth_image_data_1,(xmin,ymin),(xmax,ymax), (0,0,255), 2)
        # histimg=calcAndDrawHist(depth_image_data_1, (0,0,255),5)
        # histimg = calcAndDrawHist(depth_image_data_1_middle, (0, 0, 255), 5)
        #返回直方图和最大数量的像素值
        histimg,max_gray_scale_value = calcAndDrawHist_max_pixle_value_cutout_person(depth_image_data_1_middle, (0, 0, 255))
        ret,depth_image_data_1_person_threshold=cv2.threshold(depth_image_data_1_person, max_gray_scale_value-cutout_the, 255,cv2.THRESH_BINARY)
        ret_1, depth_image_data_1_person_threshold_1 = cv2.threshold(depth_image_data_1_person,
                                                                 max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)
        depth_image_data_1_person_threshold_three_chan=cv2.bitwise_and(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold_1)
        depth_image_data_1_person_threshold_sum=depth_image_data_1_person_threshold_three_chan[:,:,0:1]
        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_OPEN,kernel=kernel1)
        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_ERODE,kernel=kernel1)
        # depth_image_data_1_person_threshold_sum = cv2.GaussianBlur(depth_image_data_1_person_threshold_sum, (5, 5), 0)
        # print(depth_image_data_1_person_threshold_sum.shape)

        contours, hierarchy = cv2.findContours(depth_image_data_1_person_threshold_sum, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        contours=sorted(contours,key=lambda c: cv2.contourArea(c), reverse=True)
        cv2.drawContours(depth_image_data_1_person_threshold_three_chan, contours, 0, (0, 0, 255), 2)
        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        # # kernel = cv2.getStructuringElement(cv2. MORPH_ELLIPSE, (12, 12))
        # depth_image_data_1_person_threshold_sum_BLACKHAT=cv2.morphologyEx(depth_image_data_1_person_threshold_sum, cv2.MORPH_BLACKHAT, kernel)
        # ret, depth_image_data_1_person_threshold = cv2.threshold(depth_image_data_1_person_threshold,max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)
        # print(max_gray_scale_value)
        # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_middle,max_gray_scale_value - cutout_the, max_gray_scale_value + cutout_the)
        # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_person, 0,255)
        # cv2.bitwise_not(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold)
        # print(ret)

        cimg = np.zeros_like(depth_image_data_1_person_threshold_three_chan)

        cv2.drawContours(cimg, contours, 0, color=(255, 255, 255), thickness=-1)

        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # #先腐蚀后膨胀
        # cimg = cv2.morphologyEx(cimg, cv2.MORPH_OPEN,kernel=kernel1)
        # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # # 先腐蚀后膨胀
        # cimg = cv2.morphologyEx(cimg, cv2.MORPH_ERODE, kernel=kernel2)
        print(cimg.shape)
        cimg_h,cimg_w,_=cimg.shape
        #设置随机，使人体形状和大小变化
        background_shape_h_random_n=random.randint(int(background_shape_h*0.3),int(background_shape_h*0.6))
        background_shape_w_random_n=int(cimg_w/cimg_h*background_shape_h_random_n*random.uniform(0.8,1.3))
        dst_w, dst_h=background_shape_w_random_n,background_shape_h_random_n
        # dst_w,dst_h=266,387
        depth_image_data_1_person_raw=cv2.resize(depth_image_data_1_person_raw,(dst_w,dst_h))
        rgb_image_data_1_person=cv2.resize(rgb_image_data_1_person,(dst_w,dst_h))
        cimg=cv2.resize(cimg,(dst_w,dst_h))

        dst_loc_x_max=background_shape_w-background_shape_w_random_n
        dst_loc_y_max = background_shape_h - background_shape_h_random_n

        dst_loc_x_r,dst_loc_y_r=random.randint(0,dst_loc_x_max),random.randint(0,dst_loc_y_max)


        # cv2.imshow('cimg', cimg)
        # cv2.imshow('depth_image_data_1_person_raw', depth_image_data_1_person_raw)
        # cv2.imshow('rgb_image_data_1_person', rgb_image_data_1_person)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(cimg.shape)
        cimg_h, cimg_w, cimg_c = cimg.shape
        cimg_h_r, cimg_w_r = cimg_h, cimg_w
        random_dst_background_depth=normalize_depth_image(random_dst_background_depth)
        # cv2.imshow('random_dst_background_depth_raw', random_dst_background_depth)

        for i in range(cimg_h):
            for j in range(cimg_w):
                # if cimg[i,j,0]==0:
                #     rgb_image_data_1_person[i,j,0:3]=0
                #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                if cimg[i, j, 0] == 255:
                    random_dst_background_rgb[dst_loc_y_r+i, dst_loc_x_r+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                    random_dst_background_depth[dst_loc_y_r+i, dst_loc_x_r+j, 0:3] = depth_image_data_1_person_raw[i,j,0:3]


#####
        random_rgb_1_n = rgb_path_1_n_list[random.randint(0,len(rgb_path_1_n_list)-1)]
        annotation_1_n = anno_path_1_n + '/' + random_rgb_1_n.rstrip('jpg') + 'xml'

        xmin, ymin, xmax, ymax = readXML(annotation_1_n)
        xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
        # print(args)

        rgb_image_path_1_n = rgb_path_1_n + '/' + random_rgb_1_n
        rgb_image_data_1_n = cv2.imread(rgb_image_path_1_n)

        depth_image_path_1_n = depth_path_1_n + '/' + random_rgb_1_n
        depth_image_data_1_n = cv2.imread(depth_image_path_1_n)

        depth_image_data_1_person_n = depth_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]
        depth_image_data_1_person_raw_n = depth_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]
        rgb_image_data_1_person_n = rgb_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]

        depth_image_data_1_middle_n = depth_image_data_1_n[
                                    int((ymin + ymax - 2) / 2) - middle_the:int((ymin + ymax - 2) / 2) + middle_the + 1,
                                    int((xmin + xmax - 2) / 2) - middle_the:int((xmin + xmax - 2) / 2) + middle_the + 1,
                                    0:3]
        # depth_image_data_1 = depth_image_data_1[0:532, 0:775, 0:3]
        # depth_image_data_1 = depth_image_data_1[531, 774, 0:3]

        # depth_image_data_1_rect=cv2.rectangle(depth_image_data_1,(xmin,ymin),(xmax,ymax), (0,0,255), 2)
        # histimg=calcAndDrawHist(depth_image_data_1, (0,0,255),5)
        # histimg = calcAndDrawHist(depth_image_data_1_middle, (0, 0, 255), 5)
        # 返回直方图和最大数量的像素值
        histimg, max_gray_scale_value_n = calcAndDrawHist_max_pixle_value_cutout_person(depth_image_data_1_middle_n,
                                                                                      (0, 0, 255))
        ret, depth_image_data_1_person_threshold_n = cv2.threshold(depth_image_data_1_person_n,
                                                                 max_gray_scale_value_n - cutout_the, 255,
                                                                 cv2.THRESH_BINARY)
        ret_1, depth_image_data_1_person_threshold_1_n = cv2.threshold(depth_image_data_1_person_n,
                                                                     max_gray_scale_value_n + cutout_the, 255,
                                                                     cv2.THRESH_BINARY_INV)
        depth_image_data_1_person_threshold_three_chan_n = cv2.bitwise_and(depth_image_data_1_person_threshold_n,
                                                                         depth_image_data_1_person_threshold_1_n)
        depth_image_data_1_person_threshold_sum_n = depth_image_data_1_person_threshold_three_chan_n[:, :, 0:1]
        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_OPEN,kernel=kernel1)
        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        depth_image_data_1_person_threshold_sum_n = cv2.morphologyEx(depth_image_data_1_person_threshold_sum_n,
                                                                   cv2.MORPH_DILATE, kernel=kernel1)
        kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
        depth_image_data_1_person_threshold_sum_n = cv2.morphologyEx(depth_image_data_1_person_threshold_sum_n,
                                                                   cv2.MORPH_ERODE, kernel=kernel1)
        # depth_image_data_1_person_threshold_sum = cv2.GaussianBlur(depth_image_data_1_person_threshold_sum, (5, 5), 0)
        # print(depth_image_data_1_person_threshold_sum.shape)

        contours_n, hierarchy = cv2.findContours(depth_image_data_1_person_threshold_sum_n, cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_NONE)
        contours_n = sorted(contours_n, key=lambda c: cv2.contourArea(c), reverse=True)
        # cv2.drawContours(depth_image_data_1_person_threshold_three_chan, contours_n, 0, (0, 0, 255), 2)


        # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        # # kernel = cv2.getStructuringElement(cv2. MORPH_ELLIPSE, (12, 12))
        # depth_image_data_1_person_threshold_sum_BLACKHAT=cv2.morphologyEx(depth_image_data_1_person_threshold_sum, cv2.MORPH_BLACKHAT, kernel)
        # ret, depth_image_data_1_person_threshold = cv2.threshold(depth_image_data_1_person_threshold,max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)
        # print(max_gray_scale_value)
        # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_middle,max_gray_scale_value - cutout_the, max_gray_scale_value + cutout_the)
        # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_person, 0,255)
        # cv2.bitwise_not(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold)
        # print(ret)

        cimg_n = np.zeros_like(depth_image_data_1_person_threshold_three_chan_n)

        cv2.drawContours(cimg_n, contours_n, 0, color=(255, 255, 255), thickness=-1)

        # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
        # #先腐蚀后膨胀
        # cimg = cv2.morphologyEx(cimg, cv2.MORPH_OPEN,kernel=kernel1)
        # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        # # 先腐蚀后膨胀
        # cimg = cv2.morphologyEx(cimg, cv2.MORPH_ERODE, kernel=kernel2)
        print(cimg_n.shape)
        cimg_h, cimg_w, _ = cimg_n.shape
        # 设置随机，使人体形状和大小变化
        for k in range(random.randint(1, 1)):
            background_shape_h_random_n = random.randint(int(background_shape_h * 0.1), int(background_shape_h * 0.3))
            background_shape_w_random_n = int(cimg_w / cimg_h * background_shape_h_random_n * random.uniform(0.8, 1))
            print(background_shape_h_random_n,background_shape_w_random_n)
            if background_shape_w_random_n ==0:
                background_shape_w_random_n = 32
            dst_w_n, dst_h_n = background_shape_w_random_n, background_shape_h_random_n
            # dst_w,dst_h=266,387
            depth_image_data_1_person_raw_n = cv2.resize(depth_image_data_1_person_raw_n, (dst_w_n, dst_h_n))

            random_aug_blur_n = random.randint(3, 7)
            depth_image_data_1_person_raw_n = cv2.blur(depth_image_data_1_person_raw_n,
                                                     (random_aug_blur_n, random_aug_blur_n))

            rgb_image_data_1_person_n = cv2.resize(rgb_image_data_1_person_n, (dst_w_n, dst_h_n))
            cimg_n = cv2.resize(cimg_n, (dst_w_n, dst_h_n))
            depth_image_data_1_person_threshold_three_chan_n_mubu = cv2.resize(depth_image_data_1_person_threshold_three_chan_n, (dst_w_n, dst_h_n))

            # dst_loc_x_max = background_shape_w - background_shape_w_random_n
            # dst_loc_y_max = background_shape_h - background_shape_h_random_n
            #
            # dst_loc_x_n, dst_loc_y_n = random.randint(0, dst_loc_x_max), random.randint(0, dst_loc_y_max)

            # cv2.imshow('cimg', cimg)
            # cv2.imshow('depth_image_data_1_person_raw', depth_image_data_1_person_raw)
            # cv2.imshow('rgb_image_data_1_person', rgb_image_data_1_person)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # print(cimg.shape)
            cimg_h, cimg_w, cimg_c = cimg_n.shape
            cimg_h1, cimg_w1, cimg_c1 = depth_image_data_1_person_threshold_three_chan_n_mubu.shape

            dst_loc_x_max1 = (background_shape_w) if (background_shape_w - (
                    dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else dst_loc_x_r
            dst_loc_x_min1 = (dst_loc_x_r + cimg_w_r) if (background_shape_w - (
                    dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else 0

            dst_loc_x_max = dst_loc_x_max1 - background_shape_w_random_n
            dst_loc_y_max = background_shape_h - background_shape_h_random_n
            dst_loc_x_n, dst_loc_y_n = random.randint(dst_loc_x_min1, dst_loc_x_max), random.randint(0, dst_loc_y_max)

            random_value = random.randint(2, 8)
            # if random.randint(0,1):
            for i in range(cimg_h):
                for j in range(cimg_w):
                    # if cimg[i,j,0]==0:
                    #     rgb_image_data_1_person[i,j,0:3]=0
                    #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                    if cimg_n[i, j, 0] == 255:
                        # random_dst_background_rgb[dst_loc_y+i, dst_loc_x+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                        random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                        0:3] = 0.1 * random_value * depth_image_data_1_person_raw_n[i, j, 0:3]
                # for i in range(cimg_h1):
                #     for j in range(cimg_w1):
                #         # if cimg[i,j,0]==0:
                #         #     rgb_image_data_1_person[i,j,0:3]=0
                #         #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                #         if depth_image_data_1_person_threshold_three_chan_n_mubu[i, j, 0] == 255:
                #             # random_dst_background_rgb[dst_loc_y+i, dst_loc_x+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                #             random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                #             0:3] = 0.1 * random_value * depth_image_data_1_person_raw_n[i, j, 0:3]
            # else:

                # for i in range(cimg_h):
                #     for j in range(cimg_w):
                #         # if cimg[i,j,0]==0:
                #         #     rgb_image_data_1_person[i,j,0:3]=0
                #         #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                #         if cimg_n[i, j, 0] == 255:
                #             # random_dst_background_rgb[dst_loc_y+i, dst_loc_x+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                #             random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                #             0:3] = 0.1 * random_value * cimg_n[i, j, 0:3]
            for l in range(random.randint(1, 5)):
                background_shape_h_random_n = random.randint(int(background_shape_h * 0.1),
                                                           int(background_shape_h * 0.3))
                background_shape_w_random_n = random.randint(int(background_shape_w * 0.05),
                                                           int(background_shape_w * 0.1))
                dst_w_n, dst_h_n = background_shape_w_random_n, background_shape_h_random_n
                # dst_w,dst_h=266,387
                depth_image_data_1_person_raw_n = cv2.resize(depth_image_data_1_person_raw_n, (dst_w_n, dst_h_n))

                # random_aug_blur_n = random.randint(1, 3)
                # depth_image_data_1_person_raw = cv2.blur(depth_image_data_1_person_raw,
                #                                          (random_aug_blur_n, random_aug_blur_n))

                rgb_image_data_1_person_n = cv2.resize(rgb_image_data_1_person_n, (dst_w_n, dst_h_n))
                cimg_n = cv2.resize(cimg_n, (dst_w_n, dst_h_n))

                # dst_loc_x_max = background_shape_w - background_shape_w_random_n
                # dst_loc_y_max = background_shape_h - background_shape_h_random_n
                #
                # dst_loc_x_n, dst_loc_y_n = random.randint(0, dst_loc_x_max), random.randint(0, dst_loc_y_max)

                # cv2.imshow('cimg', cimg)
                # cv2.imshow('depth_image_data_1_person_raw', depth_image_data_1_person_raw)
                # cv2.imshow('rgb_image_data_1_person', rgb_image_data_1_person)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # print(cimg.shape)
                cimg_h, cimg_w, cimg_c = cimg_n.shape
                # cv2.imshow('random_dst_background_depth_raw', random_dst_background_depth)

                dst_loc_x_max1 = (background_shape_w) if (background_shape_w - (
                        dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else dst_loc_x_r
                dst_loc_x_min1 = (dst_loc_x_r + cimg_w_r) if (background_shape_w - (
                        dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else 0

                dst_loc_x_max = dst_loc_x_max1 - background_shape_w_random_n
                dst_loc_y_max = background_shape_h - background_shape_h_random_n
                dst_loc_x_n, dst_loc_y_n = random.randint(dst_loc_x_min1, dst_loc_x_max), random.randint(0,
                                                                                                         dst_loc_y_max)

                random_value = random.randint(2, 9)
                for i in range(cimg_h):
                    for j in range(cimg_w):
                        # if cimg[i,j,0]==0:
                        #     rgb_image_data_1_person[i,j,0:3]=0
                        #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                        if cimg_n[i, j, 0] == 255:
                            # random_dst_background_rgb[dst_loc_y+i, dst_loc_x+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                            random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                            0:3] = 0.1 * random_value * depth_image_data_1_person_raw_n[i, j, 0:3]



##rgb
            ##rgb
            rgb_random_rgb_1_n = rgb_rgb_path_1_n_list[random.randint(0, len(rgb_rgb_path_1_n_list) - 1)]
            rgb_annotation_1_n = rgb_anno_path_1_n + '/' + rgb_random_rgb_1_n.rstrip('jpg') + 'xml'

            xmin, ymin, xmax, ymax = readXML(rgb_annotation_1_n)
            xmin, ymin, xmax, ymax = int(xmin), int(ymin), int(xmax), int(ymax)
            # print(args)

            rgb_image_path_1_n = rgb_rgb_path_1_n + '/' + rgb_random_rgb_1_n
            rgb_image_data_1_n = cv2.imread(rgb_image_path_1_n)

            depth_image_path_1_n = rgb_depth_path_1_n + '/' + rgb_random_rgb_1_n
            depth_image_data_1_n = cv2.imread(depth_image_path_1_n)

            depth_image_data_1_person_n = depth_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]
            depth_image_data_1_person_raw_n = depth_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]
            rgb_image_data_1_person_n = rgb_image_data_1_n[ymin - 1:ymax, xmin - 1:xmax, 0:3]

            depth_image_data_1_middle_n = depth_image_data_1_n[
                                          int((ymin + ymax - 2) / 2) - middle_the:int(
                                              (ymin + ymax - 2) / 2) + middle_the + 1,
                                          int((xmin + xmax - 2) / 2) - middle_the:int(
                                              (xmin + xmax - 2) / 2) + middle_the + 1,
                                          0:3]
            # depth_image_data_1 = depth_image_data_1[0:532, 0:775, 0:3]
            # depth_image_data_1 = depth_image_data_1[531, 774, 0:3]

            # depth_image_data_1_rect=cv2.rectangle(depth_image_data_1,(xmin,ymin),(xmax,ymax), (0,0,255), 2)
            # histimg=calcAndDrawHist(depth_image_data_1, (0,0,255),5)
            # histimg = calcAndDrawHist(depth_image_data_1_middle, (0, 0, 255), 5)
            # 返回直方图和最大数量的像素值
            histimg, max_gray_scale_value_n = calcAndDrawHist_max_pixle_value_cutout_person(
                depth_image_data_1_middle_n,
                (0, 0, 255))
            ret, depth_image_data_1_person_threshold_n = cv2.threshold(depth_image_data_1_person_n,
                                                                       max_gray_scale_value_n - cutout_the, 255,
                                                                       cv2.THRESH_BINARY)
            ret_1, depth_image_data_1_person_threshold_1_n = cv2.threshold(depth_image_data_1_person_n,
                                                                           max_gray_scale_value_n + cutout_the, 255,
                                                                           cv2.THRESH_BINARY_INV)
            depth_image_data_1_person_threshold_three_chan_n = cv2.bitwise_and(
                depth_image_data_1_person_threshold_n,
                depth_image_data_1_person_threshold_1_n)
            depth_image_data_1_person_threshold_sum_n = depth_image_data_1_person_threshold_three_chan_n[:, :, 0:1]
            # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_OPEN,kernel=kernel1)
            # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            # depth_image_data_1_person_threshold_sum=cv2.morphologyEx(depth_image_data_1_person_threshold_sum,cv2.MORPH_DILATE,kernel=kernel1)
            kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
            depth_image_data_1_person_threshold_sum_n = cv2.morphologyEx(depth_image_data_1_person_threshold_sum_n,
                                                                         cv2.MORPH_DILATE, kernel=kernel1)
            kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (1, 1))
            depth_image_data_1_person_threshold_sum_n = cv2.morphologyEx(depth_image_data_1_person_threshold_sum_n,
                                                                         cv2.MORPH_ERODE, kernel=kernel1)
            # depth_image_data_1_person_threshold_sum = cv2.GaussianBlur(depth_image_data_1_person_threshold_sum, (5, 5), 0)
            # print(depth_image_data_1_person_threshold_sum.shape)

            contours_n, hierarchy = cv2.findContours(depth_image_data_1_person_threshold_sum_n, cv2.RETR_EXTERNAL,
                                                     cv2.CHAIN_APPROX_NONE)
            contours_n = sorted(contours_n, key=lambda c: cv2.contourArea(c), reverse=True)
            # cv2.drawContours(depth_image_data_1_person_threshold_three_chan, contours_n, 0, (0, 0, 255), 2)

            # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
            # # kernel = cv2.getStructuringElement(cv2. MORPH_ELLIPSE, (12, 12))
            # depth_image_data_1_person_threshold_sum_BLACKHAT=cv2.morphologyEx(depth_image_data_1_person_threshold_sum, cv2.MORPH_BLACKHAT, kernel)
            # ret, depth_image_data_1_person_threshold = cv2.threshold(depth_image_data_1_person_threshold,max_gray_scale_value + cutout_the, 255, cv2.THRESH_BINARY_INV)
            # print(max_gray_scale_value)
            # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_middle,max_gray_scale_value - cutout_the, max_gray_scale_value + cutout_the)
            # depth_image_data_1_person_threshold = cv2.inRange(depth_image_data_1_person, 0,255)
            # cv2.bitwise_not(depth_image_data_1_person_threshold,depth_image_data_1_person_threshold)
            # print(ret)

            cimg_n = np.zeros_like(depth_image_data_1_person_threshold_three_chan_n)

            cv2.drawContours(cimg_n, contours_n, 0, color=(255, 255, 255), thickness=-1)

            # kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
            # #先腐蚀后膨胀
            # cimg = cv2.morphologyEx(cimg, cv2.MORPH_OPEN,kernel=kernel1)
            # kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
            # # 先腐蚀后膨胀
            # cimg = cv2.morphologyEx(cimg, cv2.MORPH_ERODE, kernel=kernel2)
            print(cimg_n.shape)
            cimg_h, cimg_w, _ = cimg_n.shape
            # 设置随机，使人体形状和大小变化
            for k in range(random.randint(1, 5)):
                background_shape_h_random_n = random.randint(int(background_shape_h * 0.05),
                                                             int(background_shape_h * 0.1))
                background_shape_w_random_n = random.randint(int(background_shape_h * 0.05),
                                                             int(background_shape_h * 0.1))
                # background_shape_w_random_n = int(
                #     cimg_w / cimg_h * background_shape_h_random_n * random.uniform(0.8, 1))
                print(background_shape_h_random_n, background_shape_w_random_n)
                if background_shape_w_random_n == 0:
                    background_shape_w_random_n = 32
                dst_w_n, dst_h_n = background_shape_w_random_n, background_shape_h_random_n
                # dst_w,dst_h=266,387
                depth_image_data_1_person_raw_n = cv2.resize(depth_image_data_1_person_raw_n, (dst_w_n, dst_h_n))

                # random_aug_blur_n = random.randint(3, 7)
                # depth_image_data_1_person_raw_n = cv2.blur(depth_image_data_1_person_raw_n,
                #                                            (random_aug_blur_n, random_aug_blur_n))

                rgb_image_data_1_person_n = cv2.resize(rgb_image_data_1_person_n, (dst_w_n, dst_h_n))
                cimg_n = cv2.resize(cimg_n, (dst_w_n, dst_h_n))

                # dst_loc_x_max = background_shape_w - background_shape_w_random_n
                # dst_loc_y_max = background_shape_h - background_shape_h_random_n
                #
                # dst_loc_x_n, dst_loc_y_n = random.randint(0, dst_loc_x_max), random.randint(0, dst_loc_y_max)

                dst_loc_x_max1 = (background_shape_w) if (background_shape_w - (
                        dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else dst_loc_x_r
                dst_loc_x_min1 = (dst_loc_x_r + cimg_w_r) if (background_shape_w - (
                        dst_loc_x_r + cimg_w_r)) > dst_loc_x_r else 0

                dst_loc_x_max = dst_loc_x_max1 - background_shape_w_random_n
                dst_loc_y_max = background_shape_h - background_shape_h_random_n
                dst_loc_x_n, dst_loc_y_n = random.randint(dst_loc_x_min1, dst_loc_x_max), random.randint(0,
                                                                                                         dst_loc_y_max)

                # cv2.imshow('cimg', cimg)
                # cv2.imshow('depth_image_data_1_person_raw', depth_image_data_1_person_raw)
                # cv2.imshow('rgb_image_data_1_person', rgb_image_data_1_person)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()
                # print(cimg.shape)
                cimg_h, cimg_w, cimg_c = cimg_n.shape
                cimg_h1, cimg_w1, cimg_c1 = depth_image_data_1_person_threshold_three_chan_n_mubu.shape

                # random_value = random.randint(2, 8)
                for i in range(cimg_h):
                    for j in range(cimg_w):
                        # if cimg[i,j,0]==0:
                        #     rgb_image_data_1_person[i,j,0:3]=0
                        #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                        if cimg_n[i, j, 0] == 255:
                            random_dst_background_rgb[dst_loc_y_n + i, dst_loc_x_n + j,
                            0:3] = rgb_image_data_1_person_n[i, j, 0:3]
                            # random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                            # 0:3] = 0.1 * random_value * depth_image_data_1_person_raw_n[i, j, 0:3]
                    # for i in range(cimg_h1):
                    #     for j in range(cimg_w1):
                    #         # if cimg[i,j,0]==0:
                    #         #     rgb_image_data_1_person[i,j,0:3]=0
                    #         #     depth_image_data_1_person_threshold_three_chan[i,j,0:3]=0
                    #         if depth_image_data_1_person_threshold_three_chan_n_mubu[i, j, 0] == 255:
                    #             # random_dst_background_rgb[dst_loc_y+i, dst_loc_x+j, 0:3] = rgb_image_data_1_person[i,j,0:3]
                    #             random_dst_background_depth[dst_loc_y_n + i, dst_loc_x_n + j,
                    #             0:3] = 0.1 * random_value * depth_image_data_1_person_raw_n[i, j, 0:3]

        random_aug_blur=random.randint(1,3)
        random_aug_blur1 = random.randint(1, 5)


        random_dst_background_person_rgb = cv2.blur(random_dst_background_rgb, (random_aug_blur,random_aug_blur))
        # random_dst_background_person_rgb = cv2.medianBlur(random_dst_background_rgb, 9)
        # random_dst_background_person_rgb = cv2.GaussianBlur(random_dst_background_rgb, (3,3),0)
        random_dst_background_person_depth = cv2.blur(random_dst_background_depth, (random_aug_blur1, random_aug_blur1))



        dataset_aug_random=random.randint(1,3)
        if dataset_aug_random==1:
            random_dst_background_person_rgb=cv2.medianBlur(random_dst_background_person_rgb, 3)
            random_dst_background_person_depth=cv2.medianBlur(random_dst_background_person_depth, 3)
        elif dataset_aug_random==2:
            random_dst_background_person_rgb = cv2.GaussianBlur(random_dst_background_person_rgb, (3, 3), 0)
            random_dst_background_person_depth = cv2.GaussianBlur(random_dst_background_person_depth,  (3, 3), 0)
        else:
            pass

        # bg_aug_xmin,bg_aug_ymin,bg_aug_xmax,bg_aug_ymax=dst_loc_x+1, dst_loc_y+1,dst_loc_x+1+dst_w-1,dst_loc_y+1+dst_h-1

        select_random = random.randint(1, 1)
        if select_random == 1:
            bg_aug_xmin, bg_aug_ymin, bg_aug_xmax, bg_aug_ymax = dst_loc_x_r + 1, dst_loc_y_r + 1, dst_loc_x_r + dst_w, dst_loc_y_r + dst_h
            writeXML(save_anno_path_f, 'rgb', save_anno_name,save_anno_path_f, str(background_shape_w), str(background_shape_h), '3','person', str(bg_aug_xmin), str(bg_aug_ymin), str(bg_aug_xmax), str(bg_aug_ymax))

            cv2.imwrite(save_rgb_path_f,random_dst_background_person_rgb)
            cv2.imwrite(save_depth_path_f,random_dst_background_person_depth)
        # cv2.imshow('random_dst_background_person_rgb', random_dst_background_person_rgb)
        # cv2.imshow('random_dst_background_person_depth', random_dst_background_person_depth)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(depth_image_data_1_person_raw)
        # print(random_dst_background_depth)


        # cv2.imshow('5', cimg)  # 将零件区域像素值设为(0, 0, 0)
        # final = cv2.bitwise_or(depth_image_data_1_person_threshold_three_chan, cimg)
        # cv2.imshow('6', final)
        # cv2.waitKey(0)
        # while (True):
        #     # cv2.imshow('rgb_image_data_1_person', rgb_image_data_1_person)
        #
        #     # cv2.imshow('random_dst_background_rgb', random_dst_background_rgb)
        #     # cv2.imshow('random_dst_background_depth',random_dst_background_depth)
        #     cv2.imshow('random_dst_background_person_rgb', random_dst_background_person_rgb)
        #     cv2.imshow('random_dst_background_person_depth', random_dst_background_person_depth)
        #     waitkey_count = cv2.waitKey(0)
        #     if waitkey_count == 27:
        #         print('esc')
        #         shut_down_count = True
        #         break
        #     elif waitkey_count == 106:
        #         # print('j:有用')
        #         print('有用')
        #         # cv2.imwrite()
        #         break
        #     elif waitkey_count == 107:
        #         # print('k：没用')
        #         print('没用')
        #         # shutil.move(f_src, f_dst)
        #         break
        #     else:
        #         pass
        # cv2.imshow('random_dst_background_rgb', random_dst_background_rgb)
        # cv2.imshow('random_dst_background_depth',random_dst_background_depth)
        # cv2.imshow('random_dst_background_person_rgb', random_dst_background_person_rgb)
        # cv2.imshow('random_dst_background_person_depth', random_dst_background_person_depth)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()



        # cv2.imshow('ht', rgb_image_data_1_person)
        # cv2.imshow('ht',depth_image_data_1_rect)
        # cv2.imshow('ht', depth_image_data_1_person_raw)
        # cv2.imshow('ht2', depth_image_data_1_middle)
        # cv2.imshow('ht1', histimg)
        # cv2.imshow('ht_thre', depth_image_data_1_person_threshold)
        # cv2.imshow('ht_thre_contour', depth_image_data_1_person_threshold_three_chan)
        # cv2.imshow('ht_thre_1', depth_image_data_1_person_threshold_sum)
        # cv2.imshow('ht_thre_BLACKHAT', depth_image_data_1_person_threshold_sum_BLACKHAT)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()


