from tkinter import *

root = Tk()
c = Canvas(root, width=300, height=100)
c.pack()
r = c.create_rectangle(50, 50, 91, 67, outline='blue')
t = Label(c, text="Hello John, Michael, Eric, ...", anchor='w')
clip = c.create_window(51, 51, height=15, window=t, anchor='nw')


def update_clipping(new_width):
    x, y, w, h = c.coords(r)
    c.coords(r, x, y, x + int(new_width) + 1, h)
    t.itemconfig(clip, width=new_width)


s = Scale(root, from_=10, to=200, orient=HORIZONTAL, command=update_clipping)
s.pack()

root.mainloop()
