import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data
import os

def CT_to_2(dir_name,CT_name,count):
    # 读取单张Dicom图像
    dcm = pydicom.read_file(dir_name+'/'+CT_name)
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[int(len(slices) / 2)].image.copy()

    # uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
    img = numpy.uint8(img)

    #  去除无关区域
    for j in range(img.shape[0]):  # 遍历行
        for i in range(img.shape[1]):  # 遍历列
            if mm[j, i] == 0:
                img[j, i] = 0  # 写入像素点值
            if img[j, i] > 500:
                img[j, i] = 0

    io.imsave(str(count)+'.jpg',img)


if __name__ == '__main__':
    file_dir = 'E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE'	# 修改为你对应的文件路径
    listdir = os.listdir(file_dir)
    count = 0
    for ct_name in listdir:
        count=count+1
        if count >280 :
            break
        CT_to_2(file_dir,ct_name,count)
        print(str(count)+'_finish')
