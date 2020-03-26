import socket
import json
import subprocess
import threading
import sys
import telepot
import time
import sys
from filelock import Timeout, FileLock
from functions import match, check_id, add_id, del_id
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
keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')],[InlineKeyboardButton(text="/sban", callback_data='sb')],[InlineKeyboardButton(text="/change", callback_data='c')]])

bot_name="group_oop_bot"

permitted_id=[-1001143270084,297895076]

def case1(chat_id,from_id,txt):
    global question
    markup = ReplyKeyboardRemove()
    if txt in array:
        if array[txt]!="BANNED":
            question=txt
            bot.sendMessage(chat_id,"Digitare la risposta:",reply_markup=markup)
            id_command=add_id(id_command,from_id,chat_id,4)
    else:
        bot.sendMessage(chat_id,"Error: Question not found",reply_markup=markup)

def case2(chat_id,from_id,txt):
    with lock:
        bug_array=[]
        with open('teacher.txt','r') as f:
            bug_array=json.load(f)
        bug_array.append(txt.replace("'","#").replace('"','$'))
        with open('teacher.txt','w') as f:
            f.write(str(bug_array).replace("'",'"'))
    bot.sendMessage(chat_id, 'Bug segnalato')
    id_command=del_id(id_command,from_id,chat_id)

def case3(chat_id,from_id,txt):
    markup = ReplyKeyboardRemove()
    if txt in array:
        bot.sendMessage(chat_id,"La domanda '"+txt+"' é stata bannata",reply_markup=markup)
        array[txt]="BANNED"
        txt = txt.replace(":","@")
        txt += ": BANNED"
        conn.send(txt.encode())
    else:
        bot.sendMessage(chat_id,"Error: String not found",reply_markup=markup)
    id_command=del_id(id_command,from_id,chat_id)

def case4(chat_id,from_id,txt):
    global question
    bot.sendMessage(chat_id,"La risposta a '"+question+"' é '"+txt+"'")
    array[question]=txt
    question = question.replace(":","@")
    txt = txt.replace(":","@")
    txt = question+": "+txt
    conn.send(txt.encode())
    id_command=del_id(id_command,from_id,chat_id)

def case5(chat_id,from_id,txt):
    markup = ReplyKeyboardRemove()
    if txt in array:
        bot.sendMessage(chat_id,"La domanda '"+txt+"' é stata sbannata",reply_markup=markup)
        array[txt]=""
        txt = txt.replace(":","@")
        txt += ": SBANNED"
        conn.send(txt.encode())
    else:
        bot.sendMessage(chat_id,"Error: String not found",reply_markup=markup)
    id_command=del_id(id_command,from_id,chat_id)

def answer(chat_id,from_id):
    list1=[]
    for elem in array:
        if array[elem]=="":
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    if list1 ==[] :
        bot.sendMessage(chat_id, StringLVT,reply_markup=keyboard1)
    else :
        bot.sendMessage(chat_id, StringSLT,reply_markup=keyboard1)
    id_command=add_id(id_command,from_id,chat_id,1)

def change(chat_id,from_id):
    list1=[]
    for elem in array:
        if array[elem]!="" and array[elem]!="BANNED":
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    if list1 ==[] :
        bot.sendMessage(chat_id, StringLVT,reply_markup=keyboard1)
    else :
        bot.sendMessage(chat_id, StringSLT,reply_markup=keyboard1)
    id_command=add_id(id_command,from_id,chat_id,1)

def ans_list(chat_id,from_id):
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

def sban(chat_id,from_id):
    list1=[]
    for elem in array:
        if array[elem]=='BANNED':
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    if list1 ==[] :
        bot.sendMessage(chat_id, StringLVT,reply_markup=keyboard1)
    else :
        bot.sendMessage(chat_id, StringSLT,reply_markup=keyboard1)
    id_command=add_id(id_command,from_id,chat_id,5)

def ban(chat_id,from_id):
    list1=[]
    for elem in array:
        if array[elem]=="":
            list1.append([elem])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    if list1 ==[] :
        bot.sendMessage(chat_id, StringLVT,reply_markup=keyboard1)
    else :
        bot.sendMessage(chat_id, StringSLT,reply_markup=keyboard1)
    id_command=add_id(id_command,from_id,chat_id,3)

def ban_list(chat_id,from_id):
    stringa=""
    for elem in array:
        if array[elem] == 'BANNED':
            if stringa == "":
                stringa=elem
            else:
                stringa+=",\n"+elem
            print(stringa)
    if stringa !="":
        bot.sendMessage(chat_id, stringa)
    else:
        bot.sendMessage(chat_id, StringLVT)

def switch_case(chat_id,from_id,txt):
    if check_id(id_command,from_id,chat_id)==1:
        case1(chat_id,from_id,txt)
    elif check_id(id_command,from_id,chat_id)==2:
        case2(chat_id,from_id,txt)
    elif check_id(id_command,from_id,chat_id)==3:
        case3(chat_id,from_id,txt)
    elif check_id(id_command,from_id,chat_id)==4:
        case4(chat_id,from_id,txt)
    elif check_id(id_command,from_id,chat_id)==5:
        case5(chat_id,from_id,txt)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    chat_id=msg["message"]["chat"]["id"]
    if chat_id in permitted_id:
        if query_data=='a':
            answer(chat_id,from_id)
        elif query_data=='r':
            bot.sendMessage(chat_id, 'Digitare il bug da segnalare al programmatore:')
            id_command=add_id(id_command,from_id,chat_id,2)
        elif query_data=='s':
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        elif query_data=='l':
            ans_list(chat_id,from_id)
        elif query_data=='b':
            ban(chat_id,from_id)
        elif query_data=='bl':
            ban_list(chat_id,from_id)
        elif query_data=='sb':
            sban(chat_id,from_id)
        elif query_data=='c':
            change(chat_id,from_id)
    else:
        bot.sendMessage(chat_id,"Permesso negato")
        

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
    global id_command
    from_id=msg["from"]["id"]
    print(msg)
    if content_type == 'text':
        global question
        txt=msg['text'].lower()
        threadLock.acquire()
        if match(txt,'/start',chat_type,bot_name,chat_id,permitted_id,True,bot):
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        elif match(txt,'/answer',chat_type,bot_name,chat_id,permitted_id,True,bot):
            answer(chat_id,from_id)
        elif match(txt,'/ban',chat_type,bot_name,chat_id,permitted_id,True,bot):
            ban(chat_id,from_id)
        elif match(txt,'/report',chat_type,bot_name,chat_id,permitted_id,True,bot):
            bot.sendMessage(group_id, 'Digitare il bug da segnalare al programmatore:')
            id_command=add_id(id_command,from_id,chat_id,2)
        elif match(txt,'/list',chat_type,bot_name,chat_id,permitted_id,True,bot):
            ans_list(chat_id,from_id)
        elif match(txt,'/ban_list',chat_type,bot_name,chat_id,permitted_id,True,bot):
            ban_list(chat_id,from_id)
        elif match(txt,'/sban',chat_type,bot_name,chat_id,permitted_id,True,bot):
            sban(chat_id,from_id)
        elif match(txt,'/change',chat_type,bot_name,chat_id,permitted_id,True,bot):
            change(chat_id,from_id)
        elif check_id(id_command,from_id,chat_id) != 0:
            switch_case(chat_id,from_id,txt)
        threadLock.release()


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
            bot.sendMessage(-1001143270084,"Revisione richiesta per "+msg.decode())
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