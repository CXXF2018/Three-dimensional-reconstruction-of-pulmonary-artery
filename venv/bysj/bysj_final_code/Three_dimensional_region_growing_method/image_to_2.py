# 图片二值化
from PIL import Image

img = Image.open('testgeli.jpg')
img2 = Image.open('before100.jpg')
img3 = Image.open('before155.jpg')

# 模式L”为灰色图像，它的每个像素用8个bit表示，0表示黑，255表示白，其他数字表示不同的灰度。
Img = img.convert('L')
Img2 = img2.convert('L')
Img3 = img3.convert('L')

# 自定义灰度界限，大于这个值为黑色，小于这个值为白色
threshold = 200

table = []
table2 = []
table3 = []
for i in range(256):
    if i < threshold:
        table.append(0)
        table2.append(0)
        table3.append(0)
    else:
        table.append(1)
        table2.append(1)
        table3.append(1)

# 图片二值化
photo = Img.point(table, '1')
photo.save("testgeli.jpg")

photo2 = Img2.point(table, '1')
photo2.save("before100.jpg")

photo2 = Img3.point(table, '1')
photo2.save("before155.jpg")