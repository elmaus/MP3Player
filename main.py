
import tkinter as tk
from tkinter import ttk
import pygame
import time
import threading
import mutagen
from mutagen.mp3 import MP3
import wave
import matplotlib.pyplot as plt

import os
pygame.mixer.pre_init(47200, -16, 2, 2048) # if missing, the play speed will be too slow
pygame.mixer.init()
# pygame.mixer.init(frequency=47200, size=-16, channels=2, buffer=4096)

mode = 'songlist' # single, playlist, songlist

song_list = ["SongList/I'll be Over You.mp3", 'SongList/still_the_one.mp3']

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


class Songs(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)


class Player(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)
        self.pack()
        self.playing = 'stopped'
        self.current_song = ''
        self.canvas = tk.Canvas(self, width=350, height=250, bg='blue')
        self.canvas.pack()
        self.song_number = 0

        self.t0 = threading.Thread(target=self.run, args=(10,))

        self.current_song_label = tk.Label(self, text='I Still Loving You', font=('Roboto', 12, 'bold'), pady=30)
        self.current_song_label.pack()

        self.timer_frame = tk.Frame(self, width=100, bg='grey')
        self.timer_frame.pack(fill='y', side='top')

        self.track_timer = tk.Label(self.timer_frame, width=21, text='00 : 00', anchor='w')
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

        # self.load_audio(self.current_song)
        # self.i = threading.Thread(target=self.initialize)
        # self.i.start()
        self.initialize()

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
                self.initialize()
                break

    def initialize(self):
        global mode
        if mode == 'songlist':
            try:
                self.load_audio(song_list[self.song_number])
                if self.song_number > 0:
                    self.playing = 'playing'
                    self.t0 = threading.Thread(target=self.run, args=(10,))
                    self.t0.start()
                    pygame.mixer.music.play(loops=0)
                try:
                    self.song_number += 1
                except:
                    mode = 'undefined'
            except:
                print('no other song')


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
        self.timer -= 3

    def forward(self):
        self.timer += 3

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
        tk.Tk.__init__(self, *args, **kwargs)
        self.geometry('350x550')

        self.ntbk = ttk.Notebook(self)
        self.ntbk.pack()

        self.player_page = Player(self.ntbk)
        self.ntbk.add(self.player_page, text=f'{"Player": ^20s}')

        self.songs_page = Player(self.ntbk)
        self.ntbk.add(self.songs_page, text=f'{"Songs": ^20s}')

        self.playlist_page = Player(self.ntbk)
        self.ntbk.add(self.playlist_page, text=f'{"Playlist": ^20s}')

if __name__ ==  '__main__':
    app = App()
    app.mainloop()

# self.songsframe = tk.LabelFrame(self, text="Song Playlist", font=("times new roman", 15, "bold"), bg="grey",
#                         fg="white", bd=5, relief='groove')
# self.songsframe.place(x=600, y=0, width=400, height=200)
# # Inserting scrollbar
# self.scrol_y = tk.Scrollbar(self.songsframe, orient='vertical')
# # Inserting Playlist listbox
# self.playlist = tk.Listbox(self.songsframe, yscrollcommand=self.scrol_y.set, selectbackground="gold", selectmode='single',
#                         font=("times new roman", 12, "bold"), bg="silver", fg="navyblue", bd=5, relief='groove')
# # Applying Scrollbar to listbox
# self.scrol_y.pack(side='right', fill='y')
# self.scrol_y.config(command=self.playlist.yview)
# self.playlist.pack(fill='both')
#
# for track in range(10):
#     self.playlist.insert('end', 'sam')
