#-*- coding: UTF-8 -*-
import snowboydecoder
import sys
reload(sys) 
sys.setdefaultencoding('utf-8')
import signal

interrupted = False

import pyaudio
import wave
from baidu_speech_api import BaiduVoiceApi
import json
import signal

import RPi.GPIO as GPIO
import os
from aip.speech import AipSpeech
from word import word_dispose
from urllib2 import Request, urlopen, URLError, HTTPError
import serial
import time
from word_dispose import word_dispose
import serial
from pixels import Pixels 
from pixels import Pixels, pixels
global pixels
from google_home_led_pattern import GoogleHomeLedPattern
pixels.pattern = GoogleHomeLedPattern(show=pixels.show)


ser = serial.Serial('/dev/ttyUSB0',9600)


"""
command
"""

def w():
    ser.write(b'3')
def a():
    ser.write(b'1')
def s():
    ser.write(b'0')    
def d():
    ser.write(b'2')
def t():
    ser.write(b'3')
def demo(string):
    if 'w' in string:
        w()
        os.system("play ./rev.mp3")
        
    elif 'a' in string:
        a()
        os.system("play ./rev.mp3")
        
    elif 's' in string:
        s()
        os.system("play ./rev.mp3")
        
    elif 'd' in string:
        d()
        os.system("play ./rev.mp3")
        
    elif 't' in string:
        t()
        os.system("play ./rev.mp3")
        
    else:
        pass

"""
speech to text
"""

def reg():

    RESPEAKER_RATE = 16000
    RESPEAKER_CHANNELS = 1
    RESPEAKER_WIDTH = 2
    CHUNK = 1024
    RECORD_SECONDS = 2
    #WAVE_OUTPUT_FILENAME = "output.wav"



    p = pyaudio.PyAudio()
    stream = p.open(
                rate=RESPEAKER_RATE,
                format=p.get_format_from_width(RESPEAKER_WIDTH),
                channels=RESPEAKER_CHANNELS,
                input=True,
                start=False,)

    APP_ID = '10783244'
    API_KEY = 'GlQae1odOq3Y1w2wCpGBOI27'
    SECRET_KEY = 'aeb8dc5f91cc18990a873edb294e6641'


    aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

    baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)



    def generator_list(list):
        for l in list:
            yield l

    def record():
        stream.start_stream()
        pixels.wakeup()
        print("* recording")
        frames = []
        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done recording")
        stream.stop_stream()
        print("start to send to baidu")
	pixels.off()
        # audio_data should be raw_data
        text = baidu.server_api(generator_list(frames))
        if text:
            try:
                text = json.loads(text)
                for t in text['result']:
                    print(t)
                    return(t)
            except KeyError: 
                return("get nothing")
        else:
            print("get nothing")
            return("get nothing")


    os.system("play dong.wav")
    outputtext = record()
    temp = word_dispose(outputtext).tran()
    print "Command!!!", temp
    demo(temp)
    print outputtext
    stream.close()
    p.terminate()
            






"""
operation after waking up
"""
def callback():
    global detector
    snowboydecoder.play_audio_file()
    detector.terminate()
    reg()
    wake_up()

"""
wake up
"""

def wake_up():
    global detector
    model = './q.pmdl'
    signal.signal(signal.SIGINT, signal_handler)
    detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)
    print('Listening... Press Ctrl+C to exit')
    detector.start(detected_callback=callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

    detector.terminate()




def signal_handler(signal, frame):
    global interrupted
    stream.stop_stream()
    stream.close()
    p.terminate()
    print 'catched interrupt signal!'
    sys.exit(0)
    interrupted = True


def interrupt_callback():
    global interrupted
    return interrupted

if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)

wake_up()

