from tkinter import *
from tkinter import messagebox


def displayText():
    """ Display the Entry text value. """

    global entryWidget

    if entryWidget.get().strip() == "":
        messagebox.showerror("Tkinter Entry Widget", "Enter a text value")
    else:
        messagebox.showinfo("Tkinter Entry Widget", "Text value =" + entryWidget.get().strip())


if __name__ == "__main__":
    root = Tk()

    root.title("Tkinter Entry Widget")
    root["padx"] = 40
    root["pady"] = 20

    button = Button(root, text="Submit", command=displayText)
    button.pack()

    canvas = Canvas(root, width=300, height=300)
    canvas.configure(background='#888888')
    canvas.pack(fill=BOTH, expand=1)
    canvas.create_rectangle(50, 25, 150, 75, fill="blue")
    entryWidget = Entry(canvas, width=150)
    canvas.create_window(10, 40, window=entryWidget, anchor=NW)
    #    w = Label(root, text="Red", bg="red", fg="white")
    ##    w.pack(fill=X)
    #   canvas.create_window(10, 40, window=entryWidget)
    #   w = Label(root, text="Green", bg="green", fg="black")
    #   w.pack(fill=X)
    #   w = Label(root, text="Blue", bg="blue", fg="white")
    #   w.pack(fill=X)

    # uncomment this line to demonstrate problem
    # entryWidget.pack(side=BOTTOM)
    entryWidget.focus_set()
    canvas.pack(fill=BOTH, expand=1)

    root.update()
    root.mainloop()
