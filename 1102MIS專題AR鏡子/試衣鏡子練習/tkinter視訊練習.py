import cv2
import tkinter as tk
from PIL import Image,ImageTk

def take_snapshot():
    print("有人給你點贊啦！")

def video_loop():
    success, img = camera.read()  # 從攝像頭讀取照片
    if success:
        cv2.waitKey(0)
        cv2image = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)#轉換顏色從BGR到RGBA
        current_image = Image.fromarray(cv2image)#將影象轉換成Image物件
        imgtk = ImageTk.PhotoImage(image=current_image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)
        root.after(1, video_loop)

camera = cv2.VideoCapture(0)    #攝像頭
root = tk.Tk()
root.title("opencv + tkinter")
#root.protocol('WM_DELETE_WINDOW', detector)
panel = tk.Label(root)  # initialize image panel
panel.pack(padx=10, pady=10)
root.config(cursor="arrow")
btn = tk.Button(root, text="點贊!", command=take_snapshot)
btn.pack(fill="both", expand=True, padx=10, pady=10)

video_loop()

root.mainloop()
# 當一切都完成後，關閉攝像頭並釋放所佔資源
camera.release()
cv2.destroyAllWindows()