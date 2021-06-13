from src.record import RecorderPython
from tkinter import *

window=Tk()
record=RecorderPython(window)
record.widget()
window.mainloop()