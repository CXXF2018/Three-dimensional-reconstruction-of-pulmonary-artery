import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data
import os

def CT_to_2(mm,dcm,count,thred_low,thred_high):

    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[int(len(slices) / 2)].image.copy()

    # 对图像进行阈值分割
    ret, mm = cv2.threshold(mm, 200, 1, cv2.THRESH_BINARY)

    # uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
    mm = numpy.uint8(mm)

    for j in range(img.shape[0]):  # 遍历行
        for i in range(img.shape[1]):  # 遍历列
            if mm[j, i] == 0:
                img[j, i] = -2000  # 写入像素点值
            if img[j, i] < thred_low or img[j, i] > thred_high:
                img[j, i] = -2000

    io.imsave(str(count) + '.jpg', img)


def process():
    file_dir = 'E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE'	# 修改为你对应的文件路径
    listdir = os.listdir(file_dir)
    count = 0
    mm = image.imread("test2.jpg")
    for ct_name in listdir:
        count=count+1
        if count >280 :
            break
        # 读取单张Dicom图像
        dcm = pydicom.read_file(file_dir + '/' + ct_name)
        CT_to_2(mm,dcm,count,500,750)
        print(str(count)+'_finish')

if __name__ == '__main__':
    process()