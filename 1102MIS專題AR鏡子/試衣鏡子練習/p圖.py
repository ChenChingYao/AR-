import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
from IPython.display import clear_output


# img1 = cv2.imread('wonyoung_body.jpg')
# img2 = cv2.imread('cloth1.jpg')
# # img2 = cv2.resize(img2, (img1.shape[0],img1.shape[1]), interpolation=cv2.INTER_CUBIC)



#cv2.imshow("dst-1",dst)
#cv2.imshow("img1-1",img1)

def show_img(img, bigger=False):
    if bigger:
        plt.figure(figsize=(15,15))
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()

def resize_img(img, scale_percent):

    width = int(img.shape[1] * scale_percent / 100) # 縮放後圖片寬度
    height = int(img.shape[0] * scale_percent / 100) # 縮放後圖片高度
    dim = (width, height) # 圖片形狀 
    resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)  
    
    return resize_img
# Load two images
img1 = cv2.imread("wonyoung_body3.jpg")
img1 = cv2.resize(img1, (0, 0), fx = 0.7, fy = 0.7)
# print("Image1:")
# show_img(img1)

img2 = cv2.imread("pant1.png")
# print("Image2:")
# show_img(img2)
#img2 = resize_img(img2, scale_percent = 25) # 要放大縮小幾%
# print("resize Image2:")
# show_img(img2)

#調整img2的尺寸
img2 = cv2.resize(img2, (img1.shape[1],img1.shape[0]), interpolation=cv2.INTER_CUBIC)
#第一次訪設
rows, cols, ch = img2.shape
re_x = img1.shape[0]
re_y = img1.shape[1]
p1 = np.float32([[80*re_x, 40*re_y], [150*re_x, 40*re_y], [120*re_x, 110*re_y]])
 #p1 = np.float32([[0, 0], [cols-1, 0], [0, rows-1]])
p2 = np.float32([[90, 446], [169, 451], [int((102+176)/2), int((619+619)/2)]])
m = cv2.getAffineTransform(p1, p2)
dst = cv2.warpAffine(img2, m, (cols, rows))
img2 = dst



copyIma = img2.copy()
h, w = img2.shape[:2]
mask = np.zeros([h+2, w+2], np.uint8)
cv2.floodFill(copyIma, mask, (30, 30), (255, 255, 255), (100, 100, 100), (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)  

# print("floodFill:")
# show_img(copyIma)

# Now create a mask of logo and create its inverse mask also
img2gray = cv2.cvtColor(copyIma,cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)

# print("mask:")
# show_img(mask)

# I want to put logo on top-left corner, So I create a ROI
rows, cols, channels = img2.shape
x = 450 
y = 170
roi = img1#[y:y+rows, x:x+cols]
# print(img1.shape)
# print(img2.shape)
# print(roi.shape)

# print("Use mask to crop origin image1:")
# Now black-out the area of logo in ROI
img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
# show_img(img1_bg)

# print("mask_inv:")
mask_inv = cv2.bitwise_not(mask)
# show_img(mask_inv)

# print("Take element from image2:")
# Take only region of logo from logo image.
img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
# show_img(img2_fg)

# print("result image:")
# Put logo in ROI and modify the main image
dst = cv2.add(img1_bg,img2_fg)
img1 = dst#[y:y+rows, x:x+cols] = dst

#cv2.imshow("img1", img1)
#cv2.imshow("img2", img2)
cv2.imshow("dst", dst)
cv2.waitKey(0)
# show_img(img1, bigger=True)



