import socket
import json
import subprocess
import threading
import sys
import telepot
import time
import sys
from filelock import Timeout, FileLock
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

group_id=-1001143270084
num=0
array={}
id_command={}
threadLock = threading.Lock()
question=""

lock = FileLock("teacher.txt.lock")

TOKEN = '1025374826:AAGcMIi_DeOLT986CCSzHfc0nhjFThblRfo'
bot = telepot.Bot(TOKEN)
keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')]])

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if query_data=='a':
        list1=[]
        for elem in array:
            if array[elem]=="":
                list1.append([elem])
        print(list1)
        keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
        bot.sendMessage(group_id, 'Digitare il codice della domanda:',reply_markup=keyboard1)
        id_command[group_id]=1
    if query_data=='r':
        bot.sendMessage(group_id, 'Digitare il bug da segnalare al programmatore:')
        id_command[group_id]=2
    if query_data=='s':
        bot.sendMessage(group_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
    if query_data=='l':
        stringa=""
        for elem in array:
            if array[elem]=="":
                if stringa == "":
                    stringa=elem
                else:
                    stringa+=",\n"+elem
                print(stringa)
        if stringa !="":
            bot.sendMessage(group_id, stringa)
        else:
            bot.sendMessage(group_id, "Lista vuota")
    if query_data=='b':
        list1=[]
        for elem in array:
            if array[elem]=="":
                list1.append([elem])
        print(list1)
        keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
        bot.sendMessage(group_id, 'Digitare il codice della domanda:',reply_markup=keyboard1)
        id_command[group_id]=3
    if query_data=='bl':
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
            bot.sendMessage(group_id, "Lista vuota")

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
    if content_type == 'text' and chat_id == -1001143270084:
        print(msg)
        global question
        txt=msg['text'].lower()
        threadLock.acquire()
        if txt=="/start":
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        elif txt=="/answer":
            list1=[]
            for elem in array:
                if array[elem]=="":
                    list1.append([elem])
            print(list1)
            keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
            bot.sendMessage(group_id, 'Digitare il codice della domanda:',reply_markup=keyboard1)
            id_command[group_id]=1
        elif txt=="/ban":
            list1=[]
            for elem in array:
                if array[elem] == "":
                    list1.append([elem])
            print(list1)
            keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
            bot.sendMessage(group_id, 'Digitare il codice della domanda:',reply_markup=keyboard1)
            id_command[group_id]=3
        elif txt=="/report":
            bot.sendMessage(group_id, 'Digitare il bug da segnalare al programmatore:')
            id_command[group_id]=2
        elif txt == "/list":
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
                bot.sendMessage(chat_id, "Lista vuota")
        elif txt == "/ban_list":
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
                bot.sendMessage(group_id, "Lista vuota")
        elif chat_id in id_command:
            if id_command[chat_id]==1:
                if txt in array:
                    if array[txt]=="":
                        question=txt
                        bot.sendMessage(chat_id,"Digitare la risposta:")
                        id_command[chat_id]=4
                else:
                    bot.sendMessage(chat_id,"Error: Question not found")
            elif id_command[chat_id]==2:
                with lock:
                    with open('teacher.txt','a') as f:
                        f.write("@@@"+txt+"###")
                bot.sendMessage(chat_id, 'Bug segnalato')
                del id_command[chat_id]
            elif id_command[chat_id]==3:
                if txt in array:
                    bot.sendMessage(chat_id,"La domanda '"+txt+"' é stata bannata")
                    array[txt]="BANNED"
                    txt = txt.replace(":","@")
                    txt += ": BANNED"
                    conn.send(txt.encode())
                    del id_command[chat_id]
                else:
                    bot.sendMessage(chat_id,"Error: String not found")
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
        bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})
        while 1:
            time.sleep(10)
            
def ricevo() :
    while True:
        msg=conn.recv(4096)
        x=msg.decode()
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
        array[elem]=data[elem]["a"]

print("teacher: "+str(array))

print("Connected")
ricevo()
ShellThread.join()