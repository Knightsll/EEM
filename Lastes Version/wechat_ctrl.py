#coding: utf-8

import itchat
from word_dispose import word_dispose
global top_1,top_2,num,my_id
import os
import serial
ser = serial.Serial('/dev/ttyUSB0',9600)


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
        print("No this command!!!")
        os.system("play ./no.mp3")




@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    temp = msg[r'Text']
    a = word_dispose(temp).tran()
    img = './wechat.jpeg'
    if u'照' in temp:
        itchat.send_msg("get it, plz be see the picture!",toUserName='filehelper')
        itchat.send_image(img,toUserName='filehelper')
        os.system("play ./rev.mp3")
    else:
        print ("Command!!!", a)
        demo(a)
        itchat.send_msg("get it, plz be sure the command correct!",toUserName='filehelper')

    print(a)

itchat.auto_login()
itchat.run()


