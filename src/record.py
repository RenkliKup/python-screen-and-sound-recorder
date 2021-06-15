from tkinter import *
import pyautogui
import cv2
import time
import numpy as np
import threading
import sounddevice as sd
from scipy.io.wavfile import write
from moviepy.editor import *
import os
import time
import alsaaudio, wave, numpy
class RecorderPython():
    def __init__(self,window,duration):
        self.duration=duration
        self.end=False
        
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
        self.before_time=time.time()
        writer=cv2.VideoWriter("selam.mp4", cv2.VideoWriter_fourcc(*"XVID"),10,pyautogui.size())
        while True:
            duration=int(time.time()-self.before_time)
            frame=np.array(pyautogui.screenshot())
            frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            writer.write(frame)
            if cv2.waitKey(1)==ord("q") or self.hold_down==True:
                break
            
            self.time_label.configure(text=str(duration))
            if int(duration)==self.duration or int(duration)==self.duration:
                self.thread1()
                self.thread1()
                break
        
        writer.release()
        cv2.destroyAllWindows()
        
        self.combine()
        return 0
    def voice_record(self):
        
        sampleRate=44100
        voice=sd.rec(int(self.duration*sampleRate),channels=1,samplerate=sampleRate)
        sd.wait()
        
        '''
        inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE)
        inp.setchannels(1)
        inp.setrate(44100)
        inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)
        inp.setperiodsize(1024)

        w = wave.open('test.wav', 'w')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(44100)

        while True:
            l, data = inp.read()
            a = numpy.fromstring(data, dtype='int16')
            print numpy.abs(a).mean()
            w.writeframes(data)
            write("output.wav",sampleRate,voice)'''
    def thread(self):
        t3=threading.Thread(target=lambda:self.voice_record())
        t3.start()
        t1 = threading.Thread(target=lambda:self.rec())
        t1.start()
        t2 = threading.Thread(target=lambda:self.play())
        t2.start()
    
    def thread1(self):
        t3=threading.Thread(target=lambda:self.stop())
        t3.start()
        
    def combine(self):
        clip = VideoFileClip("selam.mp4")
        print(time.strftime("%x %X "))
        clip = clip.subclip(0, self.duration)
        audioclip = AudioFileClip("output.wav").subclip(0, self.duration)
        videoclip = clip.set_audio(audioclip)
        print(videoclip.filename)
        print(videoclip.ipython_display())
        t=time.strftime('%x %X').replace(':','.').replace("/",".").replace("\\", ".")
        os.rename("__temp__.mp4", f"{t}.mp4")