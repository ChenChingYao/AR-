from unittest import result
import cv2
import time
from cv2 import imread
import mediapipe as mp
import numpy as np
import matplotlib.pyplot as plt
import glob
from IPython.display import clear_output

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

#衣服
img_cloth = imread("cloth2.png")
#庫子
img_pants = imread("pants1.png")
#鏡頭
cap = cv2.VideoCapture(1)
#cap = cv2.VideoCapture("naeun.mp4")
ptime = 0
cloth = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] #右手軸 右肩 左肩 左手軸 又屁股 左屁股
pants = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] #又屁股 右膝蓋 右腳踝 左屁股 左膝蓋 左腳踝


#合成圖片尺寸調整
def resize_img(img, scale_percent):
    
    width = int(img.shape[1] * scale_percent / 100) # 縮放後圖片寬度
    height = int(img.shape[0] * scale_percent / 100) # 縮放後圖片高度
    dim = (width, height) # 圖片形狀 
    resize_img = cv2.resize(img, dim, interpolation = cv2.INTER_AREA) 
    return resize_img 

#圖片仿射加貼上
def mix_cloth(img1, img2):
    for i in cloth:
        if(i == 0):
            return img1
    #調整img2的尺寸
    #print(img1.shape)
    #print(img2.shape)
    shape_x = img1.shape[1]
    shape_y = img1.shape[0]
    img2 = cv2.resize(img2, (shape_x,shape_y), interpolation=cv2.INTER_AREA)
    rows, cols, ch = img2.shape
    p1 = np.float32([[240,110], [620,110], [400, 550]])
    #p1 = np.float32([[0, 0], [cols-1, 0], [0, rows-1]])
    p2 = np.float32([cloth[1], cloth[2], [int((cloth[4][0]+cloth[5][0])/2), int((cloth[4][1]+cloth[5][1])/2)]])
    m = cv2.getAffineTransform(p1, p2)
    dst = cv2.warpAffine(img2, m, (cols, rows))
    img2 = dst
    copyIma = img2.copy()
    h, w = img2.shape[:2]
    mask = np.zeros([h+2, w+2], np.uint8)
    cv2.floodFill(copyIma, mask, (30, 30), (255, 255, 255), (100, 100, 100), (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)  
    img2gray = cv2.cvtColor(copyIma,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)
    roi = img1
    img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
    mask_inv = cv2.bitwise_not(mask)
    img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
    dst = cv2.add(img1_bg,img2_fg)
    img1 = dst
    return dst

def mix_pants(img1, img2):
    #for i in range(2):
    #    if(pants[i] == 0):
    #        return 0
    #調整img2的尺寸
    img2 = cv2.resize(img2, (img1.shape[1],img1.shape[0]), interpolation=cv2.INTER_CUBIC)
    re_x = img1.shape[1]/100
    re_y = img1.shape[0]/100
    rows, cols, ch = img2.shape
    #p1 = np.float32([[80, 40], [150, 40], [120, 120]])
    p1 = np.float32([[280,110], [500,110], [400, 450]])
    p2 = np.float32([pants[0], pants[3], [int((pants[2][0]+pants[5][0])/2), int((pants[2][1]+pants[5][1])/2)]])
    m = cv2.getAffineTransform(p1, p2)
    dst = cv2.warpAffine(img2, m, (cols, rows))
    img2 = dst
    copyIma = img2.copy()
    h, w = img2.shape[:2]
    mask = np.zeros([h+2, w+2], np.uint8)
    cv2.floodFill(copyIma, mask, (30, 30), (255, 255, 255), (100, 100, 100), (50, 50, 50), cv2.FLOODFILL_FIXED_RANGE)  
    img2gray = cv2.cvtColor(copyIma,cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 254, 255, cv2.THRESH_BINARY)
    roi = img1
    img1_bg = cv2.bitwise_and(roi, roi, mask = mask)
    mask_inv = cv2.bitwise_not(mask)
    img2_fg = cv2.bitwise_and(img2, img2, mask = mask_inv)
    dst = cv2.add(img1_bg,img2_fg)
    img1 = dst
    return dst



def draw_cloth(img):
    img_draw = img
    arr = np.array([cloth[1], cloth[2], [cloth[2][0], cloth[5][1]], [cloth[1][0], cloth[4][1]]])
    img_draw = cv2.drawContours(img_draw, [arr], -1, (255, 0, 255), thickness=-1)
    img_draw = cv2.line(img_draw, cloth[0], cloth[1], (255,255,0), 20)
    img_draw = cv2.line(img_draw, cloth[2], cloth[3], (255,255,0), 20)
    return img_draw

def draw_pants(img):
    img_draw = img
    img_draw = cv2.line(img_draw, pants[0], pants[1], (0,255,255), 20)
    img_draw = cv2.line(img_draw, pants[1], pants[2], (0,255,255), 20)
    img_draw = cv2.line(img_draw, pants[3], pants[4], (0,255,255), 20)
    img_draw = cv2.line(img_draw, pants[4], pants[5], (0,255,255), 20)
    return img_draw

#main()
while True:
    success, img = cap.read()
    img = cv2.resize(img, (0, 0), fx = 1.25, fy = 1.25)
    #print(img.shape)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)

    ctime = time.time()
    fps = 1/(ctime - ptime)
    ptime = ctime
    cv2.putText(img, "FPS:" + str(int(fps)), (10, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
    if(result.pose_landmarks):
        cv2.imshow("img", img)
        mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
        #cv2.imshow("img", img)
        
        for id, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
            #print(id, cx, cy)

            #衣服
            if(id == 14):#右手軸
                cloth[0] = cx, cy
            elif(id == 12):#右肩膀
                cloth[1] = cx, cy
            elif(id == 11):#左肩膀
                cloth[2] = cx, cy
            elif(id == 13):#左手軸
                cloth[3] = cx, cy
            elif(id == 24):#又屁股
                cloth[4] = cx, cy
                pants[0] = cx, cy
            elif(id == 23):#左屁股
                cloth[5] = cx, cy
                pants[3] = cx, cy
            #庫子
            # if(id == 24):#又屁股
            #     pants[0] = cx, cy
            elif(id == 26):#右膝蓋
                pants[1] = cx, cy
            elif(id == 28):#右腳踝
                pants[2] = cx, cy
            # if(id == 23):#左屁股
            #     pants[3] = cx, cy
            elif(id == 25):#左膝蓋
                pants[4] = cx, cy
            elif(id == 27):#左腳踝
                pants[5] = cx, cy
        print("cloth : ", cloth)
        print("pants : ", pants)

    #cv2.imshow("img1", img)
    #cv2.imshow("img2", img_cloth)
    #img_draw = draw_cloth(img)
    #img_draw = draw_pants(img)
    #cv2.imshow("img_draw", img_cloth)
    img_mix = mix_cloth(img, img_cloth)
    img_mix = mix_pants(img_mix, img_pants)
    cv2.imshow("img_mix", img_mix)
    #cv2.imshow("img_pants", img_mix_pants)

    if(cv2.waitKey(1) == ord('q')):
        break