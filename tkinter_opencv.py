import tkinter as tk
import vlc
import os
import cv2
import HandTracking as ht 
import math
import numpy as np  
import sys
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
import time
import webcam_test as wt 
from tkinter import messagebox


class App:
    def __init__(self,parent,window_title,video_source=0):
        self.window = Toplevel(parent)
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(video_source)
        self.canvas = tk.Canvas(self.window, width = self.vid.width, height = self.vid.height)
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
    def __init__(self,video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("unable to open video source",video_source)


        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)


    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            if ret:
                cv2.rectangle(frame,(5,5),(270,270),color=(255,22,0),thickness=2)
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
