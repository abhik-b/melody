from tkinter import *
import os
from ttkthemes import themed_tk as tk

from tkinter import ttk
import time
import threading
import tkinter.messagebox
from pygame import mixer
from pygame.mixer import Sound
from tkinter import filedialog
from mutagen.mp3 import MP3


root = tk.ThemedTk()
root.get_themes()
root.set_theme("elegance")
root.configure(bg="#151515")
mixer.init()
root.geometry("500x300")
root.title("melody")
root.iconbitmap(r'melody/melody.ico')

leftframe = Frame(root,bg="#151515")
leftframe.pack(side=LEFT)
rightframe = Frame(root,bg="#151515")
rightframe.pack(side=RIGHT, padx=15)

menubar = Menu(root,bg="#151515")
root.config(menu=menubar)
submenu = Menu(menubar, tearoff=0)
paused = FALSE
lb1 = Listbox(root,border=0,relief=GROOVE,bg="#151515",fg="white")
lb1.pack()
playlist=[]


def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    addplaylist(filename_path)


def addplaylist(filename):
    filename = os.path.basename(filename)

    index = 0
    lb1.insert(index, filename)
    playlist.insert(index,filename_path)
    print(playlist)
    index += 1


menubar.add_cascade(label="File", menu=submenu)
submenu.add_command(label="Open", command=browse_file)
submenu.add_command(label="exit", command=root.destroy)


def about_us():
    tkinter.messagebox.showinfo("CREDITS", ''' Author: Abhik Bhattacharya 

 Description: Made with tkinter in python''')
def manual():
    newwin = Toplevel(root)
    newwin.iconbitmap(r'melody/melody.ico')
    play = Label(newwin,
    text="▶   -   play music/restart music")
    play.pack()
    pause=Label(newwin,
    text=" ⏸   -   pause music")
    pause.pack()
    stop=Label(newwin,
    text=" ⏹   -  stop music")
    stop.pack()
    speaker=Label(newwin,
    text=" speaker  -   mute/unmute")
    speaker.pack()
    add=Label(newwin,
    text="+Add -  add music(mp3 files only) to playlist")
    add.pack()
    dele=Label(newwin,
    text="-Del -  delete music file from playlist")
    dele.pack()





submenu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Help", menu=submenu)
submenu.add_command(label="Manual", command=manual)
submenu.add_command(label="About Me", command=about_us)




length = Label(leftframe, text="Total Length   --:--",bg="#151515",fg="white")
length.pack()
current = Label(leftframe, text="Current Time   --:--",bg="#151515",fg="white")
current.pack()
def delsong():
     
     selection=lb1.curselection()
     
     selection=int(selection[0])
     playlist.pop(selection)
     
     lb1.delete(selection)
    
     
    
     


beechframe = Frame(root)
beechframe.pack(padx=5)
addbtn = Button(beechframe, text="+Add", command=browse_file,border=0,padx=4,bg="#151515",fg="white")
addbtn.grid(row=1, column=0)
delbtn = Button(beechframe, text="-Del",command=delsong,relief=GROOVE,border=0,bg="#151515",fg="white",padx=5)
delbtn.grid(row=1, column=1)


def show_details(play_it):
    mixer.init()
    a = MP3(play_it)
    total_length = a.info.length
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    length["text"] = "Total Length - "+timeformat
    t1 = threading.Thread(target=start_count, args=(total_length,))
    t1.start()


def start_count(t):
    global paused
    x = 0
    while x <= t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(x, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            current["text"] = "Current Time - "+timeformat
            time.sleep(1)
            x += 1


pausephoto = PhotoImage(file='melody/pause.png')

middleframe = Frame(rightframe,bg="#151515")
middleframe.pack()


def play_music():
    global paused
    global filename_path
    if paused:
        mixer.music.unpause()
        paused = FALSE
        statusbar["text"] = "Playing  " + os.path.basename(filename_path)
    else:
        try:
            stop_music()
            time.sleep(1)
            selection=lb1.curselection()
            selection=int(selection[0])
            play_it=playlist[selection]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing  " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror(
                "error", "haven't selected any files yet")

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"


def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music paused"


def mute_music():
    global muted
    if muted:

        mixer.music.set_volume(0.7)
        volbtn.configure(image=volphoto)
        scale.set(70)
        muted = FALSE
    else:
        muted = TRUE
        mixer.music.set_volume(0)
        volbtn.configure(image=mutephoto)
        scale.set(0)


playphoto = PhotoImage(file='melody/play.png')
playbtn = Button(middleframe, image=playphoto, command=play_music, border=0,bg="#151515")
playbtn.grid(row=0, column=0)
muted = FALSE

stopphoto = PhotoImage(file='melody/stop.png')
stopbtn = Button(middleframe, image=stopphoto, command=stop_music, border=0,bg="#151515")
stopbtn.grid(row=0, column=2,pady=10)

pausephoto = PhotoImage(file='melody/pause.png')
pausebtn = Button(middleframe, image=pausephoto, command=pause_music, border=0,bg="#151515")
pausebtn.grid(row=0, column=1, padx=5)

# rewindphoto = PhotoImage(file='melody/rewind.png')
# rewindbtn = Button(middleframe, image=rewindphoto,
#                    command=rewind_music, border=0)
# rewindbtn.grid(row=1, column=1)
mutephoto = PhotoImage(file='melody/mute.png')
volphoto = PhotoImage(file='melody/speaker.png')
volbtn = Button(middleframe, image=volphoto, command=mute_music,border=0,bg="#151515")
volbtn.grid(row=0, column=3,padx=5,pady=10)


def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)


scale = ttk.Scale(rightframe, from_=0, to_=100, orient=HORIZONTAL,
              command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.pack()

statusbar = Label(root, text="welcome to melody",  border=0,bg="#151515",fg="white",font='Times 10 italic')
statusbar.pack(side=BOTTOM, fill=X)


def on_closing():
    stop_music()
    root.destroy()


root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
