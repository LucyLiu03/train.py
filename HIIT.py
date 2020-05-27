import time 

try: 
    import Tkinter as tk 
except ImportError: 
    import tkinter as tk
    from tkinter import *

from pygame import mixer 
import os

FONT_TIMER = ("Courier", 40)
FONT_BUTTON = ("System", 15, "bold")
FONT_START = ("System", 20, "bold")
FONT_LABEL = ("System", 15, "bold")

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

SOUND_FILE = '{d}/timer_trim.mp3'.format(d=PROJECT_DIR)
SOUND_VOLUME = '0.75'

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
        self.start_button.grid(row = 20, column = 1)
        self.reset_button = tk.Button(master, text="Reset", width = 5, bg ="#b8e8f2",font = FONT_BUTTON,command = self.reset)
        self.reset_button.grid(row = 30)
        self.close_button = tk.Button(master, text="Close", bg ="#b8e8f2", font = FONT_BUTTON,command = self.master.quit)
        self.close_button.grid(row = 30, column = 7)    

        #self.outputtext = None
        #self.caption = None
        self.close_button_start = None
        self.input_warning = tk.Label(self.master, font=FONT_LABEL, fg = "red",bg = "#ecfbff")
        self.input_warning.grid()

        mixer.init()
        mixer.music.load(SOUND_FILE)

        self.canvas = tk.Canvas(self.master, width=800, height=400, borderwidth=0, highlightthickness=0, bg="#ecfbff")

    def play_sound(self):
        os.system("play -q -v {vol} {fname} &".format(
            vol=SOUND_VOLUME, fname=SOUND_FILE
        ))

    def check_input(self, value):
        try:
            if value:
                v = int(value)
            return value
        except ValueError:
            return None

    def check_all_inputs(self):
        active_time = self.check_input(self.active_entry.get())
        rest_time = self.check_input(self.rest_entry.get())
        num_sets = self.check_input(self.num_sets_entry.get())
        num_circuits = self.check_input(self.num_circuits_entry.get())
        rest_circuits = self.check_input(self.rest_circuits_entry.get())
        
        if (active_time or rest_circuits or rest_time or num_circuits or num_sets) == '':
            #self.reset()
            self.input_warning.config(text = "check values")
        else: 
            self.start(int(active_time), int(rest_time), int(num_sets), int(num_circuits), int(rest_circuits))


    def start(self, active_time, rest_time, num_sets, num_circuits, rest_circuits):
        
        
        for widget in self.master.winfo_children():
           widget.grid_forget()

        #canvas = tk.Canvas(self.master, width=800, height=300, borderwidth=0, highlightthickness=0, bg="#ecfbff")
        #tk.Canvas.create_circle = self._create_circle(10,10,10)
        #canvas.create_oval(x-r, y-r, x+r, y+r,fill = "white", **kwargs)

        self.canvas.grid()

        y = 250
        x = 400
        r1 = 100
        r2 = 80

        self.canvas.create_oval(x-r1, y-r1, x+r1,y+r1,fill = "#dfbde3")
        self.canvas.create_oval(x-r2, y-r2, x+r2,y+r2,fill = "#ecfbff")

        self.close_button_start = tk.Button(self.master, text="End Session", font = FONT_BUTTON, bg ="#b8e8f2", command = self.master.quit)
        self.close_button_start.grid(row = 7)
        #self.outputtext = tk.Entry(self.master)
        #self.outputtext.grid(column = 21, row = 5)
        #self.outputtext.config(width = 10, font=FONT_TIMER, bg = "#ecfbff")

        #self.caption = tk.Entry(self.master)
        #self.caption.grid(row = 5)
        #self.caption.config(width = 20, font=FONT_TIMER, bg = "#ecfbff")

        self.circuit(int(active_time), int(rest_time), int(num_sets), int(num_circuits), int(rest_circuits))

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



    
    def circuit(self, active_time, rest_time, num_sets, num_circuits, rest_circuits):
        for i in range(num_circuits):
            for j in range(num_sets):
                self.countdown(active_time, "Keep moving for: ")
                self.countdown(rest_time, "Rest time: ")
            self.countdown(rest_circuits, "Rest time: ")


root = tk.Tk()


root.title("My GUI")
mainframe = Frame(root, bg = "#ecfbff")

mainframe.grid(column = 0, row = 0)

my_gui = testGUI(mainframe)
root.mainloop()