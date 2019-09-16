from tkinter import Button, Label, Frame, DoubleVar, StringVar
from tkinter.ttk import Progressbar

class Progress(Progressbar):
    def __init__(self, master=None, box=None, **kw):
        super().__init__(master=master, **kw)
        self.box = box
        self.time = DoubleVar(master=master, value=0)
        self.timestr = StringVar(master=master, value=0)
        self.pb = Progressbar(master=master, variable=self.time)
        # self.pb['value'] = self.time.get()
        # self.pb['maximum'] = self.length.get()
        self.label = Label(master=master, textvariable=self.timestr)
        self.label.pack()
        self.pb.pack()
        self.update()
    
    def update(self):
        time = self.box.mp3.get_time()/1000
        length = self.box.mp3.get_length()/1000
        timestr = f'{time:.2f} / {length:.2f}'
        self.time.set(time)
        self.timestr.set(timestr)
        # self.length.set(self.box.mp3.get_length())
        self.pb['maximum'] = length
        # print('update ',timestr)
        try:
            print(self.mp3)
        except:
            pass
        # self.length = self.box.mp3.get_length()
        self.after(100, func=self.update)

class PlayerControl(Frame):
    def __init__(self, master=None, box=None, **kw):
        # super().__init__(master=master, **kw)
        self.pb = Progress(master=master, box=box, **kw)