from threading import Timer
from turtle import left
import cv2
import tkinter as tk
import tkinter.ttk
from PIL import Image,ImageTk
import time
from cv2 import imread
import mediapipe as mp
import numpy as np

#骨架初始化
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

#衣服
img_cloth1 = cv2.imread("cloth1.png")
img_cloth2 = cv2.imread("cloth2.png")
#褲子
img_pants1 = cv2.imread("pants1.png")
img_pants2 = cv2.imread("pants2.png")
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
    p1 = np.float32([[190,130], [580,130], [400, 550]])
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


#Tkinter初始化
root = tk.Tk()
cap = cv2.VideoCapture(0)
sucess, img = cap.read()

print(root.winfo_screenwidth()) #輸出螢幕寬度
print(root.winfo_screenheight()) #輸出螢幕高度
w=1200 #width
r=700  #height
x=100  #與視窗左上x的距離
y=30  #與視窗左上y的距離
root.geometry('%dx%d+%d+%d' % (w,r,x,y))

root.resizable(0,0)#關閉調整視窗大小
root.title('tkinter練習')#視窗標題

#ui顯示畫面
L3=tk.Label(root,text='試衣鏡子',bg='#FFFACD',fg="#DAA520",
            font=("Algerian",32,"bold"))
L3.place(x=10, y=10)

timer = [0, 0, 0, 0]#衣服1、衣服2、褲子1、褲子2
#cloth1圖示
photo_cloth1 = Image.open("cloth1.png")
photo_cloth1 = photo_cloth1.resize((72, 63), Image.ANTIALIAS)
photo_cloth1 = ImageTk.PhotoImage(photo_cloth1)
#cloth2圖示
photo_cloth2 = Image.open("cloth2.png")
photo_cloth2 = photo_cloth2.resize((72,63), Image.ANTIALIAS)
photo_cloth2 = ImageTk.PhotoImage(photo_cloth2)
#pants1圖示
photo_pants1 = Image.open("pants1.png")
photo_pants1 = photo_pants1.resize((72,63), Image.ANTIALIAS)
photo_pants1 = ImageTk.PhotoImage(photo_pants1)
#pants2圖示
photo_pants2 = Image.open("pants2.png")
photo_pants2 = photo_pants2.resize((72,63), Image.ANTIALIAS)
photo_pants2 = ImageTk.PhotoImage(photo_pants2)
#衣服的單選按鈕
cloth_value = tk.IntVar()#現在衣服的值
cloth0_radio = tk.Radiobutton(root, text= 'none', variable=cloth_value, value=0)
cloth0_radio.select() 
cloth0_radio.place(x=240, y=580)
cloth1_radio = tk.Radiobutton(root, text= 'cloth1', variable=cloth_value, value=1, image = photo_cloth1) 
cloth1_radio.place(x=300, y=580)
cloth2_radio = tk.Radiobutton(root, text= 'cloth2', variable=cloth_value, value=2, image = photo_cloth2) 
cloth2_radio.place(x=400, y=580)

pants_value = tk.IntVar()#現在庫子的值
pants0_radio = tk.Radiobutton(root, text= 'none', variable=pants_value, value=0) 
pants0_radio.select()
pants0_radio.place(x=240, y=640)
pants1_radio = tk.Radiobutton(root, text= 'cloth1', variable=pants_value, value=1, image = photo_pants1) 
pants1_radio.place(x=300, y=640)
pants2_radio = tk.Radiobutton(root, text= 'cloth2', variable=pants_value, value=2, image = photo_pants2) 
pants2_radio.place(x=400, y=640)


#讀入畫面
cap = cv2.VideoCapture(0)    #鏡頭
panel = tk.Label(root)  # initialize image panel
panel.place(x=250, y=0)

#將運算完的img轉成tkinter輸出顏色
def draw_img(img):
    cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
    current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
    imgtk = ImageTk.PhotoImage(image=current_image)
    panel.imgtk = imgtk
    panel.config(image=imgtk)
    root.after(10, video_loop)

#讀鏡頭迴圈
def video_loop():
    success, img = cap.read()  # 從攝像頭讀取照片
    img = cv2.resize(img, (0, 0), fx = 1.2, fy = 1.2)
    #print(img.shape)
    # if success:
    #     cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
    #     current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
    #     imgtk = ImageTk.PhotoImage(image=current_image)
    #     panel.imgtk = imgtk
    #     panel.config(image=imgtk)
    #     root.after(1, video_loop)
    
    

    #骨架ai
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pose.process(imgRGB)
    
    if(result.pose_landmarks):
        
        for id, lm in enumerate(result.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x*w), int(lm.y*h)
            #cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
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
            elif(id == 26):#右膝蓋
                pants[1] = cx, cy
            elif(id == 28):#右腳踝
                pants[2] = cx, cy
            elif(id == 25):#左膝蓋
                pants[4] = cx, cy
            elif(id == 27):#左腳踝
                pants[5] = cx, cy

    #讀取後台data_base
    
    if(cloth_value.get() == 0 and pants_value.get() == 0):
        end_img = img
    else:
        end_img = img
        #貼上衣服
        if(cloth_value.get() == 1):
            print("cloth1")
            end_img = mix_cloth(end_img, img_cloth1)
        elif(cloth_value.get() == 2):
            print("cloth2")
            end_img = mix_cloth(end_img, img_cloth2)
        
        #貼上褲子
        if(pants_value.get() == 1):
            print("pants1")
            end_img = mix_pants(end_img, img_pants1)
        elif(pants_value.get() == 2):
            print("pants2")
            end_img = mix_pants(end_img, img_pants2)

    draw_img(end_img)
    cv2.waitKey(0)

#呼叫鏡頭輸入
video_loop()
root.mainloop()#持續顯示視窗
#釋放鏡頭
cap.release()
cv2.destroyAllWindows()