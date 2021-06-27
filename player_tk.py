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
from PIL import Image 
from PIL import ImageTk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path
import time

def main():
	
	try:
		def open_file():
			video = askopenfilename(initialdir = Path(expanduser("~")),
	                            title = "Choose a video",
	                            filetypes = (("all files", "*.*"),
	                            ("mp4 files", "*.mp4"),
	                            ("mov files", "*.mov")))
			open_file.media = vlc.MediaPlayer(video)
			if platform.system() == 'Linux':
				open_file.media.set_xwindow(frame.winfo_id())
			if platform.system() == 'Windows':
				open_file.media.set_hwnd(frame.winfo_id())
			open_file.media.play()
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

		def gesture_controller():
			'''
			call the gesture_detection program
			
			'''

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
	file.add_command(label="Stop",command=lambda:stop_file())     
	file.add_command(label="Exit",command=quit_player)  
	menubar.add_cascade(label="File", menu=file)
	root.config(menu=menubar)
	photo = PhotoImage(file='icon_images/icon.png')
	root.iconphoto(False,photo)

	#play icon
	play_image = Image.open('icon_images/play.png')
	play_image = play_image.resize((50,50))
	play_icon = ImageTk.PhotoImage(play_image)
	button = tk.Button(root,image=play_icon,fg='black',command=lambda:play(open_file.media))
	button.place(relx=0.35,rely=0.9)

	#backward icon
	backward_img = Image.open('icon_images/backward.png')
	backward_img = backward_img.resize((50,50))
	backward_icon = ImageTk.PhotoImage(backward_img)
	button3 = tk.Button(root,image=backward_icon,fg='white',command=lambda:backward(open_file.media))
	button3.place(relx=0.42,rely=0.9)

	#forward icon
	forward_img = Image.open('icon_images/forward.png')
	forward_img = forward_img.resize((50,50))
	forward_icon = ImageTk.PhotoImage(forward_img)
	button2 = tk.Button(root,image=forward_icon,fg='black',command=lambda:forward(open_file.media))
	button2.place(relx=0.49,rely=0.9)

	#pause icon
	pause_img = Image.open('icon_images/pause.png')
	pause_img = pause_img.resize((50,50))
	pause_icon = ImageTk.PhotoImage(pause_img)
	button1 = tk.Button(root,image=pause_icon,fg='black',command=lambda:pause(open_file.media))
	button1.place(relx=0.56,rely=0.9)

	#gesture button
	gesture_img = Image.open('icon_images/gesture.png')
	gesture_img = gesture_img.resize((50,50))
	gesture_icon = ImageTk.PhotoImage(gesture_img)
	button4 = tk.Button(root,image=gesture_icon,fg='black')
	button4.place(relx=0.28,rely=0.9)
	
	volume_scale = tk.Scale(root,from_=0,to=150,orient=tk.HORIZONTAL,width=28,length=150,command=set_volume)
	volume_scale.place(relx=0.634,rely=0.9)


	root.minsize(800,600)
	root.maxsize(800,600)
	root.resizable(False,False)
	root.mainloop()

if __name__ == '__main__':
	main()