import telepot
import datetime
from databases.database_class import Database
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.exception import TelegramError, BotWasBlockedError
import os

db = Database()
telegram_error = "TelegramError"
bot_was_blocked_error = "BotWasBlockedError"

def send_bug(bot_name,chat_id,string):
    global db
    db.get_postgres().run_function("insert_bug",str(chat_id),"'"+bot_name+"'","'"+string+"'")
    send_logs("WARNING",f"{bot_name} >>> {string}",chat_id,recursive=True)

def send_message(bot,chat_id,string,reply_markup=ReplyKeyboardRemove(selective=True),recursive=True):
    global db
    try:
        return bot.sendMessage(chat_id,string,reply_markup=reply_markup)
    except TelegramError:
        db.get_postgres().run_function("insert_exception",str(chat_id),"'"+telegram_error+"'","'"+str(e)+"'",str(1))
        if recursive:
            send_logs("ERROR",e,chat_id)
    except BotWasBlockedError:
        db.get_postgres().run_function("insert_exception",str(chat_id),"'"+bot_was_blocked_error+"'","'"+str(e)+"'",str(2))
        if recursive:
            send_logs("ERROR",e,chat_id)

def tag_group(chat_type,user):
    string=""
    if chat_type=="group" or chat_type=="supergroup":
        string="@"+user["username"]+": "
    return string

def match_command(command,msg,chat_type,username):
    if chat_type=="private":
        return msg==command
    else:
        return msg==(command+"@"+username)

def send_document(bot,chat_id,string,doc_name):
    global db
    with open(doc_name+".txt", 'w') as f:
        f.write(string)
    with open(doc_name+".txt", 'r') as f:
        try:
            bot.sendDocument(chat_id, f, doc_name)
        except TelegramError:
            db.get_postgres().run_function("insert_exception",str(chat_id),"'"+telegram_error+"'","'"+str(e)+"'",str(3))
            if recursive:
                send_logs("ERROR",e,chat_id)
        except BotWasBlockedError:
            db.get_postgres().run_function("insert_exception",str(chat_id),"'"+bot_was_blocked_error+"'","'"+str(e)+"'",str(4))
            if recursive:
                send_logs("ERROR",e,chat_id)
    os.remove(doc_name+".txt")
    
def send_logs(level,name,chat_id,recursive=False):
    global db
    logs_users=db.get_postgres().run_function("telegram_id_logs_get")
    logs_string=format_logs_string(level,name,chat_id)
    for logs_user in logs_users:
        send_message(db.get_bot_logs(),logs_user,logs_string,recursive=recursive)

def format_logs_string(level,name,chat_id):
    match level:
        case "ERROR":
            return emoji.emojize(f'{str(chat_id)} >>> :red_circle: {name} :red_circle:')
        case "WARNING":
            return emoji.emojize(f'{str(chat_id)} >>> :yellow_circle: {name} :yellow_circle:')
        case "OK":
            return emoji.emojize(f'{str(chat_id)} >>> :green_circle: {name} :green_circle:')
        case _:
            return emoji.emojize(f'{str(chat_id)} >>> :black_circle: {name} :black_circle:')