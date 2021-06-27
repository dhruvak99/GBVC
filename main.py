import tkinter as tk
import vlc
import cv2
import numpy as np
import os
import sys
import HandTracking as ht
import math
import time
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import *
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import *
    from tkinter.filedialog import askopenfilename
from PIL import Image 
from PIL import ImageTk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time
width, height = 640,480
min_limit,max_limit = 0,150
tipids = [4,8,12,16,20]
def detect_gestures(media):
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
    cap = cv2.VideoCapture(0)
    cap.set(3, width)
    cap.set(4, height)
    detector = ht.handDetector(detectionCon=0.7)
    previoustime = time.time()
    while True:
        # print(lmlist)
        success, img = cap.read()
        cv2.rectangle(img,(5,5),(270,270),color=(255,22,0),thickness=2)
        cv2.putText(img,"Perform the gesture inside the blue box",(70,430),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,22,0),2,cv2.LINE_AA)
        detection_region = img[5:270,5:270]
        detection_region = detector.findHands(detection_region)
        lmlist = detector.findPosition(detection_region, draw=False)
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
            
            # vlc.libvlc_media_player_get_position(media)
            # vlc.libvlc_media_player_set_position(media,a)

            #seek forward
            if total_fingers == 2 and lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2]:
                video_position = vlc.libvlc_media_player_get_position(media)
                if video_position == 1:
                    vlc.libvlc_media_player_set_position(media,video_position-0.01)
                if  video_position != -1:
                    vlc.libvlc_media_player_set_position(media,video_position+0.001)

                # print("forward")
                
            #seek backward
            elif total_fingers == 3 and lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2] and lmlist[16][2] < lmlist[14][2]:
                video_position = vlc.libvlc_media_player_get_position(media)
                if video_position == 0:
                    vlc.libvlc_media_player_set_position(media,video_position+0.01)
                if  video_position != -1:
                    vlc.libvlc_media_player_set_position(media,video_position-0.001)
                # print('backward')
                
                
            #play/pause
            elif total_fingers == 5 and  lmlist[8][2] < lmlist[6][2] and lmlist[12][2] < lmlist[10][2] and lmlist[16][2] < lmlist[14][2] and lmlist[20][2] < lmlist[18][2]:
                currenttime = time.time()
                # print(currenttime,previoustime)
                if currenttime-previoustime>3:
                    if vlc.libvlc_media_player_is_playing(media) == 1:
                        media.pause()
                    elif vlc.libvlc_media_player_is_playing(media) == 0:
                        media.play()
                previoustime = currenttime

            #volume gesture
            elif total_fingers == 2 and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[18][2] < lmlist[20][2]:
                cv2.line(img, (lmlist[8][1],lmlist[8][2]),(lmlist[4][1],lmlist[4][2]),(0,255,255),10)
                cv2.circle(img,(lmlist[8][1],lmlist[8][2]),radius=8,color=(0,255,255),thickness=-1)
                cv2.circle(img,(lmlist[4][1],lmlist[4][2]),radius=8,color=(0,255,255),thickness=-1) 
                distance = math.sqrt((lmlist[8][1]-lmlist[4][1])**2+(lmlist[8][2]-lmlist[4][2])**2)
                vol = int(np.interp(distance,[12,175],[min_limit,max_limit]))
                media.audio_set_volume(vol)
            
            #mute
            elif total_fingers == 0 and lmlist[6][2] < lmlist[8][2] and lmlist[10][2] < lmlist[12][2] and lmlist[14][2] < lmlist[16][2] and lmlist[4][1] < lmlist[3][1]:
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

def video_player():
    
    try:
        def open_file():
            video = askopenfilename(initialdir = Path(expanduser("~")),
                                title = "Choose a video",
                                filetypes = (("all files", "*.*"),
                                ("mp4 files", "*.mp4"),
                                ("mov files", "*.mov")))
            open_file.media = vlc.MediaPlayer(video)
            open_file.media.set_hwnd(frame.winfo_id())
            open_file.media.play()
            detect_gestures(open_file.media)
            volume_scale.set(vlc.libvlc_audio_get_volume(open_file.media))
        def quit_player():
            exit()

        def stop_file():
            if vlc.libvlc_media_player_is_playing(open_file.media):
                open_file.media.stop()
        def play(media):
            if vlc.libvlc_media_player_is_playing(media)==False:
                media.play()

        def pause(media):
            if vlc.libvlc_media_player_is_playing(media):
                media.pause()

        def forward(media):
            video_position = vlc.libvlc_media_player_get_position(media)
            if video_position == 1:
                vlc.libvlc_media_player_set_position(media,video_position-0.01)
            if video_position !=-1:
                vlc.libvlc_media_player_set_position(media,video_position+0.001)
        def backward(media):
            video_position = vlc.libvlc_media_player_get_position(media)
            if video_position == 0:
                vlc.libvlc_media_player_set_position(media,video_position+0.01)
            if video_position!=-1:
                vlc.libvlc_media_player_set_position(media,video_position-0.001)
        def set_volume(_=None):
            # volume = int(val)/100
            open_file.media.audio_set_volume(volume_scale.get())

        def stop_file():
            vlc.libvlc_media_player_stop(open_file.media)

    except:
        pass
            
    root = tk.Tk()
    root.title("VIDEO PLAYER")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    frame = tk.Frame(root, width=800, height=600,bg='white')
    frame.pack()
    menubar = Menu(root)
    file = Menu(menubar, tearoff=0)  
    file.add_command(label="Open",command=lambda:open_file()) 
    # file.add_command(label="Stop",command=lambda:stop_file())     
    file.add_command(label="Exit",command=quit_player)  
    menubar.add_cascade(label="File", menu=file)
    root.config(menu=menubar)
    photo = PhotoImage(file='icon.png')
    root.iconphoto(False,photo)

    #play icon
    play_image = Image.open('play.png')
    play_image = play_image.resize((50,50))
    play_icon = ImageTk.PhotoImage(play_image)
    button = tk.Button(root,image=play_icon,fg='black',command=lambda:play(open_file.media))
    button.place(relx=0.35,rely=0.9)

    #backward icon
    backward_img = Image.open('backward.png')
    backward_img = backward_img.resize((50,50))
    backward_icon = ImageTk.PhotoImage(backward_img)
    button3 = tk.Button(root,image=backward_icon,fg='white',command=lambda:backward(open_file.media))
    button3.place(relx=0.42,rely=0.9)

    #forward icon
    forward_img = Image.open('forward.png')
    forward_img = forward_img.resize((50,50))
    forward_icon = ImageTk.PhotoImage(forward_img)
    button2 = tk.Button(root,image=forward_icon,fg='black',command=lambda:forward(open_file.media))
    button2.place(relx=0.49,rely=0.9)

    #pause icon
    pause_img = Image.open('pause.png')
    pause_img = pause_img.resize((50,50))
    pause_icon = ImageTk.PhotoImage(pause_img)
    button1 = tk.Button(root,image=pause_icon,fg='black',command=lambda:pause(open_file.media))
    button1.place(relx=0.56,rely=0.9)
    
    volume_scale = tk.Scale(root,from_=0,to=150,orient=tk.HORIZONTAL,width=28,length=150,command=set_volume)
    volume_scale.place(relx=0.634,rely=0.9)


    root.minsize(800,600)
    root.maxsize(800,600)
    root.resizable(False,False)

    root.mainloop()


def main():
    '''
    start the video player
    then select the video 
    play the video 
    start the gesture recognition window
    start reconizing the gesture
    '''
    video_player()



if __name__ == '__main__':
    main()