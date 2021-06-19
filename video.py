import cv2
import time
import numpy as np 
import os
import HandTracking as ht
import pyautogui
import math

def main():
    '''
    return which gesture got detected
    '''
    width, height = 640,480
    min_limit,max_limit = 0,150
    tipids = [4,8,12,16,20]
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    detector = ht.handDetector(detectionCon=0.75)
    gesture = None
    previous_gesture = None
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
                gesture = 'forward'
                # print("forward")
                
            #seek backward
            elif total_fingers == 3 and lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2] and lmlist[16][2] < lmlist[14][2]:
                gesture = 'backward'
                # print('backward')
                
                
            #play/pause
            elif total_fingers == 5:
                gesture = 'play/pause'
                # print('play/pause')

            #volume gesture
            elif total_fingers == 2 and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
                cv2.line(img, (lmlist[8][1],lmlist[8][2]),(lmlist[4][1],lmlist[4][2]),(0,255,255),10)
                cv2.circle(img,(lmlist[8][1],lmlist[8][2]),radius=8,color=(0,255,255),thickness=-1)
                cv2.circle(img,(lmlist[4][1],lmlist[4][2]),radius=8,color=(0,255,255),thickness=-1) 
                distance = math.sqrt((lmlist[8][1]-lmlist[4][1])**2+(lmlist[8][2]-lmlist[4][2])**2)
                vol = int(np.interp(distance,[12,175],[min_limit,max_limit]))
                gesture = 'volume'
                # print('volume')
            
            #mute
            elif total_fingers == 0:
                gesture = 'mute'
                # print('mute')
            if gesture == previous_gesture:
                pass
            else:
                print(gesture)
                previous_gesture = gesture
        cv2.imshow("Image",img)
        k = cv2.waitKey(50)
        # if cv2.waitKey(5) & 0xFF == 27:
        #   break
        if k == 27:
            break
    cap.release()


# def main():
#     '''
#     takes the gesture as input and performs the automation
#     '''
#     while True:
#         hand()
#     # gesture = None
#     # previous_gesture = None
#     # while True:
#     #     if previous_gesture == 'play/pause' or previous_gesture == 'mute':
#     #         continue
#     #     gesture = hand()
#     #     if gesture == 'play/pause':
#     #         print(gesture)
#     #         # pyautogui.typewrite(['space'],0.5)
#     #         previous_gesture = 'play/pause'
#     #     elif gesture == 'mute':
#     #         print(gesture)
#     #         # pyautogui.press('m')
#     #         previous_gesture = 'mute'
#     #     elif gesture == 'forward':
#     #         print(gesture)
#     #         # pyautogui.hotkey('shift','right')
#     #         previous_gesture = 'forward'
#     #     elif gesture == 'backward':
#     #         print(gesture)
#     #         # pyautogui.hotkey('shift','left')
#     #         previous_gesture = 'backward'
#     #     elif gesture == 'volume':
#     #         print(gesture)
#     #         previous_gesture = 'volume'

if __name__ == '__main__':
    main()

