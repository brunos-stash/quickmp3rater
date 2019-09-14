from tkinter import Tk, Frame, Listbox, filedialog, Button, END
from tkinter import ttk
from pathlib import Path
import re
import vlc

from overlay import PlayerButtons
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
        self.bind('<Return>', func=self.play)
        self.bind('<Left>', func=self.prev)
        self.bind('<Right>', func=self.next)
        # self.bind('<Return>', func=self.play)
        self.current_mp3id = 3
        # self.selectpath()
    
    def selectpath(self):
        d = filedialog.askdirectory()
        self.searchpath = Path(d)
        self.search()
    
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
    
    def _mp3_as_uri(self):
        f = self.get(self.current_mp3id)
        fp = Path(f)
        self.current_mp3uri = fp.as_uri()
        print(fp)
        print(type(fp))
        print(self.current_mp3uri)

    def play(self, *event):
        mp3id = self.current_mp3id
        next_mp3 = self.next_mp3id
        print(mp3id, next_mp3)
        if mp3id != next_mp3:
            
        self._mp3_as_uri()
        uri = self.current_mp3uri
        self.mp3 = vlc.MediaPlayer(uri)
        if self.mp3.is_playing():
            self.mp3.stop()
        else:
            self.mp3.play()

    def next(self, *event):
        id = self.current_mp3id
        if self.mp3:
            self.mp3.stop()
        id += 1
        if id > (self.size()-1):
            self.next_mp3id = 0
        # self._mp3_as_uri()
        # uri = self.current_mp3uri
        # self.mp3 = vlc.MediaPlayer(uri)
        self.play()
    
    def prev(self, *event):
        if self.mp3:
            self.mp3.stop()
        self.current_mp3id -= 1
        if self.current_mp3id < 0:
            self.current_mp3id = self.size()-1
        self.play()


class FindBtn(Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack()



mf = MainFrame(master=app)
lb = FinderBox(master=mf,yscrollcommand=True)
b1 = Button(master=mf, text='select',command=lb.selectpath)
b1.pack()
app.mainloop()