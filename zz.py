# -*- coding:utf-8 -*-
# PYTHON 3 ONLY

from tkinter import *
from tkinter import messagebox

root = Tk()
root.title('ROOT WINDOW')
Label(root,
      text='Place the toplevel window over the root window\nThen, push the button and you will see that the root window is again over the toplevel').grid()

topWindow = Toplevel(root)
topWindow.title('TOPLEVEL WINDOW')
Label(topWindow,
      text='This button will open a messagebox but will\ndo a "focus_force()" thing on the root window').grid()
Button(topWindow, text='[Push me !]', command=lambda: messagebox.showinfo('foo', 'bar!')).grid()

# --

root.mainloop()
