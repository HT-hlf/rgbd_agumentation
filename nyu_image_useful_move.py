# coding:utf-8
# @Author     : HT
# @Time       : 2022/4/3 14:52
# @File       : nyu_image_useful_move.py
# @Software   : PyCharm
import os
import cv2
import shutil

dst_background_depth_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_depths'
dst_background_rgb_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_images'
dst_background_depth_list=os.listdir(dst_background_depth_path)

useful_dst_background_depth_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_depths_useful'
useful_dst_background_rgb_path=r'G:\Graduation_Design_Dataset\collect_RGBD\NYU Depth Dataset V2 for image augmention\nyu_images_useful'
for f in dst_background_depth_list:
    dst_background_rgb_file=dst_background_rgb_path+'/'+f.rstrip('png')+'jpg'
    dst_background_depth_file=dst_background_depth_path+'/'+f
    useful_dst_background_rgb_file = useful_dst_background_rgb_path + '/' + f.rstrip('png') + 'jpg'
    useful_dst_background_depth_file = useful_dst_background_depth_path + '/' + f
    dst_background_depth_data=cv2.imread(dst_background_rgb_file)
    while (True):
        cv2.imshow('ht', dst_background_depth_data)
        waitkey_count = cv2.waitKey(0)
        if waitkey_count == 27:
            print('esc')
            shut_down_count = True
            break
        elif waitkey_count == 106:
            # print('j:有用')
            print('有用')
            shutil.move(dst_background_rgb_file, useful_dst_background_rgb_file)
            shutil.move(dst_background_depth_file, useful_dst_background_depth_file)
            # cv2.imwrite()
            break
        elif waitkey_count == 107:
            # print('k：没用')
            print('没用')
            # shutil.move(f_src, f_dst)
            break
        else:
            pass
    cv2.destroyAllWindows()