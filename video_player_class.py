import tkinter as tk
import vlc
import os
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
from PIL import Image 
from PIL import ImageTk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time

class MenuBar(Menu,tk.Button,tk.Scale):
    def __init__(self,root):
        tk.Menu.__init__(self,root)
        self.parent = root
        file = Menu(self,tearoff = False)
        file.add_command(label="Open",command=self.OnOpen)
        # file.add_command(label="Stop")
        file.add_command(label="Exit",command=self.close)

        self.add_cascade(label="File",menu=file)

        #buttons 
        #play button
        self.play_image = Image.open('icon_images/play.png')
        self.play_image = self.play_image.resize((50,50))
        self.play_icon = ImageTk.PhotoImage(self.play_image)
        self.play_button = tk.Button(root,image=self.play_icon,fg='black',command=self.play_video)
        self.play_button.place(relx=0.35,rely=0.9)

        #pause icon
        self.pause_image = Image.open('icon_images/pause.png')
        self.pause_image = self.pause_image.resize((50,50))
        self.pause_icon = ImageTk.PhotoImage(self.pause_image)
        self.pause_button = tk.Button(root,image=self.pause_icon,fg='black',command=self.pause_video)
        self.pause_button.place(relx=0.56,rely=0.9)
        #forward icon
        self.forward_image = Image.open('icon_images/forward.png')
        self.forward_image = self.forward_image.resize((50,50))
        self.forward_icon = ImageTk.PhotoImage(self.forward_image)
        self.forward_button = tk.Button(root,image=self.forward_icon,fg='black',command=self.go_forward)
        self.forward_button.place(relx=0.49,rely=0.9)
        #backward_icon
        self.backward_image = Image.open('icon_images/backward.png')
        self.backward_image = self.backward_image.resize((50,50))
        self.backward_icon = ImageTk.PhotoImage(self.backward_image)
        self.backward_button = tk.Button(root,image=self.backward_icon,fg='black',command=self.go_back)
        self.backward_button.place(relx=0.42,rely=0.9)
        #gesture_icon
        self.gesture_image = Image.open('icon_images/gesture.png')
        self.gesture_image = self.gesture_image.resize((50,50))
        self.gesture_icon = ImageTk.PhotoImage(self.gesture_image)
        self.gesture_button =  tk.Button(root,image=self.gesture_icon,fg='black')
        self.gesture_button.place(relx=0.28,rely=0.9)

        self.volume_scale = tk.Scale(root,from_=0,to=150,orient=tk.HORIZONTAL,width=28,length=150,command=self.set_volume)
        self.volume_scale.place(relx=0.634,rely=0.9)

    def OnOpen(self):
        video = askopenfilename(initialdir = Path(expanduser("~")),
            title = "Choose a video file",
            filetypes = (("all files","*.*"),
                ("mp4 files", "*.mp4"),
                ("mov files", "*.mov")))

        self.Play(video)

    def Play(self,video):
        self.media = vlc.MediaPlayer(video)
        if platform.system() == 'Linux':
            self.media.set_xwindow(self.parent.winfo_id())
        if platform.system() == 'Windows':
            self.media.set_hwnd(self.parent.winfo_id())
        self.media.play()
        self.volume_scale.set(vlc.libvlc_audio_get_volume(self.media))
            
    def pause_video(self):
        if vlc.libvlc_media_player_is_playing(self.media):
            self.media.pause()

    def play_video(self):
        if vlc.libvlc_media_player_is_playing(self.media)==False:
            self.media.play()

    def go_back(self):
        video_position = vlc.libvlc_media_player_get_position(self.media)
        if video_position == 0:
            vlc.libvlc_media_player_set_position(self.media,video_position+0.01)
        if video_position!=-1:
            vlc.libvlc_media_player_set_position(media,video_position-0.001)

    def go_forward(self):
        video_position = vlc.libvlc_media_player_get_position(self.media)
        if video_position == 1:
            vlc.libvlc_media_player_set_position(self.media,video_position-0.01)
        if video_position!=-1:
            vlc.libvlc_media_player_set_position(media,video_position+0.001)

    def close(self):
        self.exit()

    def set_volume(self,_=None):
        self.media.audio_set_volume(self.volume_scale.get())

    def exit(self):
        exit()

class FrameBox(tk.Frame):
    def __init__(self,root):
        super().__init__(root)

        self.width = root.winfo_screenwidth()
        self.height = root.winfo_screenheight()
        self.frame = tk.Frame(root,width=self.width,height=self.height,bg='green')
        self.frame.pack()

class App(tk.Tk):
    def __init__(self):
        super().__init__()


        #configure root window
        self.title('Video Player')
        self.minsize(800,600)
        self.maxsize(800,600)
        self.resizable(False,False)
    

    def set_icon(self,path):
        player_icon = PhotoImage(file=path)
        self.iconphoto(False,player_icon)


def main():
    app = App()
    app.set_icon('icon_images/icon.png')
    frame = FrameBox(app)
    file_menu = MenuBar(app)
    app.config(menu=file_menu)
    app.mainloop()

if __name__ == '__main__':
    main()