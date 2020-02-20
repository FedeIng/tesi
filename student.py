import telepot
import json
import time
import socket
import sys
import spacy
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from random import seed
from random import random
from random import randrange
from datetime import datetime
import threading
from spacy.lang.it.examples import sentences 
from filelock import Timeout, FileLock
from gensim.models import Word2Vec

lock = FileLock("student.txt.lock")
nlp = spacy.load('it_core_news_sm')
model = Word2Vec.load('wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m')
keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/question", callback_data='q')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')]])

id_command={}

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if query_data=='q':
        bot.sendMessage(from_id, 'Digitare la domanda da inviare al prof o agli assistenti del corso:')
        id_command[from_id]=1
    if query_data=='r':
        bot.sendMessage(from_id, 'Digitare il bug da segnalare al programmatore:')
        id_command[from_id]=2
    if query_data=='s':
        bot.sendMessage(from_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)

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
array={}
threadLock = threading.Lock()

try:
    s=socket.socket()
    s.connect(("127.0.0.1",1500))
    print("Connected")
except socket.error as errore:
    print("Error:"+str(errore))
    sys.exit()

class OutputThread (threading.Thread):
    def __init__(self,s):
      threading.Thread.__init__(self)
      self.inp=s
    def run(self):
        while True:
            txt=self.inp.recv(4096)
            y=txt.decode().split(": ")
            threadLock.acquire()
            y[0] = y[0].replace("@",":")
            y[1] = y[1].replace("@",":")
            if y[0] in array:
                if array[y[0]] == "":
                    print("La risposta "+y[0]+" é stata eliminata")
                    if y[1] =='BANNED':
                        for elem in array[y[0]]['id']:
                            bot.sendMessage(elem, "La domanda '"+y[0]+"' é stata bannata")
                    else :
                        for elem in array[y[0]]['id']:
                            bot.sendMessage(elem, "La risposta alla domanda '"+y[0]+"' e' '"+y[1]+"'")
                    for i in array:
                        if y[0] == array[i]:
                            array[i]['a']=y[1]
                    with open('data.txt','w') as f:
                        f.write(str(array).replace("'",'"'))
            else :
                print("Error: String not found")
            threadLock.release()

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print(chat_id)
    req_type=0
    sim=0
    val=0
    num=0
    if content_type == 'text':
        threadLock.acquire()
        trovata = False
        txt=msg['text'].lower()
        if  txt == '/start' and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        elif  txt == '/question' and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, 'Digitare la domanda da inviare al prof o agli assistenti del corso:')
            id_command[chat_id]=1
        elif  txt == '/report' and req_type==0 :
            req_type=3
            trovata = True
            bot.sendMessage(chat_id, 'Digitare il bug da segnalare al programmatore:')
            id_command[chat_id]=2
        elif chat_id in id_command:
            if id_command[chat_id]==1 :
                req_type=1
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
                            with open('data.txt','w') as f:
                                f.write(str(array).replace("'",'"'))
                    elif array[val]['a']=='BANNED':
                        bot.sendMessage(chat_id, 'La domanda da te fatta é stata bannata')
                    else :
                        bot.sendMessage(chat_id, array[val]['a'])
            elif id_command[chat_id]==2 and req_type==0 :
                req_type=2
                with lock:
                    with open('student.txt','a') as f:
                        f.write("@@@"+txt+"###")
                bot.sendMessage(chat_id, 'Bug segnalato')
            del id_command[chat_id]
        else:
            req_type=4
            trovata = True
            bot.sendMessage(chat_id, 'Comando non trovato')
            bot.sendMessage(chat_id, 'Benvenuto nel bot di programmazione ad oggetti, selezionare un comando per usarlo', reply_markup=keyboard)
        if  not trovata and req_type==1:
            array[txt]['id']=[]
            array[txt]['id'].append(str(chat_id))
            with open('data.txt','w') as f:
                f.write(str(array).replace("'",'"'))
            array[txt]['a']=''
            bot.sendMessage(chat_id, 'Risposta non trovata. Domanda inviata al professore')
            msg=txt
            s.send(msg.encode())
        threadLock.release()

TOKEN = '1064330916:AAGjmjJZcEwyudWgPYplyP7OvyFQl4Ju_GI'
ShellThread=OutputThread(s)
ShellThread.start()
bot = telepot.Bot(TOKEN)

with open('data.txt','r') as json_file:
    array=json.load(json_file)

bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

print('Listening ...')

while 1:
    time.sleep(10)
