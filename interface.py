from tkinter import *
from tkinter import ttk

root = Tk()
frm = ttk.Frame(root, padding=200)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)

root.mainloop()