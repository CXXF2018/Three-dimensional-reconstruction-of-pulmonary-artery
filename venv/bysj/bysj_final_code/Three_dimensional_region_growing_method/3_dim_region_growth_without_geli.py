# 区域生长 programmed by changhao
from PIL import Image
import matplotlib.pyplot as plt  # plt 用于显示图片
import numpy as np
import pydicom
import cv2
import numpy
from matplotlib import image
from skimage import io,data
import os

class Point(object):
    def __init__(self, x, y,z):
        self.x = x
        self.y = y
        self.z = z

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getY(self):
        return self.z

#读取所有图片，并保存到数组中
def getAllImages(path):
    file_dir = path  # 修改为你对应的文件路径
    listdir = os.listdir(file_dir)
    count = 0
    images = []
    for ct_name in listdir:
        count = count + 1
        if count > 280:
            break
        dcm = pydicom.read_file(file_dir + '/' + ct_name)
        dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept

        # 获取图像中的像素数据
        slices = []
        slices.append(dcm)

        # 复制Dicom图像中的像素数据
        img = slices[int(len(slices) / 2)].image.copy()
        images.append(img)

    print('图片导入完成,开始执行三维区域生长过程！！！')
    return images

#获取两个像素点的差值
def getGrayDiff(images, currentPoint, tmpPoint):
    return abs(int(images[currentPoint.z][currentPoint.x, currentPoint.y]) - int(images[tmpPoint.z][tmpPoint.x, tmpPoint.y]))

#可以扩展的领域
def selectConnects():

    connects = [ Point(-1, -1,0), Point(0, -1,0), Point(1, -1,0), Point(1, 0,0), Point(1, 1,0), \
                Point(0, 1,0), Point(-1, 1,0), Point(-1, 0,0),Point(-1, -1,1), Point(0, -1,1), Point(1, -1,1), Point(1, 0,1), Point(1, 1,1), \
                Point(0, 1,1), Point(-1, 1,1), Point(-1, 0,1),Point(0, 0,1), Point(-1, 0,-1),Point(-1, -1,-1), Point(0, -1,-1), Point(1, -1,-1), Point(1, 0,-1), Point(1, 1,-1), \
                Point(0, 1,-1), Point(-1, 1,-1), Point(-1, 0,-1),Point(0, 0,-1)]
    return connects

#三维区域生长
def regionGrow(images, seeds, thresh):
    count = 0
    height, weight = images[0].shape
    result = []
    while (count < len(images)):
        seedMark = np.zeros(images[0].shape)
        result.append(seedMark)
        count = count + 1

    seedList = []
    for seed in seeds:
        seedList.append(seed)
    connects = selectConnects()

    while (len(seedList) > 0):
        currentPoint = seedList.pop(0)

        #种子点是否符合要求
        if images[currentPoint.z][currentPoint.x, currentPoint.y] <200 :
            continue
        result[currentPoint.z][currentPoint.x, currentPoint.y] = images[currentPoint.z][currentPoint.x, currentPoint.y]

        for i in range(26):
            tmpX = currentPoint.x + connects[i].x
            tmpY = currentPoint.y + connects[i].y
            tmpZ = currentPoint.z + connects[i].z
            if tmpX < 0 or tmpY < 0 or tmpX >= height or tmpY >= weight or tmpZ<0 or tmpZ>=len(images):
                continue
            grayDiff = getGrayDiff(images, currentPoint, Point(tmpX, tmpY,tmpZ))
            if grayDiff < thresh and result[tmpZ][tmpX, tmpY] == 0:
                result[tmpZ][tmpX, tmpY] = images[tmpZ][tmpX, tmpY]
                seedList.append(Point(tmpX, tmpY,tmpZ))
    return result

#去除心脏
def getNeedRegion(images):
#220以后的删除
    img = image.imread("testgeli.jpg")
    img2 = image.imread("before155.jpg")
    img3 = image.imread("before100.jpg")
    count = 0

    while(len(images)>0):
        count = count + 1
        im = images.pop(0)
        io.imsave('image_without_geli/'+str(count) + '.jpg', im)
        print(str(count) + '_finish')



if __name__ == '__main__':
    path = 'E:/ctOperator/zhanglijuan/JDM0ZOYH/JPYS0CQE'
    images = getAllImages(path)
    count = 0

    seeds = [Point(250, 300,100), Point(300, 330,100), Point(250, 295,100),Point(280, 300,100)]

    res = regionGrow(images, seeds, 250)
    print('三维区域生长已完成，开始导出图片！！！')
    getNeedRegion(res)
