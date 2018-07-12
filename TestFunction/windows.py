from tkinter import *
from tkinter.ttk import *
import sys
win=Tk()
win.title("DCDetect")
count=0
def clickStart():
  global count
  count=count + 1
  statuslabel.config(text="Click Start " + carsize_entry.get() + " times")
def clickStop():
  statuslabel.config(text="Stop")
def clickExit():
  sys.exit(0)



statuslabel=Label(win, text="Hello World!")
carsize_label=Label(win, text="Car Size(Def:3000):")
carsize_entry=Entry(win)
carsize_entry.insert(END,'3000')
startbutton=Button(win, text="Start", command=clickStart)
stopbutton=Button(win, text="Stop", command=clickStop)
exitbutton=Button(win, text="Exit", command=clickExit)
statuslabel.grid(row = 0,column=1)
carsize_label.grid(row = 1 ,column=0)
carsize_entry.grid(row = 1 ,column=1)
startbutton.grid(row =2,column=0)
stopbutton.grid(row =2,column=1)
exitbutton.grid(row=2,column=2)
win.mainloop()