
from tkinter import *


top = Tk()


# top.geometry('300x100')
top.resizable(0, 0)

l1 = Label(text="输入关键词")

l1.grid(row=0, column=0, rowspan=1, columnspan=1)

input = Entry()
input.grid(row=0, column=1, rowspan=1, columnspan=1)


btn_confirm = Button(text="confirm")

btn_confirm.grid(row=1, column=0, rowspan=1, columnspan=2, sticky=E+W)



top.mainloop()

