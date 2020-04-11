import telepot
from functions import match, msg_man, callback_man, post_1
import time
from filelock import Timeout, FileLock

bot_name="polito1_bot"

lockM = FileLock("mode.txt.lock")
lockS = FileLock("mode_s.txt.lock")

id_command=[]

array=['/start','/question','/report']

bot_name="polito1_bot"

def on_callback_query(msg):
    id_command=callback_man(msg,id_command,bot)

def on_chat_message(msg):
    id_command=msg_man(msg,array,id_command,bot,bot_name)

TOKEN = '1064330916:AAGjmjJZcEwyudWgPYplyP7OvyFQl4Ju_GI'
bot = telepot.Bot(TOKEN)

bot.message_loop({'chat':on_chat_message,'callback_query':on_callback_query})

while post_1("mode_s.txt",lockS,id_command,bot):
    time.sleep(10)