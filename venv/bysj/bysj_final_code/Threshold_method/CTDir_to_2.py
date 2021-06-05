import cv2
import numpy
import pydicom
from matplotlib import pyplot as plt
from matplotlib import image
from skimage import io,data
import os

def CT_to_2(mm,dir_name,CT_name,count):
    # 读取单张Dicom图像
    dcm = pydicom.read_file(dir_name+'/'+CT_name)
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

    # 获取图像中的像素数据
    slices = []
    slices.append(dcm)

    # 复制Dicom图像中的像素数据
    img = slices[int(len(slices) / 2)].image.copy()

    # 对图像进行阈值分割
    ret, img = cv2.threshold(img, 400, 3071, cv2.THRESH_BINARY)
    ret, mm = cv2.threshold(mm, 200, 1, cv2.THRESH_BINARY)

    # uint8是专门用于存储各种图像的（包括RGB，灰度图像等），范围是从0–255
    img = numpy.uint8(img)
    mm = numpy.uint8(mm)

    # 提取分割结果中的轮廓(cv2.findContours()函数来查找检测物体的轮廓)
    contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # numpy.zeros()把数组转换成想要的矩阵
    mask = numpy.zeros(img.shape, numpy.uint8)

    # 填充孔洞(cv2.fillPoly()函数可以用来填充任意形状的图型)
    for contour in contours:
        cv2.fillPoly(mask, [contour], 255)
    img[(mask > 0)] = 255

    # 对分割结果进行形态学的开操作
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))  # 返回指定形状和尺寸的结构元素
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)  # 形态学运算：MORPH_OPEN 开运算

    #  去除无关区域
    for j in range(img.shape[0]):  # 遍历行
        for i in range(img.shape[1]):  # 遍历列
            if mm[j, i] == 0:
                img[j, i] = 0  # 写入像素点值

    #name = os.path.splitext(CT_name)[0]
    io.imsave(str(count)+'.jpg',img)


if __name__ == '__main__':
    file_dir = 'E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE'	# 修改为你对应的文件路径
    listdir = os.listdir(file_dir)
    count = 0
    mm = image.imread("test2.jpg")
    for ct_name in listdir:
        count=count+1
        if count >280 :
            break
        CT_to_2(mm,file_dir,ct_name,count)
        print(str(count)+'_finish')
