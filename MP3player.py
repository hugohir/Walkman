# Hugo Hiraoka MEDIA PLAYER
# This is an implementation of a Python MP3 player


import pygame
import time
import sys
import os
from tkinter import *
import tkinter.ttk as ttk
from PIL import ImageTk, Image
from tkinter import filedialog
import time
# from mutagen.mp3 import MP3
from mutagen.mp3 import *
import codecs
from mutagen.easyid3 import EasyID3
import pathlib

# from io import BytesIO

music = pathlib.Path('resources/music').absolute()
images = pathlib.Path('resources/images').absolute()
os.chdir(music)

walkman = Tk()


walkman.title("Hugo Media Player")
walkman.geometry("480x480+80+80")
walkman.resizable(False,False)
walkman.attributes('-alpha',1)
walkman.iconbitmap(images/'walkman_16px.ico')
pygame.mixer.init()

# main frame
walkman_player = Frame(walkman)
walkman_player.pack()

walkman_player.pack(pady=10)

# top frame
top_frame = Frame(walkman_player, background='red')
top_frame.grid(row=0, column=0)

# song playlist frame
#song_playlist_frame = Frame(top_frame, background='blue')
song_playlist_frame = Frame(walkman_player, background='blue')
#song_playlist_frame.grid(row=1, column=0)
song_playlist_frame.grid(row=0, column=0)

# artwork frame
#artwork_frame = Frame(top_frame)
artwork_frame = Frame(walkman_player,background='black')
#artwork_frame.grid(row=1, column=2)
artwork_frame.grid(row=0, column=4)

# volume frame
#volume_frame = LabelFrame(top_frame, text="volume")
volume_frame = LabelFrame(walkman_player, text="volume")
#volume_frame.grid(row=1, column=4)
volume_frame.grid(row=0, column=3)

# songinfo frame
songinfo_frame = Frame(walkman_player)
songinfo_frame.grid(row=2, column=0)

# slider frame
slider_frame = Frame(walkman_player)
slider_frame.grid(row=3, column=0)

# control frame
controls_frame = Frame(walkman_player)
controls_frame.grid(row=4, column=0)

# power frame
power_frame = Frame(walkman_player)
power_frame.grid(row=4, column=1)

# message frame
message_frame = Frame(walkman_player)
message_frame.grid(row=6, column=0)

# Listbox for song titles
song_playlist = Listbox(song_playlist_frame, bg="black", fg="blue", width=40, height=11, selectbackground="gray",
                        selectforeground="black")

song_playlist.grid(row=0, column=0, pady=0)

canvas_for_image = Canvas(walkman_player, bg='green', height=11, width=11, borderwidth=0, highlightthickness=0)
canvas_for_image.grid(row=0, column=1, sticky='nesw', padx=0, pady=0)

# create image from image location resize it to 240X240 and put in on canvas
image = Image.open(images/'albumcoversample.jpg')

canvas_for_image.image = ImageTk.PhotoImage(image.resize((120, 240), resample=Image.BICUBIC))
canvas_for_image.create_image(0, 0, image=canvas_for_image.image, anchor=NW)

# global variables
global paused
paused = False

global muted
muted = False


# function to loop the music, it unhighlights button when loop is off
def loopmusic():
    mymusic = song_playlist.get(ACTIVE)
    mymusic = f'{mymusic}.mp3'
    pygame.mixer.music.load(mymusic)
    pygame.mixer.music.play(loops=-1)
    repeaton_button = Button(controls_frame, image=img_repeaton_btn, borderwidth=0, command=unloopmusic)
    repeaton_button.grid(row=1, column=5, padx=5)
    mymusictime()


# function to unloop, it highlights button when loop is on
def unloopmusic():
    mymusic = song_playlist.get(ACTIVE)
    mymusic = f'{mymusic}.mp3'
    pygame.mixer.music.load(mymusic)
    pygame.mixer.music.play(loops=0)
    repeat_button = Button(controls_frame, image=img_repeat_btn, borderwidth=0, command=loopmusic)
    repeat_button.grid(row=1, column=6, padx=5)
    mymusictime()


# function mute, it highlights/unhighlights button when mute is on/off
def mute(is_muted):
    global muted
    muted = is_muted

    if muted:
        pygame.mixer.music.set_volume(0.0)
        muted = False
        muteon_button = Button(controls_frame, image=img_mute_btn, borderwidth=0, command=lambda: mute(muted))
        muteon_button.grid(row=1, column=3, padx=5)
    else:
        pygame.mixer.music.set_volume(0.5)
        muted = True
        mute_button = Button(controls_frame, image=img_muteon_btn, borderwidth=0, command=lambda: mute(muted))
        mute_button.grid(row=1, column=3, padx=5)


# function to add 1 song to playlist. Change directory accordingly.
def add_mymusic():
    #mymusic = filedialog.askopenfilename(initialdir='', title="Choose a song", filetypes=(("mp3 files", "*.mp3"),
    #                                                                                      ("mp4 files", "*.mp4"),
    #                                                                                     ("wav files", "*.wav"),))
    mymusic = filedialog.askopenfilename(initialdir=music, title="Choose a song", filetypes=(("mp3 files", "*.mp3"),("mp4 files", "*.mp4"),("wav files", "*.wav"),))
    mymusic = mymusic.replace("", "")
    mymusic = mymusic.replace(".mp3", "")
    song_playlist.insert(END, mymusic)


# function to add several songs
def add_manymymusic():
    mymusics = filedialog.askopenfilenames(initialdir='', title="Choose a song",
                                           filetypes=(("mp3 files", "*.mp3"),
                                                      ("mp4 files", "*.mp4"),
                                                      ("wav files", "*.wav"),))
    for mymusic in mymusics:
        mymusic = mymusic.replace("", "")
        mymusic = mymusic.replace(".mp3", "")
        song_playlist.insert(END, mymusic)


# function to clear the selected song only
def remove_mymusic():
    song_playlist.delete(ANCHOR)
    pygame.mixer.music.stop()


# function to clear the entire playlist
def remove_allmymusic():
    song_playlist.delete(0, END)
    pygame.mixer.music.stop()


# function to play the selected song
def play():
    mymusic = song_playlist.get(ACTIVE)
    mymusic = f'{mymusic}.mp3'
    pygame.mixer.music.load(mymusic)

    # getartwork(mymusic)

    pygame.mixer.music.play(loops=0)
    mymusictime()
    # positionslider = int(mymusic_lentime)
    # musicslider.config(to=positionslider, value=0)


##def getartwork(song):
#    track = MP3(song, ID3=EasyID3)

#    try:
#        album_art = track['pictures'][0]
#    except:
#        album_art = ""

#    if album_art =="":
#        try:
#           os.remove


# function to play the previous song
def prevmusic():
    prevmymusic = song_playlist.curselection()

    prevmymusic = prevmymusic[0] - 1

    mymusic = song_playlist.get(prevmymusic)
    mymusic = f'{mymusic}.mp3'
    pygame.mixer.music.load(mymusic)
    pygame.mixer.music.play(loops=0)

    song_playlist.selection_clear(0, END)
    song_playlist.activate(prevmymusic)

    song_playlist.selection_set(prevmymusic, last=None)


# function to play next song
def nextmusic():
    nextmymusic = song_playlist.curselection()

    nextmymusic = nextmymusic[0] + 1

    mymusic = song_playlist.get(nextmymusic)
    mymusic = f'{mymusic}.mp3'
    pygame.mixer.music.load(mymusic)
    pygame.mixer.music.play(loops=0)

    song_playlist.selection_clear(0, END)
    song_playlist.activate(nextmymusic)

    song_playlist.selection_set(nextmymusic, last=None)


# function to get and display the length of the song playing
def mymusictime():
    mymusic_curtime = pygame.mixer.music.get_pos() / 1000
    mymusic_curtimedisplay = time.strftime('%H:%M:%S', time.gmtime(mymusic_curtime))

    # mymusic_current = walkman.curselection()

    mymusic = song_playlist.get(ACTIVE)
    mymusic = f'{mymusic}.mp3'

    # total time of the song
    mymusic_mutagen = MP3(mymusic)

    global mymusic_lentime
    mymusic_lentime = mymusic_mutagen.info.length

    mymusic_lentimedisplay = time.strftime('%H:%M:%S', time.gmtime(mymusic_lentime))

    statusbar.config(text=f'{mymusic_curtimedisplay} |  {mymusic_lentimedisplay}')
    musicslider.config(value=mymusic_curtime)

    statusbar.after(1000, mymusictime)


# function to pause and unpause the song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
        pauseon_button = Button(controls_frame, image=img_pause_btn, borderwidth=0, command=lambda: pause(paused))
        pauseon_button.grid(row=0, column=3, padx=5)
    else:
        pygame.mixer.music.pause()
        paused = True
        pause_button = Button(controls_frame, image=img_pauseon_btn, borderwidth=0, command=lambda: pause(paused))
        pause_button.grid(row=0, column=3, padx=5)


# function to stop the song
def stop():
    pygame.mixer.music.stop()
    song_playlist.selection_clear(ACTIVE)

    # clear status
    statusbar.config(text="")


# function to fast forward the song
def fastforward():
    # get current music
    currentmusic = song_playlist.curselection()
    print(currentmusic)
    
    # get current position
    mymusic_curtime = pygame.mixer.music.get_pos() / 1000

    # mymusic_current = walkman.curselection()

    mymusic = song_playlist.get(ACTIVE)
    mymusic = f'/{mymusic}.mp3'

    # total time of the song
    mymusic_mutagen = MP3(mymusic)

    global mymusic_lentime
    mymusic_lentime = mymusic_mutagen.info.length

    print(mymusic_lentime)
    print(mymusic_curtime)

    if (mymusic_curtime >= mymusic_lentime):
        pygame.mixer.music.set_pos(mymusic_curtime - 200)
    else:
        pygame.mixer.music.set_pos(mymusic_curtime + 200)


# function to rewind the song
def rewind():
    pygame.mixer.music.rewind()


# function to display the song time slider
def slider(x):
    musicslider_label.config(text=f'{int(musicslider.get())} | {int(mymusic_lentime)}')


# function to display the volume slider
def volume(x):
    pygame.mixer.music.set_volume(volumeslider.get())
    curvolume = pygame.mixer


# function to quit the app, linked to the power button
def quit():
    sys.exit("Goodbye")


# function to menu bar option
def tellmeabout():
    pass


# defintion of controls
# newsize = (48,48);

img_poweron_btn = PhotoImage(file=images/'poweron48.png')
img_equalizer_btn = PhotoImage(file=images/'equalizer48.png')
img_volume_btn = PhotoImage(file=images/'volume48.png')
img_mute_btn = PhotoImage(file=images/'mute48.png')
img_muteon_btn = PhotoImage(file=images/'muteon48.png')
img_skipreverse_btn = PhotoImage(file=images/'skipreverse48.png')
img_reverse_btn = PhotoImage(file=images/'reverse48.png')
img_pause_btn = PhotoImage(file=images/'pause48.png')
img_pauseon_btn = PhotoImage(file=images/'pauseon48.png')
img_play_btn = PhotoImage(file=images/'play48.png')
img_stop_btn = PhotoImage(file=images/'stop48.png')
img_record_btn = PhotoImage(file=images/'record48.png')
img_forward_btn = PhotoImage(file=images/'forward48.png')
img_skipforward_btn = PhotoImage(file=images/'skipforward48.png')
img_repeat_btn = PhotoImage(file=images/'repeat48.png')
img_repeaton_btn = PhotoImage(file=images/'repeaton48.png')
img_shuffle_btn = PhotoImage(file=images/'shuffle48.png')

poweron_button = Button(power_frame, image=img_poweron_btn, borderwidth=0, command=quit)
equalizer_button = Button(controls_frame, image=img_equalizer_btn, borderwidth=0)
volume_button = Button(controls_frame, image=img_volume_btn, borderwidth=0)
mute_button = Button(controls_frame, image=img_mute_btn, borderwidth=0, command=lambda: mute(muted))
skipreverse_button = Button(controls_frame, image=img_skipreverse_btn, borderwidth=0, command=prevmusic)
reverse_button = Button(controls_frame, image=img_reverse_btn, borderwidth=0, command=rewind)
stop_button = Button(controls_frame, image=img_stop_btn, borderwidth=0, command=stop)
pause_button = Button(controls_frame, image=img_pause_btn, borderwidth=0, command=lambda: pause(paused))
pauseon_button = Button(controls_frame, image=img_pauseon_btn, borderwidth=0, command=lambda: pause(paused))
play_button = Button(controls_frame, image=img_play_btn, borderwidth=0, command=play)
record_button = Button(controls_frame, image=img_record_btn, borderwidth=0)
forward_button = Button(controls_frame, image=img_forward_btn, borderwidth=0, command=fastforward)
skipforward_button = Button(controls_frame, image=img_skipforward_btn, borderwidth=0, command=nextmusic)
shuffle_button = Button(controls_frame, image=img_shuffle_btn, borderwidth=0)
repeat_button = Button(controls_frame, image=img_repeat_btn, borderwidth=0, command=loopmusic)

skipreverse_button.grid(row=0, column=0, padx=5)
reverse_button.grid(row=0, column=1, padx=5)
stop_button.grid(row=0, column=2, padx=5)
pause_button.grid(row=0, column=3, padx=5)
play_button.grid(row=0, column=4, padx=5)
forward_button.grid(row=0, column=5, padx=5)
skipforward_button.grid(row=0, column=6, padx=5)
#poweron_button.grid(row=1, column=0, padx=5)
poweron_button.grid(row=0, column=0, padx=5)
equalizer_button.grid(row=1, column=1, padx=5)
volume_button.grid(row=1, column=2, padx=5)
mute_button.grid(row=1, column=3, padx=5)
record_button.grid(row=1, column=4, padx=5)
repeat_button.grid(row=1, column=5, padx=5)
shuffle_button.grid(row=1, column=6, padx=5)

playmenu = Menu(walkman)
walkman.config(menu=playmenu)

# menu
add_mymusic_menu = Menu(playmenu)
playmenu.add_cascade(label="Add Music", menu=add_mymusic_menu)
add_mymusic_menu.add_command(label="Add one song to Playlist", command=add_mymusic)
add_mymusic_menu.add_command(label="Add songs to Playlist", command=add_manymymusic)

remove_mymusic_menu = Menu(playmenu)
playmenu.add_cascade(label="Remove Music", menu=remove_mymusic_menu)
remove_mymusic_menu.add_command(label="Remove song from Playlist", command=remove_mymusic)
remove_mymusic_menu.add_command(label="Remove all songs from Playlist", command=remove_allmymusic)

about_mymusic_menu = Menu(playmenu)
playmenu.add_cascade(label="About", menu=about_mymusic_menu)
about_mymusic_menu.add_command(label="About", command=tellmeabout)
about_mymusic_menu.add_command(label="By Hugo Hiraoka (2020)", command=tellmeabout)

# music slider time label frame

musicslider = ttk.Scale(slider_frame, from_=0, to=100, orient=HORIZONTAL, value=0, length=400, command=slider)
musicslider.grid(row=2, column=0)

musicslider_label = Label(slider_frame, text="0")
musicslider_label.grid(row=3, column=0, ipady=20)

volumeslider = ttk.Scale(volume_frame, from_=0, to=1, orient=VERTICAL, value=1, length=142, command=volume)
volumeslider.pack(pady=10)

statusbar = Label(message_frame, text='', bd=1, relief=GROOVE, anchor=E)
statusbar.pack(fill=X, side=BOTTOM, pady=3)

walkman.mainloop()
