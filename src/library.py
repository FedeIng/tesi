import telepot
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.exception import TelegramError, BotWasBlockedError
import os

def set_time(from_id,chat_id,array):
    if from_id==chat_id:
        array[chat_id]=datetime.datetime.today()
    else :
        if chat_id not in array:
            array[chat_id]={}
            array[chat_id][from_id]=datetime.datetime.today()
        else :
            array[chat_id][from_id]=datetime.datetime.today()
    return array

def edit_message(bot,msg_id,reply_markup=None):
    try:
        bot.editMessageReplyMarkup(msg_id,reply_markup=reply_markup)
    except TelegramError:
        pass
    except BotWasBlockedError:
        pass

def send_doc(bot,chat_id,string,reply):
    q_string="questions.txt"
    with open(q_string,"w") as doc:
        doc.write(string)
    with open(q_string,"rb") as doc:
        try:
            bot.sendDocument(chat_id,doc,reply_to_message_id=reply)
        except TelegramError:
            pass
        except BotWasBlockedError:
            pass
    os.remove(q_string)

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

def del_id(from_id,chat_id,array):
    if from_id==chat_id:
        if chat_id in array:
            del array[chat_id]
    else :
        if chat_id in array:
            if from_id in array[chat_id]:
                del array[chat_id][from_id]
            if len(array[chat_id])==0:
                del array[chat_id]
    return array

def add_id(from_id,chat_id,array,val):
    if from_id==chat_id:
        array[chat_id]=val
    else :
        if chat_id not in array:
            array[chat_id]={}
            array[chat_id][from_id]=val
        else :
            array[chat_id][from_id]=val
    return array

def check_id(from_id,chat_id,array):
    ret_val=0
    if from_id==chat_id:
        if chat_id in array:
            ret_val=array[chat_id]
    else :
        if chat_id in array and from_id in array[chat_id]:
            ret_val=array[chat_id][from_id]
    return ret_val

def tag_group(chat_type,user):
    string=""
    if chat_type=="group" or chat_type=="supergroup":
        string="@"+user["username"]+": "
    return string

def selection(chat_id,from_id,lang,list1,chat_type,bot,lang_class,singleton,name):
    user=bot.getChat(from_id)  
    data=[]
    for elem in list1:
        data.append([elem])
        create_reply_keyboard(data)
    keyboard1 = create_reply_keyboard(data)
    if list1 ==[] :
        singleton.del_time_id(chat_type,lang_class,lang,from_id,chat_id,name)
        send_message(bot,chat_id, tag_group(chat_type,user)+lang_class.get_string(lang,"empty"),lang_class.get_string(lang,"canc"),singleton.check_time_id(chat_type,lang_class,lang,from_id,chat_id,name)!=0)
    else :
        send_message(bot,chat_id, tag_group(chat_type,user)+lang_class.get_string(lang,"select"),lang_class.get_string(lang,"canc"),singleton.check_time_id(chat_type,lang_class,lang,from_id,chat_id,name)!=0,keyboard1)

def list_to_str(data):
    stringa=""
    for elem in data:
        stringa+=elem+"\n"
    return stringa

def matrix_to_key(matrix):
    data=[]
    count=0
    for elem in matrix:
        data.append([])
        for elem1 in elem:
            data[count].append(KeyboardButton(text=elem1))
        count+=1
    return data

def array_to_matrix(array):
    data=[]
    for elem in array:
        data.append([elem])
    return data

def create_reply_keyboard(matrix,only_one=True):
    return ReplyKeyboardMarkup(keyboard=matrix_to_key(matrix),resize_keyboard=True,one_time_keyboard=True,selective=only_one)

def delete_bug(t,time,lang,bug_array):
    data={}
    if lang in bug_array and t in bug_array[lang]:
        data[t]={}
        for elem in bug_array[lang][t]:
            if time<bug_array[lang][t][elem]:
                data[t][elem]=bug_array[lang][t][elem]
    return data

def max_date_index(array):
    max_index=None
    for from_id in array:
        if max_index==None or array[from_id] > array[max_index]:
            max_index=from_id
    return max_index

def send_timeout(from_id,chat_id,bot,chat_type,lang_class,lang):
    user=bot.getChat(from_id)
    id_chat=None
    if chat_id==None:
        id_chat=from_id
    else:
        id_chat=chat_id
    bot.sendMessage(id_chat,tag_group(chat_type,user)+lang_class.get_string(lang,"timeout"),reply_markup=ReplyKeyboardRemove())

def delete_old(array,length,chat_id,bot,lang_class,lang):
    max_index=0
    delete_index={}
    max_index=None
    for from_id in array:
        if max_index < length:
            max_index+=1
            delete_index[from_id]=array[from_id]
            max_index=max_date_index(delete_index)
        else:
            if delete_index[from_index] > array[from_id]:
                del delete_index[max_index]
                delete_index[from_id]=array[from_id]
                max_index=max_date_index(delete_index)
    for from_id in delete_index:
        del array[from_id]
        send_timeout(from_id,chat_id,bot,chat_type,lang_class,lang)
    return array

#attr["length"]=length attr["time"]=time
def normalize_array(array,bot,lang_class,chat_id=None,chat_type="private",lang="en",attr={"length":1000,"time":30}):
    new_array={}
    time_now=datetime.datetime.today()
    time_now-=attr["time"]
    for from_id in array:
        if array[from_id] > time_now:
            new_array[from_id]=array[from_id]
        else:
            send_timeout(from_id,chat_id,bot,chat_type,lang_class,lang)
    l=len(new_array)
    if l > attr["length"]:
        new_array=delete_old(new_array,l-attr["length"],chat_id,bot,lang_class,lang)
    return new_array

#ids[chat]=chat_id ids[from]=from_id
#bot[bot]=bot bot[type]=bot_type
def seg_bug(ids,txt,lang,chat_type,bot,database,lang_class):
    time=datetime.datetime.today()
    bug_array=database.read_bug()
    if lang not in bug_array:
        bug_array[lang]={}
    if bot["type"] not in bug_array[lang]:
        bug_array[lang][bot["type"]]={}
    user=bot["bot"].getChat(ids["from"])
    bug_array[lang]=delete_bug(bot["type"],time,lang,bug_array)
    if lang_class.match_array(txt,lang,bug_array[lang][bot["type"]]) == None:
        bug_array[lang][bot["type"]][txt]=time+datetime.timedelta(days=14)
        for a_id in database.get_admins(lang):
            database.get_bot_admin().get_bot().sendMessage(a_id,bot["type"]+": "+txt)
    bot["bot"].sendMessage(ids["chat"], tag_group(chat_type,user)+lang_class.get_string(lang,"bug"),reply_markup=ReplyKeyboardRemove(selective=True))
    database.write_bug(bug_array)

def match_command(command,msg,chat_type,username):
    if chat_type=="private":
        return msg==command
    else:
        return msg==(command+"@"+username)