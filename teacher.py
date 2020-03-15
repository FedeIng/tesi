import socket
import json
import subprocess
import threading
import sys
import telepot
import time
import sys
from filelock import Timeout, FileLock
from functions import match
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

group_id=-1001143270084
num=0
array={}
id_command={}
threadLock = threading.Lock()
question=""
StringSLT='Selezionare la domanda:'
StringLVT="Lista vuota"
nameFN="num.txt"

lock = FileLock("teacher.txt.lock")
lockM = FileLock("mode.txt.lock")
lockN = FileLock(nameFN+".lock")

TOKEN = '1025374826:AAGcMIi_DeOLT986CCSzHfc0nhjFThblRfo'
bot = telepot.Bot(TOKEN)
keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')]])

bot_name="group_oop_bot"

def aboard():
    list1=[]
    for elem in array:
        if array[elem]=="":
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    bot.sendMessage(group_id, StringSLT,reply_markup=keyboard1)
    id_command[group_id]=1

def lboard():
    stringa=""
    for elem in array:
        if array[elem]=="":
            if stringa == "":
                stringa=elem
            else:
                stringa+=",\n"+elem
    if stringa !="":
        bot.sendMessage(group_id, stringa)
    else:
        bot.sendMessage(group_id, StringLVT)

def bboard():
    list1=[]
    for elem in array:
        if array[elem]=="":
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    bot.sendMessage(group_id, StringSLT,reply_markup=keyboard1)
    id_command[group_id]=3

def blboard():
    stringa=""
    for elem in array:
        if array[elem] == 'BANNED':
            if stringa == "":
                stringa=elem
            else:
                stringa+=",\n"+elem
            print(stringa)
    if stringa !="":
        bot.sendMessage(group_id, stringa)
    else:
        bot.sendMessage(group_id, StringLVT)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if query_data=='a':
        aboard()
    if query_data=='r':
        bot.sendMessage(group_id, 'Digitare il bug da segnalare al programmatore:')
        id_command[group_id]=2
    if query_data=='s':
        bot.sendMessage(group_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
    if query_data=='l':
        lboard()
    if query_data=='b':
        bboard()
    if query_data=='bl':
        blboard()
        

try:
    s=socket.socket()
    s.bind(("127.0.0.1",1500))
    s.listen(1)
except socket.error as errore:
    print("Error:"+str(errore))
    sys.exit()

conn,c_address=s.accept()
    

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(msg)
    if content_type == 'text' and chat_id == -1001143270084:
        global question
        txt=msg['text'].lower()
        threadLock.acquire()
        if match(txt,'/start',chat_type,bot_name):
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        elif match(txt,'/answer',chat_type,bot_name):
            list1=[]
            for elem in array:
                if array[elem]=="":
                    list1.append([elem])
            print(list1)
            keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
            bot.sendMessage(group_id, StringSLT,reply_markup=keyboard1)
            id_command[group_id]=1
        elif match(txt,'/ban',chat_type,bot_name):
            list1=[]
            for elem in array:
                if array[elem] == "":
                    list1.append([elem])
            print(list1)
            keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
            bot.sendMessage(group_id, StringSLT,reply_markup=keyboard1)
            id_command[group_id]=3
        elif match(txt,'/report',chat_type,bot_name):
            bot.sendMessage(group_id, 'Digitare il bug da segnalare al programmatore:')
            id_command[group_id]=2
        elif match(txt,'/list',chat_type,bot_name):
            stringa=""
            for elem in array:
                if array[elem]=="":
                    if stringa == "":
                        stringa=elem
                    else:
                        stringa+=",\n"+elem
            if stringa !="":
                bot.sendMessage(chat_id, stringa)
            else:
                bot.sendMessage(chat_id, StringLVT)
        elif match(txt,'/ban_list',chat_type,bot_name):
            stringa=""
            for elem in array:
                if array[elem] == 'BANNED':
                    if stringa == "":
                        stringa=elem
                    else:
                        stringa+=",\n"+elem
                    print(stringa)
            if stringa !="":
                bot.sendMessage(group_id, stringa)
            else:
                bot.sendMessage(group_id, StringLVT)
        elif chat_id in id_command:
            if id_command[chat_id]==1:
                markup = ReplyKeyboardRemove()
                if txt in array:
                    if array[txt]=="":
                        question=txt
                        bot.sendMessage(chat_id,"Digitare la risposta:",reply_markup=markup)
                        id_command[chat_id]=4
                else:
                    bot.sendMessage(chat_id,"Error: Question not found",reply_markup=markup)
            elif id_command[chat_id]==2:
                with lock:
                    bug_array=[]
                    with open('teacher.txt','r') as f:
                        bug_array=json.load(f)
                    bug_array.append(txt.replace("'","#").replace('"','$'))
                    with open('teacher.txt','w') as f:
                        f.write(str(bug_array).replace("'",'"'))
                bot.sendMessage(chat_id, 'Bug segnalato')
                del id_command[chat_id]
            elif id_command[chat_id]==3:
                markup = ReplyKeyboardRemove()
                if txt in array:
                    bot.sendMessage(chat_id,"La domanda '"+txt+"' é stata bannata",reply_markup=markup)
                    array[txt]="BANNED"
                    txt = txt.replace(":","@")
                    txt += ": BANNED"
                    conn.send(txt.encode())
                    del id_command[chat_id]
                else:
                    bot.sendMessage(chat_id,"Error: String not found",reply_markup=markup)
                    del id_command[chat_id]
            elif id_command[chat_id]==4:
                bot.sendMessage(chat_id,"La risposta a '"+question+"' é '"+txt+"'")
                array[question]=txt
                question = question.replace(":","@")
                txt = txt.replace(":","@")
                txt = question+": "+txt
                conn.send(txt.encode())
                del id_command[chat_id]
        threadLock.release()
    else :
        bot.sendMessage(chat_id,"Permesso negato")


class InputThread (threading.Thread):
    def __init__(self):
      threading.Thread.__init__(self)
    def run(self):
        mode_change="CHANGE MODE"
        bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})
        while 1:
            with lockM:
                with open('mode.txt','r') as f:
                    mode=f.read()
                    if mode=="man":
                        conn.send(mode_change.encode())
                        print("Teacher1 bot ended")
                        with lockN:
                            num="0"
                            with open(nameFN,'r') as f:
                                num=f.read()
                            num=int(num)+1
                            with open(nameFN,'w') as f:
                                f.write(str(num))
                        exit()
            time.sleep(10)
            
def ricevo() :
    while True:
        msg=conn.recv(4096)
        x=msg.decode()
        if x=="CHANGE MODE":
            print("Teacher2 bot ended")
            for id in id_command:
                bot.sendMessage(id, 'Il bot sta entrando in modalitá manutenzione, alcune funzioni potrebbero non essere abilitate')
            with lockN:
                num="0"
                with open(nameFN,'r') as f:
                    num=f.read()
                num=int(num)+1
                with open(nameFN,'w') as f:
                    f.write(str(num))
            exit()
        threadLock.acquire()
        if x in array:
            print("Error: String found")
        else :
            bot.sendMessage(-1001143270084, msg.decode())
            print("Il messaggio inviato è "+msg.decode())
            array[x]=""
        threadLock.release()

ShellThread=InputThread()
ShellThread.start()

with open('data.txt','r') as json_file:
    data=json.load(json_file)
    for elem in data:
        elem1=elem.replace("#","'").replace("$",'"')
        array[elem1]=data[elem]["a"].replace("#","'").replace("$",'"')

print("Connected")
ricevo()