
from tkinter import *
import pyautogui
import subprocess
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
from collections import deque

class RecorderPython():
    def __init__(self,window):
        self.end=False
        self.buffersize=16
        self.que=deque(maxlen=self.buffersize)
        self.hold_down=False
        self.window=window

    def widget(self):
        frame1=Frame(self.window)
        frame1.pack()
        frame2=Frame(self.window)
        frame2.pack(side="bottom")
        self.playButton=Button(frame1,text="Play",command=lambda:self.thread())
        self.playButton.pack(side="left")
        self.var=IntVar()
        
        self.checkButton=Checkbutton(frame2,text="color detect",variable=self.var,onvalue=1)
        self.checkButton.pack(side="left")
        self.stopButton=Button(frame1,text="Stop",state=DISABLED,command=lambda:self.thread1())
        self.stopButton.pack(side="left")
        self.time_label=Label(frame2,text="süre:-")
        self.time_label.pack()
        
    def stop(self):
        self.playButton.configure(state=ACTIVE)
        self.stopButton.configure(state=DISABLED)
        self.before_time=time.time()
        self.end=True
        self.hold_down=True
    def play(self):
        self.end=False
        self.playButton.configure(state=DISABLED)
        self.stopButton.configure(state=ACTIVE)
        if self.hold_down==True:
            self.hold_down=False
            return 0
        self.time_label.after(1,lambda:self.play())

    def rec(self):
        screen=mss()
        monitor = {"top": 0, "left": 0, "width": 1920, "height": 1080}
        self.before_time=time.time()
        print(pyautogui.size())
        writer=cv2.VideoWriter("output.avi", cv2.VideoWriter_fourcc(*"DIVX"),13,pyautogui.size())
        
        while True:
            last_time=time.time()
            duration=math.ceil(int(time.time()-self.before_time))
            frame=screen.grab(monitor)
            frame=Image.frombytes("RGB",frame.size,frame.rgb)
            frame=cv2.cvtColor(np.array(frame),cv2.COLOR_BGR2RGB)
            frame=cv2.putText(frame,f"{int(1/(time.time()-last_time))}",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(255,0,0),1,cv2.LINE_AA)
            if self.var.get()==1:
                frame=self.detect(frame)
            
            writer.write(frame)
            if self.hold_down==True:
                break
            self.time_label.configure(text=str(f"süre:{duration}"))
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
                print("off")
                break
        stream.stop_stream()
        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        stream.close()
        p.terminate()

        
        
    def thread(self):
        threading.Thread(target=lambda:self.voice_record()).start()
        threading.Thread(target=lambda:self.rec()).start()
        threading.Thread(target=lambda:self.play()).start()
    def thread1(self):
        threading.Thread(target=lambda:self.stop()).start()

    def combine(self):
        
        
        audioclip = AudioFileClip("output.wav")
        #audioclip=audioclip.subclip(0,int(audioclip.duration))
        clip = VideoFileClip("output.avi")
        #clip = clip.subclip(0, int(clip.duration))
        
        file_exist=0
        while True:
            if os.path.exists(str(file_exist)+".avi")==0:
                durations1=round(int(audioclip.duration)/int(clip.duration),4)
                if int(clip.duration)>int(audioclip.duration):
                    
                    subprocess.call(f"ffmpeg -y -i output.avi -vf \"setpts={durations1}*PTS\" -r 24 {file_exist}.avi")
                    break
                else:

                    subprocess.call(f"ffmpeg -y -i output.avi -vf \"setpts={durations1}*PTS\" -r 24 {file_exist}.avi")
                    break
            else:
                file_exist=file_exist+1
        import ffmpeg

        video_stream = ffmpeg.input(f'{file_exist}.avi')
        audio_stream = ffmpeg.input('output.wav')
        ffmpeg.output(audio_stream, video_stream, str(time.strftime('%X').replace(':','.').replace("/",".").replace("\\", "."))+'.mp4').run()
        '''audioclip = AudioFileClip("output.wav")
        audioclip=audioclip.subclip(0,int(audioclip.duration))
        clip = VideoFileClip(f"{file_exist}.avi")
        clip = clip.subclip(0, int(clip.duration))
        videoclip = clip.set_audio(audioclip)
        videoclip.ipython_display(maxduration=250000)
        t=time.strftime('%X').replace(':','.').replace("/",".").replace("\\", ".")
        clip.close()
        videoclip.close()'''
        #print(os.getcwd())
        #os.rename("__temp__.mp4", f"{t}.mp4")
        #time_delay=abs(int(clip.duration-audioclip.duration))
        #print(time_delay)
        #document_name=f"{t}.mp4"
        #subprocess.call(f"ffmpeg -i {document_name} -itsoffset {time_delay} -i {document_name} -c:a copy -c:v copy -map 0:a:0 -map 1:v:0 delay.mp4")
        #subprocess.call("ffmpeg -i output.avi -filter:v fps=80 80fps.avi")
        
        #os.remove("output.avi")
        #os.remove("output.wav")
    def detect(self,frame):
        

        greenlow=(30,80,0)
        greenhigh=(100,255,255)
        mask=cv2.GaussianBlur(frame,(11,11),0)
        mask=cv2.cvtColor(mask,cv2.COLOR_BGR2HSV)
        blur=cv2.inRange(mask.copy(), greenlow, greenhigh)
        mask2=cv2.erode(blur,None,iterations=10)
        mask2=cv2.dilate(mask2,None,iterations=10)
        contour,_=cv2.findContours(mask2,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        if len(contour)>0:
            center=None
            c=max(contour,key=cv2.contourArea)
            rect=cv2.minAreaRect(c)
            (x,y),(width,height),rotate=rect
            s=f"x={x},y={y},width={width},height={height}"
            box=cv2.boxPoints(rect)
            box=np.int64(box)
            cv2.drawContours(frame,[box],0,(0,255,255),2)
            m=cv2.moments(c)
            center=(int(m["m10"]/m["m00"]),int(m["m01"]/m["m00"]))
            cv2.circle(frame,center,3,(0,255,255),-1)
            cv2.putText(frame,s,(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,255),3)
            self.que.appendleft(center)
            for i in range(1,len(self.que)):
                if self.que[i-1]==None or self.que[i]==None:continue
                cv2.line(frame,self.que[i-1],self.que[i],(0,255,255),3)
                
        return frame


            

