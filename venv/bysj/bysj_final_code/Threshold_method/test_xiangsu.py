import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data

# 读取单张Dicom图像
dcm = pydicom.read_file("E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE/I2110000.dcm")
dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept
mm = image.imread("test2.jpg")

# 获取图像中的像素数据
slices = []
slices.append(dcm)

# 复制Dicom图像中的像素数据
img = slices[ int(len(slices)/2) ].image.copy()


# 对图像进行阈值分割
#ret,img = cv2.threshold(img, 775,3071, cv2.THRESH_BINARY)
ret,mm = cv2.threshold(mm, 200,1, cv2.THRESH_BINARY)

#uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
img = numpy.uint8(img)
mm = numpy.uint8(mm)

#提取分割结果中的轮廓(cv2.findContours()函数来查找检测物体的轮廓)
contours, _ = cv2.findContours(img,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

#numpy.zeros()把数组转换成想要的矩阵
mask = numpy.zeros(img.shape, numpy.uint8)

#填充孔洞(cv2.fillPoly()函数可以用来填充任意形状的图型)
for contour in contours:
    cv2.fillPoly(mask, [contour], 255)
img[(mask > 0)] = 255

#对分割结果进行形态学的开操作
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(2,2))#返回指定形状和尺寸的结构元素
img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)#形态学运算：MORPH_OPEN 开运算

#io.imsave('test.jpg',img)
for j in range(img.shape[0]):            #遍历行
    for i in range(img.shape[1]):        #遍历列
        if mm[j,i]==0 :
            img[j,i]=0       #写入像素点值

#根据分割mask获取分割结果的像素数据
# img2 = slices[ int(len(slices)/2) ].image.copy()
# img2[(img == 0)] = -2000

# 显式原始数据，mask和分割结果
plt.figure(figsize=(12, 12))
plt.subplot(131)
plt.imshow(slices[int(len(slices) / 2)].image, 'gray')
plt.title('Original')
plt.subplot(132)
plt.imshow(mm, 'gray')
plt.title('target')
plt.subplot(133)
plt.imshow(img, 'gray')
plt.title('Result')
plt.show()