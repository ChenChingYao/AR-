import cv2
import numpy as np

cloth = cv2.imread("cloth1.png")
body = cv2.imread("wonyoung_body.jpg")

#圖形訪設
rows, cols, ch = cloth.shape
p1 = np.float32([[180, 100], [430, 100], [200, 480]])
#p1 = np.float32([[0, 0], [cols-1, 0], [0, rows-1]])
p2 = np.float32([[192, 260], [361, 253], [246, 503]])
m = cv2.getAffineTransform(p1, p2)
dst = cv2.warpAffine(cloth, m, (cols, rows))

# #過濾背景
# copyIma = dst.copy()
# h, w = dst.shape[:2]
# mask = np.zeros([h+2, w+2], np.uint8)
# cv2.floodFill(copyIma, mask, (30, 30), (255, 255, 255), (100, 100, 100), (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)  

# #過濾背景後取的遮罩
# dstgray = cv2.cvtColor(copyIma,cv2.COLOR_BGR2GRAY)
# ret, mask = cv2.threshold(dstgray, 254, 255, cv2.THRESH_BINARY)

# #印上遮罩的位置
# rows, cols, channels = dst.shape
# x = 0
# y = 0
# roi = body[y:y+10, x:x+10]
# print("Use mask to crop origin image1:")
# img1_bg = cv2.bitwise_and(roi, roi, mask = mask)



cv2.imshow("cloth", cloth)
cv2.imshow("dst", dst)
cv2.waitKey(0)