import time 

try: 
    import Tkinter as tk 
except ImportError: 
    import tkinter as tk
    from tkinter import *

from pygame import mixer 
import os
import csv
from random import seed, randint
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import spotipy.oauth2 as oauth2


CLIENT_ID = "c9ff2cb5f43c4ec9b0f1c29767ad5cba"
CLIENT_SECRET = "0e4e0d58aeb44e5a8d6e1fd458dd754b"
redirect_uri = "http://localhost:8888/callback/"

username = "myUsername"
#scope = "user-read-currently-playing"
#scope = "user-top-read"
scope = "user-modify-playback-state"

credentials = oauth2.SpotifyClientCredentials(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET)

token = util.prompt_for_user_token(username, scope, CLIENT_ID, CLIENT_SECRET, redirect_uri)
spotify = spotipy.Spotify(auth=token)

#print(spotify.current_user_playing_track())
#spotify.pause_playback(device_id=None)
spotify.start_playback(device_id=None, context_uri="spotify:playlist:6uL45FD5RZpw3sEBgev3lG", uris=None, offset=None, position_ms=None)

#print(spotify.current_user_top_tracks(limit=20, offset=0, time_range='short_term')["items"]["name"])



FONT_TIMER = ("Courier", 40)
FONT_BUTTON = ("System", 15, "bold")
FONT_START = ("System", 20, "bold")
FONT_LABEL = ("System", 15, "bold")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

SOUND_FILE = '{d}/timer_trim.mp3'.format(d=PROJECT_DIR)

EXERCISE_FILE = '{d}/exercises.csv'.format(d=PROJECT_DIR)

OPTION_LIST = ['How do you want to set up exercises?','Random Exercises!', 'Pick My Own!']

class testGUI: 
    def __init__(self, master):
        self.master = master 
        #master.title("A simple GUI")

        self.label = tk.Label(master, text="Your Workout!", font = FONT_START,
                            bg = "#b8e8f2", width = 35, height = 3 )
        self.label.grid(columnspan = 35)

        self.active_entry = self.question("Enter active time: ", 1)
        self.rest_entry = self.question("Enter rest time: ", 5)
        self.num_sets_entry = self.question("Enter number of sets in each circuit: ", 9)
        self.num_circuits_entry = self.question("Enter number of circuits: ", 13)
        self.rest_circuits_entry = self.question("Enter rest time inbetween circuits: ",17)

        self.start_button = tk.Button(master, text="Start", width = 5,bg ="#b8e8f2",font = FONT_START,command = self.check_all_inputs)
        self.start_button.grid(row = 30)
        self.reset_button = tk.Button(master, text="Reset", width = 5, bg ="#b8e8f2",font = FONT_BUTTON,command = self.reset)
        self.reset_button.grid(row = 35)
        self.close_button = tk.Button(master, text="Close", bg ="#b8e8f2", font = FONT_BUTTON,command = self.master.quit)
        self.close_button.grid(row = 35, column = 15)   
        self.ok_button = tk.Button(master, text = "ok", width = 5, bg ="#b8e8f2",font = FONT_BUTTON,command = self.ok) 
        self.ok_button.grid(row = 25, column = 10)
        
        self.close_button_start = None
        self.input_warning = tk.Label(self.master, font=FONT_LABEL, fg = "red",bg = "#ecfbff")
        self.input_warning.grid()

        mixer.init()
        mixer.music.load(SOUND_FILE)

        self.exercise_key = None
        self.exercise_data = {}

        self.new_moves = {}

        self.num_keys = None
        self.num_exercises = {}

        self.circuit_moves = []
        self.circuit_sections = []

        self.choose = False

        self.load_exercises()
        self.variable = tk.StringVar(self.master)
        
        self.drop_down_menu(OPTION_LIST, 25)

        self.ACTIVE_TIME = 0
        self.REST_TIME = 0
        self.NUM_SETS = 0
        self.NUM_CIRCUITS = 0
        self.REST_CIRCUITS = 0
        #self.variable.trace('w', self.callback())

        self.o_vars = []
        self.exer_input = []
        self.canvas = tk.Canvas(self.master, width=800, height=400, borderwidth=0, highlightthickness=0, bg="#ecfbff")

    def drop_down_menu(self,options, r):
        self.variable.set(options[0])
        opt = tk.OptionMenu(self.master, self.variable, *options)
        opt.config(width = 50, font = FONT_BUTTON, bg = "#ecfbff")
        opt.grid(row = r)

    def ok(self):
        print(self.variable.get())
        if (self.variable.get() == "Pick My Own!"):
            self.choose = True
        return self.variable.get()

    def load_exercises(self):
        reader = csv.DictReader(open("exercises.csv", encoding='utf-8-sig'))
        for row in reader:
            for column, value in row.items():
                if value!= None: 
                    self.exercise_data.setdefault(column, []).append(value)

        #print(self.exercise_data)   
        self.num_keys = len(self.exercise_data) + sum(len(v) for v in self.exercise_data.values() if isinstance(v, dict))
        #print(self.num_keys)

        for key, value in self.exercise_data.items():
            #print value
            num = len([item for item in value if item])
            self.num_exercises[str(key)] = num

        self.exercise_key = list(self.exercise_data.keys())
        print(self.num_exercises)         

    def check_input(self, value):
        try:
            if value:
                v = int(value)
            return value
        except ValueError:
            return None

    def check_all_inputs(self):
        self.ACTIVE_TIME = self.check_input(self.active_entry.get())
        self.REST_TIME = self.check_input(self.rest_entry.get())
        self.NUM_SETS = self.check_input(self.num_sets_entry.get())
        self.NUM_CIRCUITS = self.check_input(self.num_circuits_entry.get())
        self.REST_CIRCUITS = self.check_input(self.rest_circuits_entry.get())
        print(self.ACTIVE_TIME)
        
        if (self.ACTIVE_TIME or self.REST_CIRCUITS or self.REST_TIME or self.NUM_CIRCUITS or self.NUM_SETS) == '':
            #self.reset()
            self.input_warning.config(text = "check values")
        else: 
            self.info_page()

    def info_page(self):
        for widget in self.master.winfo_children():
           widget.grid_forget()

        print(self.choose)
        if (self.choose == False):
            self.canvas.grid()

            self.random_exercises()

            self.title_id = self.canvas.create_text(400, 50, font = FONT_LABEL, text = "Here's your generated workout!")

            #title = tk.Label(self.master, text="Here's your generated workout!", font=FONT_LABEL, bg = "#ecfbff")
            #title.grid(row = 1)

            for j in range(0,int(self.NUM_SETS)):
                self.title_id = self.canvas.create_text(400, 70 + (j*25), font = FONT_LABEL, text = self.circuit_moves[j])
                #exercise_label = tk.Label(self.master, text=str(self.exercise_data[self.circuit_sections[j]][self.circuit_moves[j]] ), font=FONT_LABEL, bg = "#ecfbff")
                #exercise_label.grid(row = j + 3)
        
        elif (self.choose == True):
            sections_options = list(self.exercise_data.keys())
            print(sections_options)

            for e in range(int(self.NUM_SETS)):
                var = tk.StringVar(self.master)
                var.set(value='- select -')
                #var = tk.StringVar(value="hi")
                self.o_vars.append(var)
                o = tk.OptionMenu(self.master, var, *sections_options)
                o.config(font = FONT_BUTTON, bg = "#ecfbff")
                o.grid(row = e*10)

                entry = tk.Entry(self.master, font = FONT_LABEL, bg = "#ffe8e8")
                entry.grid(row = e*10, column = 10)
                self.exer_input.append(entry)

                #self.drop_down_menu(sections_options, e*10)
                #self.ok_button = tk.Button(self.master, text = "ok", width = 5, bg ="#b8e8f2",font = FONT_BUTTON,command = self.ok) 
                #self.ok_button.grid(row = e*10, column = 10)
                #choosen_type = str(self.ok())
                #exer_options = list(self.exercise_data[str(choosen_type)])
                #self.drop_down_menu(choosen_type, e*15)

        self.start_wo_button = tk.Button(self.master, text="Start Workout!", width = 12, bg ="#b8e8f2",font = FONT_START, command = self.start_workout)
        self.start_wo_button.grid(row = 25)


        #self.start(int(active_time), int(rest_time), int(num_sets), int(num_circuits), int(rest_circuits))

    def start_workout(self):
        if (self.choose == True):
            for i in range(int(self.NUM_SETS)):
                #print(var.get())
                print(self.o_vars[i].get())
                print(self.exer_input[i].get())
                self.circuit_moves.append(self.exer_input[i].get())
                self.circuit_sections.append(self.o_vars[i].get())
            #print(self.circuit_moves)
            self.add_moves()
        self.start()

    def add_moves(self):
        for i in range(len(self.circuit_moves)):
            exist = (str(self.circuit_moves[i])) in self.exercise_data.values()
            if (exist == False):
                self.new_moves.setdefault(self.circuit_sections[i], []).append(self.circuit_moves[i])
        print(self.new_moves)
        self.update_csv()
                
    def start(self):
        
        self.canvas.delete("all")
        
        for widget in self.master.winfo_children():
           widget.grid_forget()

        #canvas = tk.Canvas(self.master, width=800, height=300, borderwidth=0, highlightthickness=0, bg="#ecfbff")
        #tk.Canvas.create_circle = self._create_circle(10,10,10)
        #canvas.create_oval(x-r, y-r, x+r, y+r,fill = "white", **kwargs)

        self.canvas.grid()

        y = 250
        x = 400
        r1 = 115
        r2 = 85

        self.canvas.create_oval(x-r1, y-r1, x+r1,y+r1,fill = "#dfbde3")
        self.canvas.create_oval(x-r2, y-r2, x+r2,y+r2,fill = "#ecfbff")

        self.close_button_start = tk.Button(self.master, text="End Session", font = FONT_BUTTON, bg ="#b8e8f2", command = root.destroy)
        self.close_button_start.grid(row = 7)
        #self.outputtext = tk.Entry(self.master)
        #self.outputtext.grid(column = 21, row = 5)
        #self.outputtext.config(width = 10, font=FONT_TIMER, bg = "#ecfbff")

        #self.caption = tk.Entry(self.master)
        #self.caption.grid(row = 5)
        #self.caption.config(width = 20, font=FONT_TIMER, bg = "#ecfbff")

        self.circuit()

    def reset(self):
        self.active_time = self.question("Enter active time: ", 1)
        self.rest_time = self.question("Enter rest time: ", 4)
        self.num_sets = self.question("Enter number of sets in each circuit: ", 7)
        self.num_circuits = self.question("Enter number of circuits: ", 10)
        self.rest_circuits = self.question("Enter rest time inbetween circuits: ",13)

    def question(self, question,rownum):
        question = tk.Label(self.master, text=str(question), font=FONT_LABEL, bg = "#ecfbff")
        question.grid(row = rownum)
        entry = tk.Entry(self.master, font = FONT_LABEL, bg = "#ffe8e8")
        entry.grid(row = rownum, column = 10)

        return entry

    def random_exercises(self):
        print(self.NUM_SETS)
        for e in range(int(self.NUM_SETS)):
            key = random.choice(list(self.exercise_data.keys()))
            n = int(self.num_exercises.get(str(key))) - 1
            exercise = randint(0, n)
            exercise_text = str(self.exercise_data[str(key)][exercise])
            self.circuit_moves.append(str(exercise_text))
            self.circuit_sections.append(str(key))

    def countdown(self, t, text):
        
        while t: 
            mins, secs = divmod(t, 60)
            timer = '{:02d}:{:02d}'.format(mins, secs)
            
            print(str(text) + timer, end="\r")
            #self.caption.insert(0,text)
            self.caption_id = self.canvas.create_text(400, 50, font = FONT_TIMER, text = text)
            #self.outputtext.insert(0,timer)
            self.timer_id = self.canvas.create_text(400, 250, font = FONT_TIMER, text = str(timer))
            if (t < 4):
                mixer.music.play()
            root.update()
            
            time.sleep(1)
            t -= 1
            #self.outputtext.delete(0, tk.END)
            #self.caption.delete(0,tk.END)
            self.canvas.delete(self.caption_id)
            self.canvas.delete(self.timer_id)


    def circuit(self):
        for i in range(int(self.NUM_CIRCUITS)):
            for j in range(0,int(self.NUM_SETS)):
                #self.countdown(active_time, str(self.exercise_data[str(key)][exercise] ))
                #self.countdown(int(self.ACTIVE_TIME), str(self.exercise_data[self.circuit_sections[j]][self.circuit_moves[j]] ))
                self.countdown(int(self.ACTIVE_TIME), str(self.circuit_moves[j]))
                if (j < int(self.NUM_SETS)-1):
                    print(j)
                    self.countdown(int(self.REST_TIME), "Rest time ")
                
            self.countdown(int(self.REST_CIRCUITS), "Rest time ")

    def update_csv(self):
        with open("exercises.csv", 'a') as file:
            writer = csv.writer(file, lineterminator = '\n')
            num = len(self.new_moves) + sum(len(v) for v in self.new_moves.values() if isinstance(v, dict))
            for k in range(num):
                for v in range(len(self.new_moves[str(self.circuit_sections[k])])):
                    value = self.new_moves[str(self.circuit_sections[k])][v]
                    val = []
                    for col in range(self.num_keys): 
                        if str(self.exercise_key[col]) == str(self.circuit_sections[k]):
                            val.append(value)
                        else:
                            val.append(None)
                    
                    writer.writerow(list(val))
        
        file.close()



root = tk.Tk()

root.title("My GUI")
mainframe = Frame(root, bg = "#ecfbff")

mainframe.grid(column = 0, row = 0)

my_gui = testGUI(mainframe)
root.mainloop()
