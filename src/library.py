import telepot
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.exception import TelegramError, BotWasBlockedError
import os

def send_message(bot,chat_id,string,button_str="Indietro",bool_val=False,reply_markup=ReplyKeyboardRemove(selective=True)):
    if reply_markup==None:
        try:
            return bot.sendMessage(chat_id,string)
        except TelegramError:
            pass
        except BotWasBlockedError:
            pass
        return
    if bool_val:
        reply_markup=sm_branch1(button_str,reply_markup)
    try:
        return bot.sendMessage(chat_id,string,reply_markup=reply_markup)
    except TelegramError:
        pass
    except BotWasBlockedError:
        pass
    
def sm_branch1(button_str,reply_markup):
    var=reply_markup[0]
    if reply_markup==ReplyKeyboardRemove(selective=True):
        reply_markup=create_reply_keyboard([[button_str]])
    elif reply_markup==ReplyKeyboardRemove() or reply_markup==ReplyKeyboardRemove(selective=False):
        reply_markup=create_reply_keyboard([[button_str]],False)
    else:
        var.append([KeyboardButton(text=button_str)])
        if len(reply_markup)==4:
            reply_markup=ReplyKeyboardMarkup(keyboard=var,resize_keyboard=True,one_time_keyboard=True,selective=reply_markup[3])
        else:
            reply_markup=ReplyKeyboardMarkup(keyboard=var,resize_keyboard=True,one_time_keyboard=True)
    return reply_markup

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
    with open(doc_name+".txt", 'w') as f:
        f.write(string)
    with open(doc_name+".txt", 'r') as f:
        try:
            bot.sendDocument(chat_id, f, doc_name)
        except TelegramError:
            pass
        except BotWasBlockedError:
            pass
    os.remove(doc_name+".txt")
    