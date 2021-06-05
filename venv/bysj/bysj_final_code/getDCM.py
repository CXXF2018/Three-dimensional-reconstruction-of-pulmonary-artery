import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data
import os

def get_9_dcm(file_dir,ct_name,count):
    # 读取单张Dicom图像
    dcm = pydicom.read_file(file_dir + '/' + ct_name)
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[int(len(slices) / 2)].image.copy()
    io.imsave('9_dcm/'+str(count) + '.jpg', img)



if __name__ == '__main__':
    file_dir = 'E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE'	# 修改为你对应的文件路径
    listdir = os.listdir(file_dir)
    count = 0
    for ct_name in listdir:
        count=count+1
        get_9_dcm(file_dir,ct_name,count)
        print(str(count)+'_finish')
