from tkinter import Tk, Frame, Listbox, filedialog, Button, END, Menu, IntVar
from tkinter.ttk import Progressbar
from pathlib import Path
import re
import vlc
from time import sleep

from overlay import PlayerControl


app = Tk()
app.geometry("300x300")
app.minsize(width=600,height=300)
app.title('Quick MP3 Rate')

class Entry:
    def __init__(self, file_id, file):
        self.id = str(file_id)
        self.file = file
        self.is_fav = False
        self._update_text()
    
    def _update_text(self):
        fav = 'X' if self.is_fav else ' '
        self.text = f'{int(self.id):<4d}| {fav} | {str(self.file)}'

    @property
    def favorite(self):
        return self.is_fav
    
    @favorite.setter
    def favorite(self, is_favorite):
        self.is_fav = is_favorite
        self._update_text()
    
class Mp3List:
    def __init__(self, iterable):
        for i, r in enumerate(iterable):
            e = Entry(i, r)
            self.__setattr__(e.i, e)
        
class MainFrame(Frame):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(expand=True, fill='both')

class FindBtn(Button):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack()

class FinderBox(Listbox):
    def __init__(self, master=None, **kw):
        super().__init__(master=master, **kw)
        self.pack(expand=True, fill='both')
        self.bind('<space>', func=self.play)
        self.bind('<Up>', func=self.prev)
        self.bind('<Down>', func=self.next)
        self.bind('<Right>', func=self.forward)
        self.bind('<Left>', func=self.backward)
        # self.bind('<Return>', func=self.play)
        self.current_mp3id = 0
        self.next_mp3id = 1
        self.mp3 = vlc.MediaPlayer()
        self.entries = None
        # self.selection = 0
        # self.activate(self.selection)
        # self.mp3 = vlc.MediaPlayer('file:///C:/Users/Bruno/Downloads/David%20Goggins/Cant%20Hurt%20Me/Cant%20Hurt%20Me%20-%20David%20Goggins.mp3')
        # self.mp3.start()
        # self.selectpath()
    
    def selectpath(self):
        d = filedialog.askdirectory()
        self.searchpath = Path(d)
        self.search()
    
    def search(self):
        results = self.searchpath.rglob('**/*.mp3')
        if not self.entries:
            self.entries = []
        for i, r in enumerate(results):
            entry = Entry(i, r)
            self.entries.append(entry)
            self.insert(END, entry.text)
            self.yview(END)
            self.update()
        self._mp3_as_uri()
        self.mp3 = vlc.MediaPlayer(self.current_mp3uri)
        # self.time = IntVar(master=self, value=self.mp3.get_time())

    def _mp3_as_uri(self):
        # f = self.get(self.current_mp3id)
        f = self.entries[self.current_mp3id].file
        fp = Path(f)
        self.current_mp3uri = fp.as_uri()
        print(fp)
        print(type(fp))
        print(self.current_mp3uri)

    def play(self, *event):
        print('selection: ',self.curselection())
        id = self.current_mp3id
        nid = self.next_mp3id
        # id, *_ = self.curselection()
        # nid, *_ = self.curselection()
        # self.activate(nid)
        print(id, nid)
        if id != nid:
            # self.activate(nid)
            self.mp3.stop()
            self.current_mp3id = nid
            # self.activate(nid)
            self._mp3_as_uri()
            uri = self.current_mp3uri
            self.mp3 = vlc.MediaPlayer(uri)
            self.mp3.play()
        else:
            if self.mp3.is_playing():
                self.mp3.pause()
            else:
                self.mp3.play()

    def next(self, *event):
        # id = self.current_mp3id
        id, *_ = self.curselection()
        nid = id + 1
        if nid > (self.size()-1):
            self.next_mp3id = 0
            # self.activate(0)
        else:
            self.next_mp3id = nid
            # self.activate(nid)
        # self._mp3_as_uri()
        # uri = self.current_mp3uri
        # self.mp3 = vlc.MediaPlayer(uri)
        self.play()
        # sleep(0.1)
    
    def prev(self, *event):
        # id = self.current_mp3id
        id, *_ = self.curselection()
        nid = id - 1
        if nid < 0:
            self.next_mp3id = (self.size()-1)
            # self.activate(self.next_mp3id)
        else:
            self.next_mp3id = nid
            # self.activate(nid)

        self.play()
        # sleep(0.1)

    def forward(self, *event):
        ct = self.mp3.get_time()
        length = self.mp3.get_length()
        nt = ct + 1000
        if nt > length:
            self.mp3.stop()
            return
        self.mp3.set_time(nt)
    
    def backward(self, *event):
        ct = self.mp3.get_time()
        length = self.mp3.get_length()
        nt = ct - 1000
        if nt < 0:
            nt = 0
        self.mp3.set_time(nt)

mf = MainFrame(master=app)
m1 = Menu(master=app)
app.config(menu=m1)
lb = FinderBox(master=mf,yscrollcommand=True)
m1.add_command(label='Search', command=lb.selectpath)
control = PlayerControl(master=mf, box=lb)
# b1 = FindBtn(master=mf, text='Search',command=lb.selectpath)
# b2 = FindBtn(master=mf, text='Search',command=lb.selectpath)
# b1.pack()
# b2.pack()
app.mainloop()