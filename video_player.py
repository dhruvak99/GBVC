import vlc
import sys

if sys.version_info[0] < 3:
    import Tkinter as Tk
    from Tkinter import ttk
    from Tkinter.filedialog import askopenfilename
    from Tkinter import PhotoImage
else:
    import tkinter as Tk
    from tkinter import ttk
    from tkinter.filedialog import askopenfilename
    from tkinter import PhotoImage

# import standard libraries
import os
import pathlib
from threading import Timer,Thread,Event
import time
import platform

class ttkTimer(Thread):
    """a class serving same function as wxTimer... but there may be better ways to do this
    """
    def __init__(self, callback, tick):
        Thread.__init__(self)
        self.callback = callback
        #print("callback= ", callback())
        self.stopFlag = Event()
        self.tick = tick
        self.iters = 0

    def run(self):
        while not self.stopFlag.wait(self.tick):
            self.iters += 1
            self.callback()
            #print("ttkTimer start")

    def stop(self):
        self.stopFlag.set()

    def get(self):
        return self.iters

class Player(Tk.Frame):
    """The main window has to deal with events.
    """
    def __init__(self, parent, title=None):
        Tk.Frame.__init__(self, parent)
    
        self.parent = parent

        if title == None:
            title = "tk_vlc"
        self.parent.title(title)

        # Menu Bar
        #   File Menu
        menubar = Tk.Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Tk.Menu(menubar)
        fileMenu.add_command(label="Open", command=self.OnOpen)
        fileMenu.add_command(label="Exit", command=_quit)
        menubar.add_cascade(label="File", menu=fileMenu)        

        # The second panel holds controls
        self.player = None
        self.videopanel = ttk.Frame(self.parent)
        self.canvas = Tk.Canvas(self.videopanel).pack(fill=Tk.BOTH,expand=1)
        self.videopanel.pack(fill=Tk.BOTH,expand=1)

        ctrlpanel = ttk.Frame(self.parent)
        pause  = ttk.Button(ctrlpanel, text="Pause", command=self.OnPause)
        play   = ttk.Button(ctrlpanel, text="Play", command=self.OnPlay)
        stop   = ttk.Button(ctrlpanel, text="Stop", command=self.OnStop)
        volume = ttk.Button(ctrlpanel, text="Volume", command=self.OnSetVolume)
        pause.pack(side=Tk.LEFT)
        play.pack(side=Tk.LEFT)
        stop.pack(side=Tk.LEFT)
        volume.pack(side=Tk.LEFT)
        self.volume_var = Tk.IntVar()
        self.volslider = Tk.Scale(ctrlpanel, variable=self.volume_var, command=self.volume_sel, 
                from_=0, to=100, orient=Tk.VERTICAL, length=100)
        self.volslider.pack(side=Tk.LEFT)
        ctrlpanel.pack(side=Tk.BOTTOM)

        # ctrlpanel2 = ttk.Frame(self.parent)
        # self.scale_var = Tk.DoubleVar()
        # self.timeslider_last_val = ""
        # self.timeslider = Tk.Scale(ctrlpanel2, variable=self.scale_var, command=self.scale_sel, 
        #         from_=0, to=1000, orient=Tk.HORIZONTAL, length=500)
        # self.timeslider.pack(side=Tk.BOTTOM, fill=Tk.X,expand=1)
        # self.timeslider_last_update = time.time()
        # ctrlpanel2.pack(side=Tk.BOTTOM,fill=Tk.X)


        # VLC player controls
        self.Instance = vlc.Instance()
        self.player = self.Instance.media_player_new()


    def OnExit(self, evt):
        """Closes the window.
        """
        self.Close()

    def OnOpen(self):
        """Pop up a new dialow window to choose a file, then play the selected file.
        """
        # if a file is already running, then stop it.
        self.OnStop()

        # Create a file dialog opened in the current home directory, where
        # you can display all kind of files, having as title "Choose a file".
        p = pathlib.Path(os.path.expanduser("~"))
        fullname =  askopenfilename(initialdir = p, title = "choose your file",filetypes = (("all files","*.*"),("mp4 files","*.mp4")))
        if os.path.isfile(fullname):
            print (fullname)
            splt = os.path.split(fullname)
            dirname  = os.path.dirname(fullname)
            filename = os.path.basename(fullname)
            # Creation
            self.Media = self.Instance.media_new(str(os.path.join(dirname, filename)))
            self.player.set_media(self.Media)
            # Report the title of the file chosen
            #title = self.player.get_title()
            #  if an error was encountred while retriving the title, then use
            #  filename
            #if title == -1:
            #    title = filename
            #self.SetTitle("%s - tkVLCplayer" % title)

            # set the window id where to render VLC's video output
            if platform.system() == 'Windows':
                self.player.set_hwnd(self.GetHandle())
            else:
                self.player.set_xwindow(self.GetHandle()) # this line messes up windows
            # FIXME: this should be made cross-platform
            self.OnPlay()

            # set the volume slider to the current volume
            #self.volslider.SetValue(self.player.audio_get_volume() / 2)
            self.volslider.set(self.player.audio_get_volume())

    def OnPlay(self):
        """Toggle the status to Play/Pause.
        If no file is loaded, open the dialog window.
        """
        # check if there is a file to play, otherwise open a
        # Tk.FileDialog to select a file
        if not self.player.get_media():
            self.OnOpen()
        else:
            # Try to launch the media, if this fails display an error message
            if self.player.play() == -1:
                self.errorDialog("Unable to play.")

    def GetHandle(self):
        return self.videopanel.winfo_id()

    #def OnPause(self, evt):
    def OnPause(self):
        """Pause the player.
        """
        self.player.pause()

    def OnStop(self):
        """Stop the player.
        """
        self.player.stop()
        

    def scale_sel(self, evt):
        if self.player == None:
            return
        nval = self.scale_var.get()
        sval = str(nval)
        if self.timeslider_last_val != sval:
            self.timeslider_last_update = time.time()
            mval = "%.0f" % (nval * 1000)
            self.player.set_time(int(mval)) # expects milliseconds


    def volume_sel(self, evt):
        if self.player == None:
            return
        volume = self.volume_var.get()
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")



    def OnToggleVolume(self, evt):
        """Mute/Unmute according to the audio button.
        """
        is_mute = self.player.audio_get_mute()

        self.player.audio_set_mute(not is_mute)
        # update the volume slider;
        # since vlc volume range is in [0, 200],
        # and our volume slider has range [0, 100], just divide by 2.
        self.volume_var.set(self.player.audio_get_volume())

    def OnSetVolume(self):
        """Set the volume according to the volume sider.
        """
        volume = self.volume_var.get()
        print("volume= ", volume)
        #volume = self.volslider.get() * 2
        # vlc.MediaPlayer.audio_set_volume returns 0 if success, -1 otherwise
        if volume > 100:
            volume = 100
        if self.player.audio_set_volume(volume) == -1:
            self.errorDialog("Failed to set volume")

    def errorDialog(self, errormessage):
        """Display a simple error dialog.
        """
        edialog = Tk.tkMessageBox.showerror(self, 'Error', errormessage)

def Tk_get_root():
    if not hasattr(Tk_get_root, "root"): #(1)
        Tk_get_root.root= Tk.Tk()  #initialization call is inside the function
    return Tk_get_root.root
        
def _quit():
    root = Tk_get_root()
    root.quit()     # stops mainloop
    root.destroy()  # this is necessary on Windows to prevent
                    # Fatal Python Error: PyEval_RestoreThread: NULL tstate
    os._exit(1)

if __name__ == "__main__":
    # Create a Tk.App(), which handles the windowing system event loop
    root = Tk_get_root()
    icon = PhotoImage(file='icon.png')
    root.iconphoto(False,icon)
    root.protocol("WM_DELETE_WINDOW", _quit)

    player = Player(root, title="Video Player")
    # show the player window centred and run the application
    root.mainloop()