from Tkinter import *
import ttk

p=Tk()

separator = PanedWindow(p,bd=0,bg="#202322",sashwidth=2)

separator.pack(fill=BOTH, expand=1)

_frame = Frame(p,bg="#383838")

t=ttk.Treeview(_frame)

t["columns"]=("first","second")
t.column("first",anchor="center" )
t.column("second")
t.heading("first",text="first column")
t.heading("second",text="second column")
t.insert("",0,"dir1",text="directory 1")
t.insert("dir1","end","dir 1",text="file 1 1",values=("file 1 A","file 1 B"))
id=t.insert("","end","dir2",text="directory 2")
t.insert("dir2","end",text="dir 2",values=("file 2 A","file 2 B"))
t.insert(id,"end",text="dir 3",values=("val 1 ","val 2"))
t.insert("",0,text="first line",values=("first line 1","first line 2"))
t.tag_configure("ttk",foreground="black")

ysb = ttk.Scrollbar(orient=VERTICAL, command= t.yview)
xsb = ttk.Scrollbar(orient=HORIZONTAL, command= t.xview)
t['yscroll'] = ysb.set
t['xscroll'] = xsb.set

ttk.Style().configure("Treeview", background="#383838",foreground="white")
p.configure(background='black')

t.grid(in_=_frame, row=0, column=0, sticky=NSEW)
ysb.grid(in_=_frame, row=0, column=1, sticky=NS)
xsb.grid(in_=_frame, row=1, column=0, sticky=EW)
_frame.rowconfigure(0, weight=1)
_frame.columnconfigure(0, weight=1)

separator.add(_frame)

w = Text(separator)
separator.add(w)

p.mainloop()