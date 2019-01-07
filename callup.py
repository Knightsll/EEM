"""
Record audio from 4 mic array, and then search the keyword "snowboy".
After finding the keyword, Direction Of Arrival (DOA) is estimated.

The hardware is respeaker 4 mic array:
    https://www.seeedstudio.com/ReSpeaker-4-Mic-Array-for-Raspberry-Pi-p-2941.html
"""
import pyaudio
import wave
from baidu_speech_api import BaiduVoiceApi
import json
import signal
import sys
import os
from aip.speech import AipSpeech
from urllib2 import Request, urlopen, URLError, HTTPError
import time
from voice_engine.source import Source
from voice_engine.channel_picker import ChannelPicker
from voice_engine.kws import KWS
from voice_engine.doa_respeaker_4mic_array import DOA
from pixels import pixels

# some parameter for STT
RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 2

# Baidu's key for STT
APP_ID = '10783244'
API_KEY = 'GlQae1odOq3Y1w2wCpGBOI27'
SECRET_KEY = 'aeb8dc5f91cc18990a873edb294e6641'
aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)





def main():
    src = Source(rate=16000, channels=4, frames_size=320)
    ch1 = ChannelPicker(channels=4, pick=1)
    kws = KWS()
    doa = DOA(rate=16000)

    src.link(ch1)
    ch1.link(kws)
    src.link(doa)
    
    def record():
        src.stream.start_stream()
        print("* recording")
        frames = []
        for i in range(0, int(RESPEAKER_RATE / CHUNK * RECORD_SECONDS)):
            data = src.stream.read(CHUNK)
            frames.append(data)
        print("* done recording")
        src.stream.stop_stream()
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
                return("get nothing")
        else:
            print("get nothing")
            return("get nothing")


    def on_detected(keyword):
        position = doa.get_direction()
        pixels.wakeup(position)
        print('detected {} at direction {}'.format(keyword, position))
        print(record())

    kws.set_callback(on_detected)

    src.recursive_start()
    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            break

    src.recursive_stop()


if __name__ == '__main__':
    main()
