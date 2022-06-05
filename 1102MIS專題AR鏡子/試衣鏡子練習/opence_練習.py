import cv2
import numpy as np

kernel = np.ones((2, 2))

#圖形處裡
# img = cv2.imread('wonyoung.jpg')
# img = cv2.resize(img, (0, 0), fx = 0.2, fy = 0.2)
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blur = cv2.GaussianBlur(img, (5, 5), 0)
# canny = cv2.Canny(img, 100, 200)
# dilate = cv2.dilate(canny, kernel, iterations=1)

# cv2.imshow('img', img)
# cv2.imshow('canny', canny)
# cv2.imshow('gray', gray)
# cv2.imshow('blur', blur)
# cv2.imshow('dilate', dilate)
# cv2.waitKey(0)


#視訊鏡頭
# cap = cv2.VideoCapture(0)
# while(True):
#     ret, frame = cap.read()

#     frame = cv2.Canny(frame, 90, 180)
#     frame = cv2.dilate(frame, kernel, iterations=1)
#     cv2.imshow('frame', frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# cap.release()
# cv2.destroyAllWindows()


#ai人臉
# face = cv2.imread('wonyoung_face.jpg')
# face = cv2.resize(face, (0, 0), fx = 0.2, fy = 0.2)
# gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
# face_cascade = cv2.CascadeClassifier("face_detect.xml")
# face_rect = face_cascade.detectMultiScale(gray, 1.05, 10)
# print(len(face_rect))

# for (x, y, w, h) in face_rect:
#     cv2.rectangle(face, (x, y), (x+w, y+h), (0, 255, 0), 2)
# cv2.imshow('img', face)
# cv2.waitKey(0)

#ai
body = cv2.imread('wonyoung_face.jpg')
body = cv2.resize(body, (0, 0), fx = 0.2, fy = 0.2)
gray = cv2.cvtColor(body, cv2.COLOR_BGR2GRAY)
body_cascade = cv2.CascadeClassifier("smile_detect.xml")
body_rect = body_cascade.detectMultiScale(gray, 1.01, 100)
#print(len(body_rect))

if body_rect != ():
    for (x, y, w, h) in body_rect:
        cv2.rectangle(body, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print('body found')
cv2.imshow('body', body)
cv2.waitKey(0)