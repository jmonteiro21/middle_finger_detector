import cv2
import mediapipe as mp
import HandTrackingModule as htm
import random
import os

cap = cv2.VideoCapture(0)
detector = htm.handDetector()

tipIds = [4, 8, 12, 16, 20]
img_shown = False 

while True:
    fingers = [1, 0, 0, 0, 0]
    success, img = cap.read()
    img = detector.findHands(img, draw=False)
    lmList = detector.findPosition(img)

    if len(lmList) != 0:
    
        if lmList[12][2] < lmList[9][2]:
            for id in range(1, 5):
                if lmList[tipIds[id]][2] < lmList[11][2]:
                    fingers[id] = 1
                else:
                    fingers[id] = 0

        else:
            for id in range(1, 5):
                if lmList[tipIds[id]][2] > lmList[11][2]:
                    fingers[id] = 1
                else:
                    fingers[id] = 0


        if lmList[6][2] < lmList[10][2] and fingers != [1, 0, 1, 0, 0]:

            if lmList[12][1] > lmList[11][1]:
                for id in range(1, 5):
                    if lmList[tipIds[id]-1][1] > lmList[11][1]:
                        fingers[id] = 1
                    else:
                        fingers[id] = 0
                fingers[2] = 1
            
            if lmList[12][1] < lmList[11][1]:
                for id in range(1, 5):
                    if lmList[tipIds[id]-1][1] < lmList[11][1]:
                        fingers[id] = 1
                    else:
                        fingers[id] = 0
                fingers[2] = 1


        if lmList[6][2] > lmList[10][2] and fingers != [1, 0, 1, 0, 0]:

            if lmList[12][1] < lmList[11][1]:
                for id in range(1, 5):
                    if lmList[tipIds[id]-1][1] < lmList[11][1]:
                        fingers[id] = 1
                    else:
                        fingers[id] = 0
                fingers[2] = 1


    if fingers == [1, 0, 1, 0, 0]:

        if not img_shown:
            images = os.listdir("resizedImages")
            random_image = random.choice(images)
            imgPath = f"resizedImages/{random_image}"
            finger = cv2.imread(imgPath)

        cv2.putText(img, "Hey, right back at you BITCH!", (210, 30), cv2.FONT_HERSHEY_PLAIN, 1.70, (255,0,255), 2)
        h, w, c = finger.shape
        img[0:h, 0:w] = finger
        img_shown = True

    elif fingers != [1, 0, 1, 0, 0]:

        img_shown = False

    cv2.imshow("Middle Finger Detector", img)
    cv2.waitKey(1)

    if cv2.getWindowProperty("Middle Finger Detector", cv2.WND_PROP_VISIBLE) <1:
        break

cv2.destroyAllWindows()