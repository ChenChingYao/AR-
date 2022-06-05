import tkinter as tk
import cv2
from cv2 import VideoCapture
from PIL import Image,ImageTk

root = tk.Tk()
cap = VideoCapture(0)
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

L3=tk.Label(root,text='試衣鏡子',bg='#FFFACD',fg="#DAA520",
            font=("Algerian",18,"bold"))
L3.pack()

def take_snapshot():
    print("有人給你點贊啦！")
btn = tk.Button(root, text="點贊!", command=take_snapshot)
btn.pack(fill="both", expand=True, padx=10, pady=10)

def video_loop():
    success, img = cap.read()  # 從攝像頭讀取照片
    #print(img.shape)
    if success:
        img = cv2.resize(img, (0, 0), fx = 1.2, fy = 1.2)
        cv2.waitKey(0)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
        current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)

cap = cv2.VideoCapture(1)    #鏡頭
panel = tk.Label(root)  # initialize image panel
panel.pack(padx=100, pady=0)




#呼叫鏡頭輸入
video_loop()
root.mainloop()#持續顯示視窗
#釋放鏡頭
cap.release()
cv2.destroyAllWindows()