from tkinter import Button, Label, Frame


class PlayerButtons(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.btn_next = Button(master=master, text='Start search', command=master.next)
        self.btn_play = Button(master=master, text='Play', command=master.play)
        self.btn_prev = Button(master=master, text='Prev', command=master.prev)
        self.btn_play.pack()
        self.btn_next.pack()
        self.btn_prev.pack()