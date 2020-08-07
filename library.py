import telepot
import datetime
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

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

def tagGroup(chat_type,user):
    string=""
    if chat_type=="group" or chat_type=="supergroup":
        string="@"+user["username"]+": "
    return string

def selection(chat_id,from_id,lang,list1,chat_type,bot,lang_class):
    user=bot.getChat(from_id)  
    data=[]
    for elem in list1:
        data.append([elem])
        createReplyKeyboard(data)
    keyboard1 = createReplyKeyboard(data)
    if list1 ==[] :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+lang_class.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
    else :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+lang_class.getString(lang,"select"),reply_markup=keyboard1)

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

def createReplyKeyboard(matrix,only_one=True):
    return ReplyKeyboardMarkup(keyboard=matrix_to_key(matrix),resize_keyboard=True,one_time_keyboard=True,selective=only_one)

def delete_bug(t,time,lang,bug_array):
    data={}
    if lang in bug_array:
        if t in bug_array[lang]:
            data[t]={}
            for elem in bug_array[lang][t]:
                if time<bug_array[lang][t][elem]:
                    data[t][elem]=bug_array[lang][t][elem]
    print(data)
    return data

def seg_bug(chat_id,from_id,txt,lang,chat_type,bot_type,bot,database,lang_class):
    time=datetime.datetime.today()
    bug_array=database.read_bug()
    print("1 : "+str(bug_array))
    if lang not in bug_array:
        bug_array[lang]={}
    print("2 : "+str(bug_array)+" , "+lang)
    if bot_type not in bug_array[lang]:
        bug_array[lang][bot_type]={}
    print("3 : "+str(bug_array)+" , "+bot_type)
    user=bot.getChat(from_id)
    bug_array[lang]=delete_bug(bot_type,time,lang,bug_array)
    print("4 : "+str(bug_array))
    if lang_class.matchArray(txt,lang,bug_array[lang][bot_type]) == None:
        bug_array[lang][bot_type][txt]=time+datetime.timedelta(days=14)
        for a_id in database.getAdmins(lang):
            database.get_bot_admin().get_bot().sendMessage(a_id,bot_type+": "+txt)
    bot.sendMessage(chat_id, tagGroup(chat_type,user)+lang_class.getString(lang,"bug"),reply_markup=ReplyKeyboardRemove(selective=True))
    database.write_bug(bug_array)

def matchCommand(command,msg,chat_type,username):
    print(command+" : "+msg)
    if chat_type=="private":
        print("case1: "+str(msg==command))
        return msg==command
    else:
        print("case2: "+str(msg==(command+"@"+username)))
        return msg==(command+"@"+username)