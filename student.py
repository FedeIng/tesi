import telepot
import json
import time
import socket
import sys
import spacy
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from random import seed
from random import random
from random import randrange
from datetime import datetime
import threading
from functions import match, check_id, add_id, del_id
from spacy.lang.it.examples import sentences 
from filelock import Timeout, FileLock
from gensim.models import Word2Vec

num=0
sim=0

nameFN="num.txt"
nameFD="data.txt"

lock = FileLock("student.txt.lock")
lockM = FileLock("mode.txt.lock")
lockN = FileLock(nameFN+".lock")

nlp = spacy.load('it_core_news_sm')

model = Word2Vec.load('wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m')

StringBNV='Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo'

keys = []
for idx in range(733392):
    keys.append(model.wv.index2word[idx])

# Set the vectors for our nlp object to the google news vectors
nlp.vocab.vectors = spacy.vocab.Vectors(data=model.wv.vectors, keys=keys)

print(nlp.vocab.vectors.shape)

keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/question", callback_data='q')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/revision", callback_data='rv')]])

id_command={}
array={}
ban_list=[]

bot_name="polito1_bot"

def get_user_banned():
    vect={}
    ban_list=[]
    for question in array:
        if array[question]["a"]=="BANNED":
            for elem in array[question]["id"]:
                if elem in vect:
                    vect[elem]+=1
                else :
                    vect[elem] = 1
    for elem in vect:
        if vect[elem] >= 10 :
            ban_list.append(elem)

    

def revision(chat_id,from_id):
    list1=[]
    for elem in array:
        if array[elem]!="" and array[elem]!="BANNED":
            list1.append([elem.replace("#","'").replace("$",'"')])
    print(list1)
    keyboard1 = ReplyKeyboardMarkup(keyboard=list1)
    if list1 ==[] :
        bot.sendMessage(chat_id, "Lista vuota",reply_markup=keyboard1)
    else :
        bot.sendMessage(chat_id,'Selezionare la domanda:',reply_markup=keyboard1)
    id_command=add_id(id_command,from_id,chat_id,3)

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    print(msg)
    chat_id=msg["message"]["chat"]["id"]
    if chat_id not in ban_list:
        if query_data=='q':
            bot.sendMessage(chat_id, 'Digitare la domanda da inviare al prof o agli assistenti del corso:')
            id_command=add_id(id_command,from_id,chat_id,1)
        elif query_data=='r':
            bot.sendMessage(chat_id, 'Digitare il bug da segnalare al programmatore:')
            id_command=add_id(id_command,from_id,chat_id,2)
        elif query_data=='s':
            bot.sendMessage(chat_id, StringBNV, reply_markup=keyboard)
        elif query_data=='rv':
            revision(chat_id,from_id)
    else :
        bot.sendMessage(chat_id,"Permesso negato")

def process_text(text):
    doc = nlp(text.lower())
    result = []
    for token in doc:
        if token.text in nlp.Defaults.stop_words:
            continue
        if token.is_punct:
            continue
        if token.lemma_ == '-PRON-':
            continue
        result.append(token.lemma_)
    return " ".join(result)

def calculate_similarity(text1, text2):
    base = nlp(process_text(text1))
    compare = nlp(process_text(text2))
    return base.similarity(compare)

seed(datetime.now())
threadLock = threading.Lock()

try:
    s=socket.socket()
    s.connect(("127.0.0.1",1500))
    print("Connected")
except socket.error as errore:
    print("Error:"+str(errore))
    sys.exit()

def answer_for(txt,y):
    for i in array:
        print(i)
        if y[0] == i:
            if y[1] =='SBANNED':
                 array[i]['a']=""
            else :
                array[i]['a']=y[1]

def answer(txt,y):
    print("La risposta "+y[0]+" é stata eliminata")
    if y[1] =='BANNED':
        for elem in array[y[0]]['id']:
            bot.sendMessage(elem, "La domanda '"+y[0].replace("#","'").replace("$",'"')+"' é stata bannata")
    elif y[1] =='SBANNED':
        for elem in array[y[0]]['id']:
            bot.sendMessage(elem, "La domanda '"+y[0].replace("#","'").replace("$",'"')+"' é stata sbannata")
    else :
        for elem in array[y[0]]['id']:
            bot.sendMessage(elem, "La risposta alla domanda '"+y[0].replace("#","'").replace("$",'"')+"' e' '"+y[1].replace("#","'").replace("$",'"')+"'")
    answer_for(txt,y)
    with open(nameFD,'w') as f:
        f.write(str(array).replace("'",'"'))

class OutputThread (threading.Thread):
    def __init__(self,s):
      threading.Thread.__init__(self)
      self.inp=s
    def run(self):
        while True:
            txt=self.inp.recv(4096)
            y=txt.decode()
            print(y)
            if y=="CHANGE MODE":
                print("Student2 bot ended")
                with lockN:
                    num="0"
                    with open(nameFN,'r') as f:
                        num=f.read()
                    num=int(num)+1
                    with open(nameFN,'w') as f:
                        f.write(str(num))
                exit()
            y=y.split(": ")
            print(y)
            threadLock.acquire()
            y[0] = y[0].replace("@",":").replace("'","#").replace('"',"$")
            y[1] = y[1].replace("@",":").replace("'","#").replace('"',"$")
            if y[0] in array:
                answer(txt,y) 
            else :
                print("Error: String not found")
            get_user_banned()
            threadLock.release()

def match_speech(chat_id,txt):
    global num
    global sim
    trovata=False
    for i in array:
        string1=process_text(txt)
        string2=process_text(i.replace("#","'").replace("$",'"'))
        num=calculate_similarity(string1,string2)
        if num>sim:
            sim=num
            val=i
        print(sim)
        if sim>0.8:
            trovata = True
            if array[val]['a'] == '':
                bot.sendMessage(chat_id, 'Domanda in attesa di risposta')
                if chat_id not in array[val]['id']:
                    array[val]['id'].append(str(chat_id))
                    with open(nameFD,'w') as f:
                        f.write(str(array).replace("'",'"'))
            elif array[val]['a']=='BANNED':
                bot.sendMessage(chat_id, 'La domanda da te fatta é stata bannata')
            else :
                bot.sendMessage(chat_id, array[val]['a'].replace("#","'").replace("$",'"'))
    return trovata

def seg_rev(chat_id,txt):
    markup = ReplyKeyboardRemove()
    bot.sendMessage(chat_id, 'Revisione richiesta per la domanda: '+txt,reply_markup=markup)
    msg=txt
    s.send(msg.encode())

def seg_bug(chat_id,txt):
    with lock:
        bug_array=[]
        with open('student.txt','r') as f:
            bug_array=json.load(f)
        bug_array.append(txt.replace("'","#").replace('"',"$"))
        with open('student.txt','w') as f:
            f.write(str(bug_array).replace("'",'"'))
    bot.sendMessage(chat_id, 'Bug segnalato')

def last_check(chat_id,txt,trovata,req_type):
    if  not trovata and req_type==1:
        txt1=txt.replace("'","#").replace('"',"$")
        array[txt1]={}
        array[txt1]['a']=""
        array[txt1]['id']=[]
        array[txt1]['id'].append(str(chat_id))
        with open(nameFD,'w') as f:
            f.write(str(array).replace("'",'"'))
        array[txt1]['a']=''
        bot.sendMessage(chat_id, 'Risposta non trovata. Domanda inviata al professore')
        msg=txt
        s.send(msg.encode())

def switch_case(chat_id,from_id,txt,req_type):
    global id_command
    if check_id(id_command,from_id,chat_id)==1 :
        return 1, match_speech(chat_id,txt)
    elif check_id(id_command,from_id,chat_id)==2 and req_type==0 :
        seg_bug(chat_id,txt)
        return 2, False
    elif check_id(id_command,from_id,chat_id)==3 and req_type==0 :
        seg_rev(chat_id,txt)
        return 3, False
    id_command=del_id(id_command,from_id,chat_id)

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global num
    global sim
    global id_command
    from_id=msg["from"]["id"]
    bot_array={}
    bot_array["bot"]=bot
    bot_array["name"]=bot_name
    print(msg)
    req_type=0
    sim=0
    num=0
    if content_type == 'text':
        threadLock.acquire()
        trovata = False
        txt=msg['text'].lower()
        if  match(txt,'/start',chat_type,chat_id,ban_list,False,bot_array) and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, StringBNV, reply_markup=keyboard)
        elif  match(txt,'/question',chat_type,chat_id,ban_list,False,bot_array) and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, 'Digitare la domanda da inviare al prof o agli assistenti del corso:')
            id_command=add_id(id_command,from_id,chat_id,1)
        elif  match(txt,'/report',chat_type,chat_id,ban_list,False,bot_array) and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, 'Digitare il bug da segnalare al programmatore:')
            id_command=add_id(id_command,from_id,chat_id,2)
        elif  match(txt,'/revision',chat_type,chat_id,ban_list,False,bot_array) and req_type==0 :
            revision(chat_id,from_id)
        elif check_id(id_command,from_id,chat_id) != 0:
            req_type, trovata=switch_case(chat_id,from_id,txt,req_type)
        else:
            req_type=4
            trovata = True
            bot.sendMessage(chat_id, 'Comando non trovato')
            bot.sendMessage(chat_id, StringBNV, reply_markup=keyboard)
        last_check(chat_id,txt,trovata,req_type)
        threadLock.release()

TOKEN = '1064330916:AAGjmjJZcEwyudWgPYplyP7OvyFQl4Ju_GI'
ShellThread=OutputThread(s)
ShellThread.start()
bot = telepot.Bot(TOKEN)

with open(nameFD,'r') as json_file:
    array=json.load(json_file)

bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

print('Listening ...')

mode_change="CHANGE MODE"

while 1:
    with lockM:
        with open('mode.txt','r') as f:
            mode=f.read()
            if mode=="man":
                s.send(mode_change.encode())
                print("Student1 bot ended")
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
    time.sleep(10)
