import cv2
import time
import numpy as np 
import os
import sys
import vlc
import HandTracking as ht
import math

def detect_gestures():
    '''
    The following functions has been used to control the mediaplayerinstance
    vlc.libvlc_media_player_get_position(media)
    vlc.libvlc_media_player_set_position(media,percentage_value)
    media.audio_set_volume(volume_value)
    media.play()
    media.pause()
    vlc.libvlc_audio_get_mute(p_mi)
    vlc.libvlc_audio_set_mute(media,True)
    vlc.libvlc_audio_set_mute(media,False)
    '''
    
    if len(sys.argv)!=2:
        print("No Video path provided")
        exit()
    media = vlc.MediaPlayer(sys.argv[1])
    # vlc_instance = vlc.Instance()
    media.play()
    width, height = 640,480
    min_limit,max_limit = 0,150
    tipids = [4,8,12,16,20]
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    detector = ht.handDetector(detectionCon=0.7)
    previoustime = time.time()
    while True:
        # print(points_list)
        success, img = cap.read()
        cv2.rectangle(img,(5,5),(270,270),color=(255,22,0),thickness=2)
        cv2.putText(img,"Perform the gesture inside the blue box",(70,430),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,22,0),2,cv2.LINE_AA)
        detection_region = img[5:270,5:270]
        detection_region = detector.findHands(detection_region)
        points_list = detector.findPosition(detection_region, draw=False)
        if len(points_list)!=0:
            fingers = []
            #for thumb
            if points_list[tipids[0]][1] > points_list[tipids[0]-1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
            #other Fingers
            for id in range(1,5):
                if points_list[tipids[id]][2] < points_list[tipids[id]-2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)
            # print(fingers)
            total_fingers = fingers.count(1)
            
            # vlc.libvlc_media_player_get_position(media)
            # vlc.libvlc_media_player_set_position(media,a)

            #seek forward
            if total_fingers == 2 and points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2]:
                video_position = vlc.libvlc_media_player_get_position(media)
                if video_position == 1:
                    vlc.libvlc_media_player_set_position(media,video_position-0.01)
                if  video_position != -1:
                    vlc.libvlc_media_player_set_position(media,video_position+0.001)

                # print("forward")
                
            #seek backward
            elif total_fingers == 3 and points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2] and points_list[16][2] < points_list[14][2]:
                video_position = vlc.libvlc_media_player_get_position(media)
                if video_position == 0:
                    vlc.libvlc_media_player_set_position(media,video_position+0.01)
                if  video_position != -1:
                    vlc.libvlc_media_player_set_position(media,video_position-0.001)
                # print('backward')
                
                
            #play/pause
            elif total_fingers == 5 and  points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2] and points_list[16][2] < points_list[14][2] and points_list[20][2] < points_list[18][2]:
                currenttime = time.time()
                # print(currenttime,previoustime)
                if currenttime-previoustime>3:
                    if vlc.libvlc_media_player_is_playing(media) == 1:
                        media.pause()
                    elif vlc.libvlc_media_player_is_playing(media) == 0:
                        media.play()
                previoustime = currenttime

            #volume gesture
            elif total_fingers == 2 and points_list[10][2] < points_list[12][2] and points_list[14][2] < points_list[16][2] and points_list[18][2] < points_list[20][2]:
                cv2.line(img, (points_list[8][1],points_list[8][2]),(points_list[4][1],points_list[4][2]),(0,255,255),10)
                cv2.circle(img,(points_list[8][1],points_list[8][2]),radius=8,color=(0,255,255),thickness=-1)
                cv2.circle(img,(points_list[4][1],points_list[4][2]),radius=8,color=(0,255,255),thickness=-1) 
                distance = math.sqrt((points_list[8][1]-points_list[4][1])**2+(points_list[8][2]-points_list[4][2])**2)
                vol = int(np.interp(distance,[12,175],[min_limit,max_limit]))
                media.audio_set_volume(vol)
            
            #mute
            elif total_fingers == 0 and points_list[6][2] < points_list[8][2] and points_list[10][2] < points_list[12][2] and points_list[14][2] < points_list[16][2] and points_list[4][1] < points_list[3][1]:
                currenttime = time.time()
                # print(currenttime,previoustime)
                # vlc.libvlc_audio_get_mute(p_mi)
                # vlc.libvlc_audio_set_mute(media,True)
                # vlc.libvlc_audio_set_mute(media,False)
                if currenttime-previoustime>3:
                    if vlc.libvlc_audio_get_mute(media):
                        vlc.libvlc_audio_set_mute(media,False)
                    else:
                        vlc.libvlc_audio_set_mute(media,True)
                previoustime = currenttime
        cv2.imshow("Image",img)
        k = cv2.waitKey(50)
        # if cv2.waitKey(5) & 0xFF == 27:
        #   break
        if k == 27:
            break
    cap.release()

if __name__ == '__main__':
    detect_gestures()

