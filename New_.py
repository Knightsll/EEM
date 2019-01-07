import os
import time
from voice_engine.kws import KWS
from voice_engine.source import Source

src = Source()
kws = KWS()
src.link(kws)

RESPEAKER_RATE = 16000
RESPEAKER_CHANNELS = 1
RESPEAKER_WIDTH = 2
CHUNK = 1024
RECORD_SECONDS = 2

APP_ID = '10783244'
API_KEY = 'GlQae1odOq3Y1w2wCpGBOI27'
SECRET_KEY = 'aeb8dc5f91cc18990a873edb294e6641'

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)
baidu = BaiduVoiceApi(appkey=API_KEY,secretkey=SECRET_KEY)

def generator_list(list):
    for l in list:
        yield l

def on_detected(keyword):
    print('found {}'.format(keyword))
    os.system('play turnon.mp3')
    
kws.on_detected = on_detected

kws.start()
src.start()
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
kws.stop()
src.stop()