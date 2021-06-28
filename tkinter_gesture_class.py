import tkinter as tk
import vlc
import os
import cv2
import HandTracking as ht 
import math
import numpy as np  
import sys
import time
import platform
if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import *
    from Tkinter.filedialog import askopenfilename
else:
    import tkinter as Tk
    from tkinter import *
    from tkinter.filedialog import askopenfilename
    from tkinter.messagebox import showinfo
import PIL
from PIL import Image 
from PIL import ImageTk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
from tkinter import messagebox


class App:
    def __init__(self,parent,media,window_title,video_source=0):
        self.window = Toplevel(parent)
        self.window.title(window_title)
        self.video_source = video_source
        self.media = media
        self.vid = MyVideoCapture(self.media,video_source)
        self.canvas = tk.Canvas(self.window, width = self.vid.WIDTH, height = self.vid.HEIGHT)
        self.canvas.pack()
        self.delay = 15
        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def on_closing(self):
        self.window.destroy()
        del self.vid
        cv2.destroyAllWindows()

        #uncomment these 4 lines for a message window
        # if messagebox.askokcancel("Quit", "Do you want to quit?"):
        #     self.window.destroy()
        #     del self.vid
        #     cv2.destroyAllWindows()

    def update(self):
     # Get a frame from the video source
        ret, frame = self.vid.get_frame()
 
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
 
        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self,media,video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        self.media = media
        if not self.vid.isOpened():
            raise ValueError("unable to open video source",video_source)

        self.WIDTH = 640
        self.HEIGHT = 480
        self.max_vol=150
        self.min_vol=0
        self.tipids = [4,8,12,16,20]
        self.detector = ht.handDetector(detectionCon=0.7)
        self.previoustime = time.time()
        self.vid.set(3,self.WIDTH)
        self.vid.set(4,self.HEIGHT)
        # self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            if ret:
                cv2.rectangle(frame,(5,5),(270,270),color=(255,22,0),thickness=2)
                cv2.putText(frame,"Perform the gesture inside the blue box",(70,430),cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,255,255),2,cv2.LINE_AA)
                detection_region = frame[5:270,5:270]
                detection_region = self.detector.findHands(detection_region)
                points_list = self.detector.findPosition(detection_region,draw=False)
                if len(points_list)!=0:
                    fingers = []
                    #for thumb
                    if points_list[self.tipids[0]][1] > points_list[self.tipids[0]-1][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                    for id in range(1,5):
                        if points_list[self.tipids[id]][2] < points_list[self.tipids[id]-2][2]:
                            fingers.append(1)
                        else:
                            fingers.append(0)
                    # print(fingers)
                    total_fingers = fingers.count(1)
                    # print(total_fingers)
                    # print(points_list)

                    #seek forward
                    if total_fingers == 2 and points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2]:
                        # print('forward')
                        video_position = vlc.libvlc_media_player_get_position(self.media)
                        if video_position == 1:
                            vlc.libvlc_media_player_set_position(self.media,video_position-0.01)
                        if video_position != -1:
                            vlc.libvlc_media_player_set_position(self.media,video_position+0.001)

                    #seek back
                    elif total_fingers == 3 and points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2] and points_list[16][2] < points_list[14][2]:
                        # print('backward')
                        video_position = vlc.libvlc_media_player_get_position(self.media)
                        if video_position == 0:
                            vlc.libvlc_media_player_set_position(self.media,video_position+0.01)
                        if video_position != -1:
                            vlc.libvlc_media_player_set_position(self.media,video_position-0.001)

                    #play-pause
                    elif total_fingers == 5 and  points_list[8][2] < points_list[6][2] and points_list[12][2] < points_list[10][2] and points_list[16][2] < points_list[14][2] and points_list[20][2] < points_list[18][2]:
                        currenttime = time.time()
                        # if currenttime-self.previoustime>3:
                        #     print('play/pause')
                        if currenttime-self.previoustime>3:
                            if vlc.libvlc_media_player_is_playing(self.media) == 1:
                                self.media.pause()
                            elif vlc.libvlc_media_player_is_playing(self.media) == 0:
                                self.media.play()
                        self.previoustime = currenttime

                    elif total_fingers == 2 and points_list[10][2] < points_list[12][2] and points_list[14][2] < points_list[16][2] and points_list[18][2] < points_list[20][2]:
                        cv2.line(frame, (points_list[8][1],points_list[8][2]),(points_list[4][1],points_list[4][2]),(0,255,255),10)
                        cv2.circle(frame,(points_list[8][1],points_list[8][2]),radius=8,color=(0,255,255),thickness=-1)
                        cv2.circle(frame,(points_list[4][1],points_list[4][2]),radius=8,color=(0,255,255),thickness=-1)
                        distance = math.sqrt((points_list[8][1]-points_list[4][1])**2+(points_list[8][2]-points_list[4][2])**2)
                        vol = int(np.interp(distance,[12,175],[self.min_vol,self.max_vol]))
                        # print(vol)
                        self.media.audio_set_volume(vol)

                    elif total_fingers == 0 and points_list[6][2] < points_list[8][2] and points_list[10][2] < points_list[12][2] and points_list[14][2] < points_list[16][2] and points_list[4][1] < points_list[3][1]:
                        currenttime = time.time()
                        # if currenttime-self.previoustime>3:
                        #     print('mute')
                        if currenttime-self.previoustime>3:
                            if vlc.libvlc_audio_get_mute(self.media):
                                vlc.libvlc_audio_set_mute(self.media,False)
                            else:
                                vlc.libvlc_audio_set_mute(self.media,True)
                        self.previoustime = currenttime
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret,None)
        else:
            return (ret,None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

def main():
    App(tk.Tk(),"Gesture Window")

if __name__ == '__main__':
    main()
