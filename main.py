from src.record import RecorderPython
from tkinter import *

window=Tk()
record=RecorderPython(window,20)
record.widget()
window.mainloop()