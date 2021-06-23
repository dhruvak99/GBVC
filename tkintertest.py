import tkinter as tk
import vlc
import os
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image 
from PIL import ImageTk
from os.path import basename, expanduser, isfile, join as joined
from pathlib import Path



class menuItems(tk.Frame):
	def __init__(self):
		menubar = Menu(root)
		file = Menu(menubar, tearoff=0)  
		file.add_command(label="Open",command=self.open)      
		file.add_command(label="Exit",command=self.ex)  
		menubar.add_cascade(label="File", menu=file)
		root.config(menu=menubar)

	def open(self):
		video = askopenfilename(initialdir = Path(expanduser("~")),
                            title = "Choose a video",
                            filetypes = (("all files", "*.*"),
                            ("mp4 files", "*.mp4"),
                            ("mov files", "*.mov")))
	def ex(self):
		exit()


def main():
	root = tk.Tk()
	root.title("VIDEO PLAYER")
	frame = tk.Frame(root, width=700, height=600,bg='black')
	frame.pack()
	menubar = menuItems()

	photo = PhotoImage(file='icon.png')
	root.iconphoto(False,photo)
	img1 = Image.open('pl.jpg')
	img1 = img1.resize((50,50))

	play_icon = ImageTk.PhotoImage(img1)
	button = tk.Button(root,image=play_icon,fg='black',command=lambda:play(media))
	button.place(relx=0.2,rely=0.9)

	img = Image.open('pa.jpg')
	img = img.resize((50,50))

	pause_icon = ImageTk.PhotoImage(img)
	button1 = tk.Button(root,image=pause_icon,fg='black',command=lambda:pause(media))
	button1.place(relx=0.7,rely=0.9)
	root.mainloop()

if __name__ == '__main__':
	main()