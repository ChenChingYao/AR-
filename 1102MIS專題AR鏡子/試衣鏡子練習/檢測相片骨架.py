import cv2
import time
import mediapipe as mp

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
cloth = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] #右手軸 右肩 左肩 左手軸 又屁股 左屁股
pants = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]] #又屁股 右膝蓋 右腳踝 左屁股 左膝蓋 左腳踝


img = cv2.imread("wonyoung_body3.jpg")
imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
result = pose.process(imgRGB)
img = cv2.resize(img, (0, 0), fx = 0.7, fy = 0.7)
print(img.shape)

if(result.pose_landmarks):
    mpDraw.draw_landmarks(img, result.pose_landmarks, mpPose.POSE_CONNECTIONS)
    cv2.imshow("img", img)

    for id, lm in enumerate(result.pose_landmarks.landmark):
        h, w, c = img.shape
        cx, cy = int(lm.x*w), int(lm.y*h)
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        print(id, cx, cy)

    # 衣服
        if(id == 14):  # 右手軸
            cloth[0] = cx, cy
        elif(id == 12):  # 右肩膀
            cloth[1] = cx, cy
        elif(id == 11):  # 左肩膀
            cloth[2] = cx, cy
        elif(id == 13):  # 左手軸
            cloth[3] = cx, cy
        elif(id == 24):  # 又屁股
            cloth[4] = cx, cy
            pants[0] = cx, cy
        elif(id == 23):  # 左屁股
            cloth[5] = cx, cy
            pants[3] = cx, cy
        # 庫子
        # if(id == 24):#又屁股
        #     pants[0] = cx, cy
        elif(id == 26):  # 右膝蓋
            pants[1] = cx, cy
        elif(id == 28):  # 右腳踝
            pants[2] = cx, cy
        # if(id == 23):#左屁股
        #     pants[3] = cx, cy
        elif(id == 25):  # 左膝蓋
            pants[4] = cx, cy
        elif(id == 27):  # 左腳踝
            pants[5] = cx, cy
        print("cloth : ", cloth)
        print("pants : ", pants)


cv2.imshow("img", img)
cv2.waitKey(0)
