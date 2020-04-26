
import tkinter as tk
from tkinter import ttk
import pygame
import time
import threading
import mutagen
from mutagen.mp3 import MP3
import wave
import matplotlib.pyplot as plt
FUNCTION = None
import os
pygame.mixer.pre_init(47200, -16, 2, 2048) # if missing, the play speed will be too slow
pygame.mixer.init()
# pygame.mixer.init(frequency=47200, size=-16, channels=2, buffer=4096)

mode = 'songlist' # single, playlist, songlist
md = {'songlist':[], 'playlist':[], 'folderlist':[]}
play_all = True

Player = None # this is the player class

playlist_dict = {}
playlist = []
folderlist = []

for r, d, f in os.walk('Songlist'):
    for song in f:
        md['songlist'].append('SongList/{}'.format(song))

class TrackTimer:
    def __init__(self):
        self._running = True
        self.timer = 0

    def terminate(self):
        self._running = False

    def run(self, n):
        while self._running == True:
            time.sleep(1)
            print(self.timer)
            self.timer += 1
            # print(pygame.mixer.music.get_pos())

        #
        # for song in args[1]:
        #     song = Mp3Button(self, args[1]key='', name='', dir='', holder='playlist')
        #
        #
        #
class SongsPage2(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, args[0])
        self.songlist = kwargs['list']
        self.target = args[1]
        self.name = kwargs['name']

        self.back_btn = tk.Button(self, text='Back', command=lambda:self.back())
        self.back_btn.pack(fill='y')

        self.canvas = tk.Canvas(self, width=500, height=550, bg='grey')
        self.scrolly = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrolly.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        self.canvas.pack(fill='both', side='top', expand='yes')
        self.scroll_frame = tk.Frame(self.canvas, width=500)
        self.scroll_frame.pack(fill='x', expand='yes')
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        key = 0
        for i in self.songlist:
            self.bt = Mp3Button(self.scroll_frame, name=song.split('.')[0], key=key, holder='songlist',
                                dir='SongList/{}'.format(song))
            key += 1

    def back(self):
        self.target.pack()



class PlaylistClass(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, args[0], padx=20, pady=8)
        self.pack(fill='x', pady=1)
        self.name = kwargs['playlistname']
        self.target = args[1]
        self.target2 = kwargs['target2']
        self.viewlist_btn = tk.Button(self, width=35, anchor='w', padx=10, bd=0, text=self.name, command=lambda:self.view())
        self.viewlist_btn.pack(side='left')

        self.play_btn = tk.Button(self, text='Play', bd=0)
        self.play_btn.pack(side='right')

    def view(self):
        self.target.pack_forget()




class PlayListPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args)

        self.list_of_playlist = ['playlist1', 'playlist2', 'playlist3', 'playlist4', 'playlist5','playlist6']

        self.fl = tk.Frame(self)
        self.fl.pack()
        self.canvas = tk.Canvas(self.fl, width=500, height=550, bg='grey')
        self.scrolly = tk.Scrollbar(self.fl, orient='vertical', command=self.canvas.yview)
        self.scrolly.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        self.canvas.pack(fill='both', side='top', expand='yes')
        self.scroll_frame = tk.Frame(self.canvas, width=500)
        self.scroll_frame.pack(fill='x', expand='yes')
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        for l in range(9):
            songs = []
            for s in range(5):
                songs.append('song')
            self.fm = SongsPage2(self, self.fl, name='name', list=songs)
            self.fm.pack()
            self.list_of_playlist.append(self.fm)

        for i in self.list_of_playlist:
            self.pl = PlaylistClass(self.scroll_frame, self.fl, target2=i, playlistname='name')



class Mp3Button(tk.Button):
    def __init__(self, *args, **kwargs):
        tk.Button.__init__(self, args[0], text=kwargs['name'], width=350, command=lambda:self.play(),
                           font=('Roboto', 9), bd=0, pady=8, padx=20, anchor='w')
        self.pack(fill='x', pady=1)
        self.holder = kwargs['holder']
        self.key = kwargs['key']
        self.name = kwargs['name']
        self.dir = kwargs['dir']

    def play(self):
        global mode, Player
        mode = 'songlist'
        Player.song_number = self.key
        Player.initialize()


class SongsPage(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, args[0])
        self.songlist = kwargs['list']
        self.canvas = tk.Canvas(self, width=500, height=550, bg='grey')
        self.scrolly = tk.Scrollbar(self, orient='vertical', command=self.canvas.yview)
        self.scrolly.pack(side='right', fill='y')
        self.canvas.configure(yscrollcommand=self.scrolly.set)
        self.canvas.pack(fill='both', side='top', expand='yes')
        self.scroll_frame = tk.Frame(self.canvas, width=500)
        self.scroll_frame.pack(fill='x', expand='yes')
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(
            scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        key = 0
        for i in self.songlist:
            self.bt = Mp3Button(self.scroll_frame, name=i.split('.')[0], key=key, holder='songlist',
                                dir='SongList/{}'.format(i))
            key += 1




class PlayerPage(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.pack()
        self.playing = 'stopped'
        self.current_song = ''
        self.canvas = tk.Canvas(self, width=350, height=250, bg='blue')
        self.canvas.pack()
        self.song_number = 0

        self.t0 = threading.Thread(target=self.run, args=(10,))

        self.current_song_label = tk.Label(self, text='...', font=('Roboto', 12, 'bold'), pady=30)
        self.current_song_label.pack()

        self.timer_frame = tk.Frame(self, width=100, bg='grey')
        self.timer_frame.pack(fill='y', side='top')

        self.track_timer = tk.Label(self.timer_frame, width=21, text='', anchor='w')
        self.track_timer.grid(row=0, column=0, sticky='nsew')
        self.track_length = tk.Label(self.timer_frame, width=20, text='', anchor='e')
        self.track_length.grid(row=0, column=1, sticky='nsew')

        self.slider = tk.Scale(self, width=5, length=300, command=self.slide_time, bg='blue', orient='horizontal', showvalue=0)
        self.slider.pack(fill='y')
        self.slider.bind("<ButtonRelease-1>", self.slide_event_release)
        self.slider.bind("<Button-1>", self.slide_event_pressed)

        self.control_frame = tk.Frame(self)
        self.control_frame.pack(pady=10)

        self.rewind_btn = tk.Button(self.control_frame, text='<< Prev', font=('Roboto', 11), command=lambda: self.rewind())
        self.rewind_btn.grid(row=0, column=0)

        self.play_btn = tk.Button(self.control_frame, text='Play', font=('Roboto', 11), command=lambda: self.play_pause())
        self.play_btn.grid(row=0, column=1)

        self.stop_btn = tk.Button(self.control_frame, text='stop', font=('Roboto', 11), command=lambda: self.stop())
        self.stop_btn.grid(row=0, column=2)

        self.forward_btn = tk.Button(self.control_frame, text='Next >>', font=('Roboto', 11), command= lambda: self.forward())
        self.forward_btn.grid(row=0, column=3)

    def extract_song_title(self, text):
        t = text.split('/')[-1].split('.')[0]
        return t

    def load_audio(self, audio):
        self.audio = MP3(audio)
        self.audio_info = self.audio.info
        self.length_in_secs = int(self.audio_info.length)
        self.slider.configure(from_=0, to=self.length_in_secs)
        lenght = self.get_time(self.length_in_secs)
        self.track_length.configure(text='{} : {}'.format(lenght[0], lenght[1]))
        self.current_song = audio
        self.current_song_label.configure(text=self.extract_song_title(self.current_song))
        pygame.mixer.music.load(audio)

    def get_time(self, sec):
        hours = sec // 3600
        sec %= 3600
        mins = sec // 60
        sec %= 60
        s = str(sec) if len(str(sec)) == 2 else '0' + str(sec)
        m = str(mins) if len(str(mins)) == 2 else '0' + str(mins)
        return [str(m), str(s)]

    def run(self, n):
        pos = self.slider.get()
        while self.playing == 'playing':
            time.sleep(1)
            self.slider.set(pos)
            track_time = self.get_time(self.slider.get())
            self.track_timer.configure(text='{} : {}'.format(track_time[0], track_time[1]))
            pos += 1
            if self.length_in_secs <= self.slider.get():
                self.playing = 'stopped'
                self.slider.set(0)
                self.track_timer.configure(text='00 : 00')
                if play_all:
                    self.initialize()
                break

    def initialize(self):
        global mode
        self.load_audio(md[mode][self.song_number])

        self.playing = 'playing'
        self.t0 = threading.Thread(target=self.run, args=(10,))
        self.t0.start()
        pygame.mixer.music.play(loops=0)
        if play_all and len(md[mode]) > self.song_number:
            self.song_number += 1
        else:
            mode = 'undefined'

    def play_pause(self):
        if self.playing == 'stopped':
            pygame.mixer.music.play(loops=0)
            self.playing = 'playing'
            self.t0 = threading.Thread(target=self.run, args=(10,))
            self.t0.start()
        elif self.playing == 'playing':
            pygame.mixer.music.pause()
            self.playing = 'paused'
        elif self.playing == 'paused':
            pygame.mixer.music.unpause()
            self.playing = 'playing'
            self.t0 = threading.Thread(target=self.run, args=(10,))
            self.t0.start()
        else:
            pass

    def stop(self):
        self.playing = 'stopped'
        pygame.mixer.music.stop()
        self.slider.set(0)

    def rewind(self):
        self.song_number -= 1
        self.initialize()

    def forward(self):
        self.initialize()

    def slide_event_release(self, event):
        self.load_audio(self.current_song)
        pygame.mixer.music.play(loops=0, start=self.slider.get())
        new_pos = self.slider.get()
        self.slider.set(new_pos)
        # pygame.mixer.music.set_pos(new_pos)
        # pygame.mixer.music.unpause()
        self.playing = 'playing'
        self.t0 = threading.Thread(target=self.run, args=(10,))
        self.t0.start()

    def slide_event_pressed(self, event):
        self.playing = "paused"
    def slide_time(self, event):
        t = self.get_time(self.slider.get())
        self.track_timer.configure(text='{} : {}'.format(t[0], t[1]))

class App(tk.Tk):
    def __init__(self, *args, **kwargs):
        global Player
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('350x550')

        self.ntbk = ttk.Notebook(self)
        self.ntbk.pack()

        self.player_page = PlayerPage(self.ntbk)
        self.ntbk.add(self.player_page, text=f'{"Player": ^20s}')

        Player = self.player_page

        self.list = []
        for r, d, f in os.walk('SongList'):
            for song in f:
                self.list.append(song)


        self.songs_page = SongsPage(self.ntbk, list=self.list)
        self.ntbk.add(self.songs_page, text=f'{"Songs": ^20s}')

        self.playlist_page = PlayListPage(self.ntbk, self.player_page)
        self.ntbk.add(self.playlist_page, text=f'{"Playlist": ^20s}')


if __name__ ==  '__main__':
    app = App()
    app.mainloop()
