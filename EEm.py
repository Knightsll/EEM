#coding:utf-8
import cv2
import numpy as np
import pyaudio
import wave
from baidu_speech_api import BaiduVoiceApi
import json
import signal
import os
from aip.speech import AipSpeech
from urllib2 import Request, urlopen, URLError, HTTPError
import serial
import time
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')

#opencv_settings
face_cascade = cv2.CascadeClassifier(r'/home/pi/opencv-3.4.1/data/haarcascades/haarcascade_frontalface_default.xml')
#if you just have one camera it should be 0. if else, please seach for the camera which you want to use and change the port
cap=cv2.VideoCapture(0)
font = cv2.FONT_HERSHEY_SIMPLEX

#raspeaker_settings
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 2
#WAVE_OUTPUT_FILENAME = "output.wav"



#micphone_settings
p = pyaudio.PyAudio()
stream = p.open(
            rate=RESPEAKER_RATE,
            format=p.get_format_from_width(RESPEAKER_WIDTH),
            channels=RESPEAKER_CHANNELS,
            input=True,
            start=False,)

#baidu_speech_settings
APP_ID = '10783244'
API_KEY = 'GlQae1odOq3Y1w2wCpGBOI27'
SECRET_KEY = 'aeb8dc5f91cc18990a873edb294e6641'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)

def generator_list(list):
    for l in list:
        yield l
#  STT
def record():
    stream.start_stream()
    print("* recording")
    frames = []
    for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    time.sleep(1.8)    
    print("* done recording")
    stream.stop_stream()
    print("start to send to baidu")
    # audio_data should be raw_data
    text = baidu.server_api(generator_list(frames))
    if text:
        try:
            text = json.loads(text)
            for t in text['result']:
                print(t)
                return(t)
        except KeyError: 
            return("get Error")
    else:
        print("get nothing")
        return("get Error")

def sigint_handler(signum, frame):
    stream.stop_stream()
    stream.close()
    p.terminate()
    print 'catched interrupt signal!'
    sys.exit(0)

# 注册ctrl-c中断


def server():
    outputtext = record()
    print(outputtext)
    if (r'没'in outputtext) or ('no' in outputtext):
        os.system('play mp3/to_order.mp3')
    elif (r'ye'in outputtext) or (r'ok'in outputtext) or (r'是'in outputtext) or (r'对' in outputtext):
        os.system('play mp3/show.mp3')
    else:
        os.system('play mp3/say_something.mp3')
        server()
        
        



t = 0
a = 0
f = 0
while True:
    ok, img = cap.read()
    if t == 40:
        gray=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.35,
            minNeighbors=5,
            minSize=(6, 6),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
        a = 0
        t = 0
        #cv2.imwrite('init.jpg',img)
    else:
        t+=2
    try:
        for(x, y, w, h) in faces:
            cv2.circle(img, (np.int(((x+x+w)/2)), np.int((y+y+h)/2)), np.int(w/2), (255, 255, 255), 3)
            cv2.putText(img, 'HEY I FOUND YOU', (np.int(((x+x+w)/2)), np.int((y+y+h)/2+20)),font,1.2,(0,255,255),2)
        cv2.imshow("Face",img)
        cv2.waitKey(1)
        if len(faces)!=0 and a == 0:
            try:
                os.system('play mp3/welcome.mp3')
                time.sleep(0.5)
                os.system('play mp3/order.mp3')
                server()
                a=1
                f=1
                start_time = time.time()
            except KeyError: 
                stream.close()
                p.terminate()
        else:
            pass
    except:
        cv2.imshow("Face",img)
    end_time = time.time()
    if f==1:
        if (end_time-start_time)>5 :
            a=0
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    signal.signal(signal.SIGINT, sigint_handler)

