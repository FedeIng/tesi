import os
import sys
import telepot
import threading
import time
from multiprocessing import Process
from filelock import Timeout, FileLock

TOKEN = '1045575516:AAF8WKCOlQQbBX6d9ywkKUlyd2h_UvNnmYA'
bot = telepot.Bot(TOKEN)

lockS = FileLock("student.txt.lock")
lockT = FileLock("teacher.txt.lock")

def student():
    os.system("student.py")

def teacher():
    os.system("teacher.py")

def parse(name):
    with open(name,"r") as f:
        string = f.read()
        if string!="":
            array=string.split("###@@@")
            array[0]=array[0].replace("@@@","")
            array[len(array)-1]=array[len(array)-1].replace("###","")
            for line in array:
                bot.sendMessage(297895076, "Error "+ name.replace(".txt","") + " " + line)
    with open(name,"w") as f:
        f.write("")

class FileThread (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
        while 1:
            time.sleep(10)
            with lockS:
                with lockT:
                    parse('student.txt')
                    parse('teacher.txt')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text' and chat_id == 297895076:
        txt=msg['text'].lower()
        if txt.startswith('/read_'):
            txt = txt.replace("/read_", "")
            with open(txt+'.txt') as openfileobject:
                for line in openfileobject:
                    bot.sendMessage(chat_id, line)
        elif txt == '/reset':
            with open('id.txt','w') as f:
                f.write("{}")
            with open('data.txt','w') as f:
                f.write("{}")
            bot.sendMessage(chat_id, "Dati cancellati")
    else :
        bot.sendMessage(chat_id,"Permesso negato")
                    


if __name__=='__main__':
    t=Process(target=teacher,args=())
    s=Process(target=student,args=())
    t.start()
    s.start()
    bot.sendMessage(297895076, "Bot operativi")
    FileThread=FileThread()
    FileThread.start()
    bot.message_loop(on_chat_message)
    while 1:
        time.sleep(10)
    bot.sendMessage(297895076, "Bot operativi")
    t.join()
    s.join()