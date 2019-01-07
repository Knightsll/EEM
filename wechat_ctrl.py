#coding: utf-8

import itchat
from word_dispose import word_dispose
global top_1,top_2,num,my_id



@itchat.msg_register(itchat.content.TEXT)
def print_content(msg):
    temp = msg[r'Text']
    a = word_dispose(temp).ser_command()
    if a != "no command":
        itchat.send_msg("get it!",toUserName='filehelper')
    else:
        itchat.send_msg("no command!!!",toUserName='filehelper')
    print(a)

itchat.auto_login()
itchat.run()


