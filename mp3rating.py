from tkinter import Tk, Frame, Listbox, filedialog, Button, END
from tkinter import ttk
from pathlib import Path
import re
import vlc

app = Tk()
app.geometry("300x300")
app.minsize(width=300,height=300)
app.title('Quick MP3 Rate')

class MainFrame(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(expand=True, fill='both')

class FinderBox(Listbox):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(expand=True, fill='both')
        # self.selectpath()
    
    def selectpath(self):
        d = filedialog.askdirectory()
        self.searchpath = Path(d)
    
    def search(self):
        results = self.searchpath.glob('*.mp3')
        for r in results:
            self.insert(END, r)
            self.update()
        results2 = self.searchpath.rglob('**/*.mp3')
        for r in results2:
            self.insert(END, r)
            self.yview(END)
            self.update()
    
    def play(self):
        f = self.get(0)
        fp = Path(f)
        furi = fp.as_uri()
        print(fp)
        print(type(fp))
        print(furi)
        try:
            self.mp3
        except:
            self.mp3 = vlc.MediaPlayer(furi)
        if self.mp3.is_playing():
            self.mp3.stop()
        else:
            self.mp3.play()

class FindBtn(Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack()

mf = MainFrame(master=app)
b1 = Button(master=mf)
lb = FinderBox(master=mf,yscrollcommand=True)
b1 = FindBtn(master=mf, text='Select path', command=lb.selectpath)
b2 = FindBtn(master=mf, text='Start search', command=lb.search)
b2 = FindBtn(master=mf, text='Play', command=lb.play)
# mf.pack(expand=True)
# lb.pack(expand=True)
app.mainloop()