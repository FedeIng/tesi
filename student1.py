import telepot
from functions import match
import time
from filelock import Timeout, FileLock

bot_name="polito1_bot"

lockM = FileLock("mode.txt.lock")
lockN = FileLock("num.txt.lock")

array=['/start','/question','/report']

id_command=[]

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    bot.sendMessage(chat_id, 'Bot in manutenzione, riprovare prossimamente')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in id_command:
        id_command.append(chat_id)
    if content_type == 'text':
        txt=msg['text'].lower()
        for elem in array:
            if match(txt,elem,chat_type,bot_name):
                bot.sendMessage(chat_id, 'Bot in manutenzione, riprovare prossimamente')

TOKEN = '1064330916:AAGjmjJZcEwyudWgPYplyP7OvyFQl4Ju_GI'
bot = telepot.Bot(TOKEN)

bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

while 1:
    with lockM:
        with open('mode.txt','r') as f:
            mode=f.read()
            if mode=="std":
                print("Student1 bot ended")
                for id in id_command:
                    bot.sendMessage(id, 'Il bot é di nuovo operativo')
                with lockN:
                    num="0"
                    with open('num.txt','r') as f:
                        num=f.read()
                    num=int(num)+1
                    with open('num.txt','w') as f:
                        f.write(str(num))
                exit()
    time.sleep(10)