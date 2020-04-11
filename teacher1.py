import telepot
from functions import match, msg_man, callback_man, post_1
import time
from filelock import Timeout, FileLock

bot_name="group_oop_bot"

lockM = FileLock("mode.txt.lock")
lockT = FileLock("mode_t.txt.lock")

bot_name="group_oop_bot"

array=['/start','/answer','/ban','/report','/list','/ban_list']

id_command=[]

def on_callback_query(msg):
    id_command=callback_man(msg,id_command,bot)

def on_chat_message(msg):
    id_command=msg_man(msg,array,id_command,bot,bot_name)

TOKEN = '1025374826:AAGcMIi_DeOLT986CCSzHfc0nhjFThblRfo'
bot = telepot.Bot(TOKEN)

bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

while post_1("mode_t.txt",lockT,id_command,bot):
    time.sleep(10)