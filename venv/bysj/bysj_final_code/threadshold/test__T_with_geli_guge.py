import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data
def threadSholdT(T,img,mm):
    # 对图像进行阈值分割
    ret,img = cv2.threshold(img, T,3071, cv2.THRESH_BINARY)
    ret, mm = cv2.threshold(mm, 200, 1, cv2.THRESH_BINARY)

    #uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
    img = numpy.uint8(img)
    mm = numpy.uint8(mm)
    for j in range(img.shape[0]):  # 遍历行
        for i in range(img.shape[1]):  # 遍历列
            if mm[j, i] == 0:
                img[j, i] = 0  # 写入像素点值
    io.imsave('test_T_geli_guge/T='+str(T)+'.jpg',img)

if __name__ == '__main__':
    # 读取单张Dicom图像
    dcm = pydicom.read_file("E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE/I2110000.dcm")
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
    mm = image.imread("test2.jpg")
    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[int(len(slices) / 2)].image.copy()
    T = [0,50,100,150,200,250,300,350,400,450,500,550,600,650,700]
    #T = [0,50,100]
    for t in T:
        threadSholdT(t,img,mm)