from tkinter import *
import pyautogui
import cv2
import time
import numpy as np
import threading
from moviepy.editor import *
import os
import pyaudio
import wave
import math
from mss import mss
from PIL import Image
class RecorderPython():
    
    def __init__(self,window):
        
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
        if self.hold_down==True:
            self.hold_down=False
            return 0
        self.time_label.after(1,lambda:self.play())

    def rec(self):
        screen=mss()
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        self.before_time=time.time()
        writer=cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"DIVX"),16.6,pyautogui.size())
        li=[]
        while True:
            last_time=time.time()
            duration=math.ceil(int(time.time()-self.before_time))
            frame=screen.grab(monitor)
            frame=Image.frombytes("RGB",frame.size,frame.rgb)
            frame=cv2.cvtColor(np.array(frame),cv2.COLOR_BGR2RGB)
            frame=cv2.putText(frame,f"{int(1/(time.time()-last_time))}",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)
            li.append(int(1/(time.time()-last_time)))
            writer.write(frame)
            if self.hold_down==True:
                break
            self.time_label.configure(text=str(duration))
        writer.release()
        cv2.destroyAllWindows()
        self.combine()

    def voice_record(self):
        CHUNK = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        WAVE_OUTPUT_FILENAME = "output.wav"
        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,input_device_index=2)
        frames = []
        while True:  
            data = stream.read(CHUNK)
            frames.append(data)
            if cv2.waitKey(1)==ord("q") or self.hold_down==True:
                break
        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        
    def thread(self):
        threading.Thread(target=lambda:self.voice_record()).start()
        threading.Thread(target=lambda:self.rec()).start()
        threading.Thread(target=lambda:self.play()).start()
    def thread1(self):
        threading.Thread(target=lambda:self.stop()).start()

    def combine(self):
        audioclip = AudioFileClip("output.wav")
        audioclip=audioclip.subclip(0,int(audioclip.duration))
        clip = VideoFileClip("output.avi")
        clip = clip.subclip(0, int(clip.duration))
        
        videoclip = clip.set_audio(audioclip)
        videoclip.ipython_display(maxduration=2500)
        t=time.strftime('%x %X').replace(':','.').replace("/",".").replace("\\", ".")
        clip.close()
        videoclip.close()
        os.rename("__temp__.mp4", f"{t}.mp4")
        os.remove("output.avi")
        os.remove("output.wav")


