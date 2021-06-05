import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data


def thredshold(img_name,thred):
    # 读取单张Dicom图像
    dcm = pydicom.read_file("E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE/" + img_name)
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[ int(len(slices)/2) ].image.copy()


    # 对图像进行阈值分割
    ret,img = cv2.threshold(img,  thred,3071, cv2.THRESH_BINARY)

    #uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
    img = numpy.uint8(img)

    return img

if __name__ == '__main__':
    img_name = 'I2030000.dcm'
    img1 = thredshold(img_name, 500)
    img2 = thredshold(img_name, 800)

    plt.figure(figsize=(12, 12))
    plt.subplot(131)
    plt.imshow(img1, 'gray')
    plt.title('Original')
    for j in range(img1.shape[0]):            #遍历行
        for i in range(img1.shape[1]):        #遍历列
            if img1[j,i]==255 :
                img1[j,i]=0


    # 显式原始数据，mask和分割结果
    plt.subplot(132)
    plt.imshow(img1, 'gray')
    plt.title('Result')
    plt.show()