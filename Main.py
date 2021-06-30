from gbvcpkg import video_player_class as vpc

def main():
	app = vpc.App()
	app.set_icon('icon.png')
	file_menu = vpc.MenuBar(app)
	app.config(menu=file_menu)
	app.mainloop()

if __name__ == '__main__':
	main()
