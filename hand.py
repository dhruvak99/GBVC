import cv2
import time
import os
import HandTracking as ht


width, height = 640,480

cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

folderpath = "FingerImages"
mylist = os.listdir(folderpath)
print(mylist)
mylist.sort()
overlay = []
for imagepath in mylist:
    image = cv2.imread(f'{folderpath}/{imagepath}')
    print(f'{folderpath}/{imagepath}')
    overlay.append(image)
print(len(overlay))
previoustime = 0

detector = ht.handDetector(detectionCon=0.75)
tipids = [4,8,12,16,20]
while True:

    success, img = cap.read()
    img = detector.findHands(img)
    lmlist = detector.findPosition(img, draw=False)
    # print(lmlist)
    if len(lmlist)!=0:
        fingers = []
        #thumb
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
        print(total_fingers)

        img[0:200,0:200] = cv2.resize(overlay[total_fingers-1],(200,200))
    currenttime = time.time()
    fps = 1/(currenttime-previoustime)
    previoustime = currenttime
    cv2.putText(img,f'FPS: {int(fps)}',(400,70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)
    cv2.imshow("Image",img)
    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()
