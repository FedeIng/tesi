import os
import subprocess
import sys
import json
import telepot
import threading
import time
from multiprocessing import Process
from filelock import Timeout, FileLock

TOKEN = '1045575516:AAF8WKCOlQQbBX6d9ywkKUlyd2h_UvNnmYA'
bot = telepot.Bot(TOKEN)

nameFM="mode.txt"
nameFN="num.txt"

lockS = FileLock("student.txt.lock")
lockT = FileLock("teacher.txt.lock")
lockM = FileLock(nameFM+".lock")
lockN = FileLock(nameFN+".lock")

def student():
    os.system("student.py")

def teacher():
    os.system("teacher.py")

def student1():
    os.system("student1.py")

def teacher1():
    os.system("teacher1.py")

t=Process(target=teacher,args=())
s=Process(target=student,args=())

mode="standard"

def parse(name):
    vector=[]
    with open(name,"r") as f:
        vector=json.load(f)
    if len(vector)>0:
        for line in vector:
            bot.sendMessage(297895076, "Error "+ name.replace(".txt","") + " " + line.replace("#","'").replace("$",'"'))
    with open(name,"w") as f:
        f.write("[]")

class FileThread (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
        while 1:
            time.sleep(10)
            with lockS:
                parse('student.txt')
            with lockT:
                parse('teacher.txt')

def on_chat_message(msg):
    global mode
    num_closed="0"
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
        elif txt=="/man_mode":
            if mode=="standard":
                mode="manutention"
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("man")
                while num_closed!="4":
                    time.sleep(10)
                    with lockN:
                        with open(nameFN,'r') as f:
                            num_closed=f.read()
                bot.sendMessage(chat_id, "Modalitá manutenzione attivata")
                t=Process(target=teacher1,args=())
                s=Process(target=student1,args=())
                t.start()
                s.start()
                with lockN:
                    with open(nameFN,'w') as f:
                        num_closed=f.write("0")
            else:
                bot.sendMessage(chat_id, "Error: Modalitá manutenzione giá attiva")
        elif txt=="/std_mode":
            if mode=="manutention":
                mode="standard"
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("std")
                while num_closed!="2":
                    time.sleep(10)
                    with lockN:
                        with open(nameFN,'r') as f:
                            num_closed=f.read()
                bot.sendMessage(chat_id, "Modalitá standard attivata")
                t=Process(target=teacher,args=())
                s=Process(target=student,args=())
                t.start()
                s.start()
                with lockN:
                    with open(nameFN,'w') as f:
                        num_closed=f.write("0")
            else:
                bot.sendMessage(chat_id, "Error: Modalitá standard giá attiva")
        elif txt=="/restart":
            if mode=="standard":
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("man")
                while num_closed!="4":
                    time.sleep(10)
                    with lockN:
                        with open(nameFN,'r') as f:
                            num_closed=f.read()
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("std")
                t=Process(target=teacher,args=())
                s=Process(target=student,args=())
                t.start()
                s.start()
                bot.sendMessage(chat_id, "Restart complete")
                with lockN:
                    with open(nameFN,'w') as f:
                        num_closed=f.write("0")
            elif mode=="manutention":
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("std")
                while num_closed!="2":
                    time.sleep(10)
                    with lockN:
                        with open(nameFN,'r') as f:
                            num_closed=f.read()
                with lockM:
                    with open(nameFM,'w') as f:
                        f.write("man")
                t=Process(target=teacher1,args=())
                s=Process(target=student1,args=())
                t.start()
                s.start()
                bot.sendMessage(chat_id, "Restart complete")
                with lockN:
                    with open(nameFN,'w') as f:
                        num_closed=f.write("0")
            else:
                print("Error: unknown mode")
    else :
        bot.sendMessage(chat_id,"Permesso negato")
                    


if __name__=='__main__':
    with lockM:
        with open(nameFM,'w') as f:
            f.write("std")
    with lockN:
        with open(nameFN,'w') as f:
            f.write("0")
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