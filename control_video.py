import cv2
import time
import numpy as np 
import os
import HandTracking as ht
import pyautogui
import math
width, height = 640,480
min_limit,max_limit = 0,150
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
folderpath = "gestures"
mylist = os.listdir(folderpath)
print(mylist)
mylist.sort()
overlay = []
for imagepath in mylist:
    image = cv2.imread(f'{folderpath}/{imagepath}')
    print(f'{folderpath}/{imagepath}')
    overlay.append(image)
detector = ht.handDetector(detectionCon=0.75)
tipids = [4,8,12,16,20]
gesture_detected = False
while True:
    # print(lmlist)
    success, img = cap.read()
    for i in range(0,1000):
        pass
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    if len(lmlist)!=0:
        fingers = []
        #for thumb
        if lmlist[tipids[0]][1] > lmlist[tipids[0]-1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        #other Fingers
        for id in range(1,5):
            if lmlist[tipids[id]][2] < lmlist[tipids[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        total_fingers = fingers.count(1)

        #seek forward
        if total_fingers == 2 and lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2]:
            img[0:200,0:200] = cv2.resize(overlay[1],(200,200))
            pyautogui.hotkey('shift','right')
            print("seek forward gesture")
            gesture_detected = True

        #seek backward
        elif total_fingers == 3 and lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2] and lmlist[16][2] < lmlist[14][2]:
            img[0:200,0:200] = cv2.resize(overlay[2],(200,200))
            pyautogui.hotkey('shift','left')
            
            print("seek backward gesture")
            gesture_detected = True
            
        #play/pause
        elif total_fingers == 5:
            img[0:200,0:200] = cv2.resize(overlay[4],(200,200))
            # pyautogui.typewrite(['space'],0.5)
            
            print("play/pause gesture")
            gesture_detected = True

        #volume gesture
        #volume decrease feature
        elif total_fingers == 2 and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
            img[0:200,0:200] = cv2.resize(overlay[0],(200,200))
            # print("volume gesture")
            cv2.line(img, (lmlist[8][1],lmlist[8][2]),(lmlist[4][1],lmlist[4][2]),(0,255,255),10)
            cv2.circle(img,(lmlist[8][1],lmlist[8][2]),radius=8,color=(0,255,255),thickness=-1)
            cv2.circle(img,(lmlist[4][1],lmlist[4][2]),radius=8,color=(0,255,255),thickness=-1) 
            distance = math.sqrt((lmlist[8][1]-lmlist[4][1])**2+(lmlist[8][2]-lmlist[4][2])**2)
            
            vol = int(np.interp(distance,[12,175],[min_limit,max_limit]))
            if int(vol) > 75:
                print("increasing volume")
                pyautogui.hotkey('ctrl','up')
            else:
                print("decreasing volume")
                pyautogui.hotkey('ctrl','down')
            # previous_volume = vol
            # time.sleep(0.001)
            # if np.interp(distance,[12,175],[min_limit,max_limit]) < previous_volume:
            #     print("decrease volume")
            #     previous_volume = np.interp(distance,[12,175],[min_limit,max_limit])
            # else:
            #     print("increase volume")
            # print("volume gesture :"+str(int(vol)))
            gesture_detected = True
        #mute
        elif total_fingers == 0:
            img[0:200,0:200] = cv2.resize(overlay[3],(200,200))
            pyautogui.press('m')
            # gestures[4]=1
            print("mute/fist closed")
            gesture_detected = True
    cv2.imshow("Image",img)
    k = cv2.waitKey(50)
    # if cv2.waitKey(5) & 0xFF == 27:
    #   break
    if k == 27:
        break
cap.release()
