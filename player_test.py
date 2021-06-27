import video_player_class as vpc

def main():
	app = vpc.App()
	app.set_icon('icon_images/icon.png')
	frame = vpc.FrameBox(app)
	file_menu = vpc.MenuBar(app)
	app.config(menu = file_menu)
	app.mainloop()

if __name__ == '__main__':
	main()