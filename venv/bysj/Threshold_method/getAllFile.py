#  -*- coding: utf-8 -*-
import cv2
import os

def Edge_Extract(root):
    img_root = os.path.join(root,'img_masks')			# 修改为保存图像的文件名
    edge_root = os.path.join(root,'img_edge')			# 结果输出文件

    if not os.path.exists(edge_root):
        os.mkdir(edge_root)

    file_names = os.listdir(img_root)
    img_name = []

    for name in file_names:
        if not name.endswith('.dcm'):
            assert "This file %s is not PNG"%(name)
        img_name.append(os.path.join(img_root,name+'.dcm'))

    index = 0
    for image in img_name:
        img = cv2.imread(image,0)
        cv2.imwrite(edge_root+'/'+file_names[index],cv2.Canny(img,30,100))
        index += 1
    return 0


if __name__ == '__main__':
    root = '‪C:/Users/chenyw/Desktop/毕业论文/testCanny/'	# 修改为你对应的文件路径
    Edge_Extract(root)