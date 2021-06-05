import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data

#img1为原始图片，mm为隔离平面，img为隔离结果
img1 = image.imread("161.jpg")
mm = image.imread("testgeli.jpg")
# 对图像进行阈值分割
ret,mm = cv2.threshold(mm, 100,1, cv2.THRESH_BINARY)
ret,img = cv2.threshold(img1, 100,1, cv2.THRESH_BINARY)
#uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255

mm = numpy.uint8(mm)#隔离平面
img = numpy.uint8(img)#进行分割后的图片

for j in range(img.shape[0]):            #遍历行
    for i in range(img.shape[1]):        #遍历列
        if mm[j,i]>0 :
            img[j,i]=0#写入像素点值

# 显式原始数据，mask和分割结果
plt.figure(figsize=(12, 12))
plt.subplot(131)
plt.imshow(img1, 'gray')
plt.title('Original image')
plt.subplot(132)
plt.imshow(mm, 'gray')
plt.title('Isolation plane')
plt.subplot(133)
plt.imshow(img, 'gray')
plt.title('Result image')
plt.show()