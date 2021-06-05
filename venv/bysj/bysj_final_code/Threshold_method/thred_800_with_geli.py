import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data

# 读取单张Dicom图像
dcm = pydicom.read_file("E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE/I2040000.dcm")
dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
mm = image.imread("test2.jpg")

# 获取图像中的像素数据
slices = []
slices.append(dcm)

# 复制Dicom图像中的像素数据
img = slices[ int(len(slices)/2) ].image.copy()


# 对图像进行阈值分割
ret,mm = cv2.threshold(mm, 100,1, cv2.THRESH_BINARY)

#uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
mm = numpy.uint8(mm)

for j in range(img.shape[0]):            #遍历行
    for i in range(img.shape[1]):        #遍历列
        if mm[j,i]==0 :
            img[j,i]=-2000#写入像素点值
        if img[j,i]>800 :
            img[j,i]=-2000
io.imsave( 'test_thred.jpg', img)

#根据分割mask获取分割结果的像素数据
# img2 = slices[ int(len(slices)/2) ].image.copy()
# img2[(img == 0)] = -2000

# 显式原始数据，mask和分割结果
plt.figure(figsize=(12, 12))
plt.subplot(131)
plt.imshow(slices[int(len(slices) / 2)].image, 'gray')
plt.title('Original')
plt.subplot(132)
plt.imshow(img, 'gray')
plt.title('Target Region')
plt.subplot(133)
plt.imshow(mm, 'gray')
plt.title('Result')
plt.show()