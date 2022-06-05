import cv2
import numpy as np
import mediapipe as mp
import  time

cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
hand_lms_style = mp_draw.DrawingSpec(color = (0, 0, 255), thickness = 5)
hand_con_style = mp_draw.DrawingSpec(color = (0, 255, 0), thickness = 10)
ptime = 0
ctime = 0


while True:
    ret, img = cap.read()
    if ret:

        img_height = img.shape[0]
        img_width = img.shape[1]
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(img_rgb)

        if(result.multi_hand_landmarks):
            for hand_lms in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_lms, mp_hands.HAND_CONNECTIONS, hand_lms_style, hand_con_style)
                for i, lm in enumerate(hand_lms.landmark):
                    xpos = int(lm.x * img_width)
                    ypos = int(lm.y * img_height)
                    cv2.putText(img, str(i), (xpos-25, ypos+5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.6, (0, 0, 255), 1)
                    print(i, xpos, ypos)

        ctime = time.time()
        fps = 1/(ctime - ptime)
        ptime = ctime
        cv2.putText(img, "fps : "+str(int(fps)), (30, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
        cv2.imshow("img", img)

    if(cv2.waitKey(1) == ord('q')):
        break

cap.release()
cv2.destroyAllWindows()