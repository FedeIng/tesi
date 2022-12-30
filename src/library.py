import telepot
import datetime
from databases.database_class import Database
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.exception import TelegramError, BotWasBlockedError
import os
import emoji

db = Database()
telegram_error = "TelegramError"
bot_was_blocked_error = "BotWasBlockedError"

def send_bug(bot_name,chat_id,string):
    global db
    db.get_postgres().run_function("insert_bug",str(chat_id),f"'{bot_name}'",f"'{string}'")
    send_logs("WARNING",f"{bot_name} >>> {string}",chat_id,recursive=True)

def send_message(bot,chat_id,string,reply_markup=ReplyKeyboardRemove(selective=True),recursive=True):
    global db
    try:
        return bot.sendMessage(chat_id,string,reply_markup=reply_markup)
    except TelegramError as e:
        e_str = str(e).replace("'","''")
        db.get_postgres().run_function("insert_exception",str(chat_id),f"'{telegram_error}'",f"'{e_str}'",str(1))
        if recursive:
            send_logs("ERROR",e,chat_id)
    except BotWasBlockedError as e:
        e_str = str(e).replace("'","''")
        db.get_postgres().run_function("insert_exception",str(chat_id),f"'{bot_was_blocked_error}'",f"'{e_str}'",str(2))
        if recursive:
            send_logs("ERROR",e,chat_id)

def tag_group(chat_type,user):
    string=""
    if chat_type=="group" or chat_type=="supergroup":
        string=f"@{user['username']}: "
    return string

def match_command(command,msg,chat_type,username):
    if chat_type=="private":
        return msg==command
    else:
        return msg==(command+"@"+username)

def send_document(bot,chat_id,string,message):
    global db
    with open(f"{str(chat_id)}.txt", 'w') as f:
        f.write(string)
    with open(f"{str(chat_id)}.txt", 'r') as f:
        try:
            bot.sendDocument(chat_id, f, caption=message)
        except TelegramError as e:
            db.get_postgres().run_function("insert_exception",str(chat_id),f"'{telegram_error}'",f"'{str(e)}'",str(3))
            send_logs("ERROR",e,chat_id)
        except BotWasBlockedError as e:
            db.get_postgres().run_function("insert_exception",str(chat_id),f"'{bot_was_blocked_error}'",f"'{str(e)}'",str(4))
            send_logs("ERROR",e,chat_id)
    os.remove(f"{str(chat_id)}.txt")
    
def send_logs(level,name,chat_id,recursive=False):
    global db
    logs_users=db.get_postgres().run_function("telegram_id_logs_get")
    logs_string=format_logs_string(level,name,chat_id)
    for logs_user in logs_users:
        send_message(db.get_bot_logs().get_bot(),logs_user,logs_string,recursive=recursive)

def format_logs_string(level,name,chat_id):
    match level:
        case "ERROR":
            return emoji.emojize(f"{str(chat_id)} >>> :red_circle: {name} :red_circle:")
        case "WARNING":
            return emoji.emojize(f"{str(chat_id)} >>> :yellow_circle: {name} :yellow_circle:")
        case "OK":
            return emoji.emojize(f"{str(chat_id)} >>> :green_circle: {name} :green_circle:")
        case _:
            return emoji.emojize(f"{str(chat_id)} >>> :black_circle: {name} :black_circle:")