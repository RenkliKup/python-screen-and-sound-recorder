from tkinter import *
import pyautogui
import cv2
import time
import numpy as np
import threading
import sys
class RecorderPython():
    def __init__(self,window):
        self.end=False
        self.before_time=time.time()
        self.hold_down=False
        self.window=window

    def widget(self):
        frame1=Frame(self.window)
        frame1.pack()
        frame2=Frame(self.window)
        frame2.pack(side="bottom")
        self.playButton=Button(frame1,text="Play",command=lambda:self.thread())
        self.playButton.pack(side="left")
        stopButton=Button(frame1,text="Stop",command=lambda:self.thread1())
        stopButton.pack(side="left")
        self.time_label=Label(frame2,text="sc")
        self.time_label.pack()

    def stop(self):
        self.playButton.configure(state=ACTIVE)
        self.before_time=time.time()
        self.end=True
        self.hold_down=True
        

    def play(self):
        self.end=False
        self.playButton.configure(state=DISABLED)
        self.time_label.configure(text=int(time.time()-self.before_time))
        
        if self.hold_down==True:
            self.hold_down=False
            return 0
        self.time_label.after(1,lambda:self.play())
    
    def rec(self):
        writer=cv2.VideoWriter("selam.mp4", cv2.VideoWriter_fourcc(*"XVID"),10,pyautogui.size())
        while True:
            frame=np.array(pyautogui.screenshot())
            writer.write(frame)
            if cv2.waitKey(1)==ord("q") or self.hold_down==True:
                sys.exit()
                break
                
            self.time_label.configure(text=int(time.time()-self.before_time))
            print("Kaydediyor...")
        writer.release()
        cv2.destroyAllWindows()
        return 0

    def thread(self):
        t1 = threading.Thread(target=lambda:self.rec())
        t1.start()
        t2 = threading.Thread(target=lambda:self.play())
        t2.start()
    def thread1(self):
        t3=threading.Thread(target=lambda:self.stop())
        t3.start()
        print("durduruldu...")