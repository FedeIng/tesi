import telepot
import json
import sys
import re
import time
import hashlib, binascii, os
import random
import string
import datetime
from telepot.loop import MessageLoop
from tree_class import *
from urllib.request import urlopen
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from firebase import firebase
from database_class import *

database = Database()
admin_pwd=None
bot_pwd=None
lang_bool={}
banned_user={}
user_request={}
prev_lang={}
query_bool={}
topic_name={}
isLogged={}
boolvett={}
lang_array=["it","de","en","es","fr"]
tokens=[]
bug_array={}
bot_creation=None
bot_admin=None
bot_teacher=None
bot_getlink=None
bot_student={}
tree=Tree(database)
bots_info={}
flag_list=["\U0001F1EE\U0001F1F9 IT \U0001F1EE\U0001F1F9","\U0001F1E9\U0001F1EA DE \U0001F1E9\U0001F1EA","\U0001F1EB\U0001F1F7 FR \U0001F1EB\U0001F1F7","\U0001F1EC\U0001F1E7 EN \U0001F1EC\U0001F1E7","\U0001F1EA\U0001F1F8 ES \U0001F1EA\U0001F1F8"]
id_command={}
id_creation={}
unconfirmed_bot={}
unc_del={}
key_st = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/question", callback_data='q')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/revision", callback_data='rv')],[InlineKeyboardButton(text="/change_lang", callback_data='cl')]])
key_te = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/free_list", callback_data='fl')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')],[InlineKeyboardButton(text="/sban", callback_data='sb')],[InlineKeyboardButton(text="/change", callback_data='c')],[InlineKeyboardButton(text="/delete", callback_data='d')],[InlineKeyboardButton(text="/hints", callback_data='h')],[InlineKeyboardButton(text="/add_hint", callback_data='ah')]])
key_cr = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/new_bot", callback_data='n')],[InlineKeyboardButton(text="/delete_bot", callback_data='d')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/change_pwd", callback_data='c')]])
i=0
switcher={
            "\U0001F1EE\U0001F1F9 IT \U0001F1EE\U0001F1F9":"it",
            "\U0001F1E9\U0001F1EA DE \U0001F1E9\U0001F1EA":"de",
            "\U0001F1EB\U0001F1F7 FR \U0001F1EB\U0001F1F7":"fr",
            "\U0001F1EC\U0001F1E7 EN \U0001F1EC\U0001F1E7":"en",
            "\U0001F1EA\U0001F1F8 ES \U0001F1EA\U0001F1F8":"es"
        }

def sendNotification():
    for bot_id in bot_student:
        tree.sendNotification(bot_teacher,bot_student[bot_id]["bot"],bot_student[bot_id]["topic"])

def write_ban():
    global banned_user
    global database
    data={}
    for elem in banned_user:
        data[str(elem)]=banned_user[elem]
    result=database.put('/bots/teachers', name="banned", data=data)
    print(result)
    #with open("ban.txt","w") as jfile:
        #json.dump(banned_user,jfile)
        
def read_ban():
    global banned_user
    global database
    #with open("ban.txt","r") as json_file:
        #banned_user=json.load(json_file)
    result=database.get('/bots/teachers/banned','')
    data={}
    for elem in result:
        data[int(elem)]=result[elem]
    banned_user=data

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

def write_bug():
    global bug_array
    global database
    global lang_array
    role_array=["students","teachers"]
    for lang in bug_array:
        for role in bug_array[lang]:
            data={}
            for e in bug_array[lang][role]:
                data[e]=bug_array[lang][role][e].isoformat()
            if len(data)>0:
                result=database.put('/bots/admin/'+lang, name=role, data=data)
    #with open("bug.txt","w") as jfile:
        #json.dump(data,jfile)

def read_bug():
    global bug_array
    global database
    global lang_array
    role_array=["students","teachers"]
    data={}
    #with open("bug.txt","r") as json_file:
        #data=json.load(json_file)
    for lang in lang_array:
        for role in role_array:
            result=database.get('/bots/admin/'+lang+'/'+role+'','')
            if result!=None:
                if lang not in data:
                    data[lang]={}
                if role not in data[lang]:
                    data[lang][role]={}
                for e in data[lang][role]:
                    date=datetime.datetime.fromisoformat(data[lang][role][e])
                    data[lang][role][e]=date
    bug_array=data

def write_pwd():
    global user_request
    data={}
    for elem in user_request:
        if len(user_request[elem])>0:
            data[str(elem)]=[]
            for e in user_request[elem]:
                data[str(elem)].append(e.isoformat())
    result=database.put('/bots/pwd',name='requests',data=data)
    #with open("pwd.txt","w") as jfile:
        #json.dump(data,jfile)

def read_pwd():
    global user_request
    global database
    data={}
    #with open("pwd.txt","r") as json_file:
        #data=json.load(json_file)
    result=database.get('/bots/pwd/requests','')
    for elem in result:
        data[int(elem)]=[]
        for e in result[elem]:
            print(e)
            date=datetime.datetime.fromisoformat(e)
            data[int(elem)].append(date)
    user_request=data

def delete_req(time,vett):
    data=[]
    for elem in vett:
        if time < elem:
            data.append(elem)
    return data

def req_pwd(chat_id):
    global user_request
    time=datetime.datetime.today()
    if chat_id not in user_request:
        user_request[chat_id]=[]
    user_request[chat_id]=delete_req(time,user_request[chat_id])
    user_request[chat_id].append(time+datetime.timedelta(days=30))
    write_pwd()
    if len(user_request[chat_id]) > 10:
        return False
    return True

def randomStringwithDigitsAndSymbols(stringLength=10):
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def hash_password(password):
    """Hash a password for storing."""
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
 
def verify_password(stored_password, provided_password):
    """Verify a stored password against one provided by user"""
    salt = stored_password[:64]
    stored_password = stored_password[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                  provided_password.encode('utf-8'), 
                                  salt.encode('ascii'), 
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == stored_password

def changePwdNotifier(pwd,topic):
    global bot_pwd
    global tree
    global bot_teacher
    bot_pwd.sendMessage(admin_pwd,"New password for "+topic+" : "+pwd)
    data=tree.getTeachersAndCollaborators(topic)
    for lang in data:
        for elem in data[lang]:
            bot_teacher.sendMessage(elem,tree.getString(lang,"pwd",xxx=pwd))

def del_id(from_id,chat_id):
    if from_id==chat_id:
        if chat_id in id_command:
            del id_command[chat_id]
    else :
        if chat_id in id_command:
            if from_id in id_command[chat_id]:
                del id_command[chat_id][from_id]
            if len(id_command[chat_id])==0:
                del id_command[chat_id]

def check_id(from_id,chat_id):
    global id_command
    ret_val=0
    if from_id==chat_id:
        if chat_id in id_command:
            ret_val=id_command[chat_id]
    else :
        if chat_id in id_command and from_id in id_command[chat_id]:
            ret_val=id_command[chat_id][from_id]
    return ret_val

def case1(chat_id,from_id,txt,lang,topic,chat_type):
    global tree
    user=bot_teacher.getChat(from_id)
    res=tree.getResponse(txt,lang,topic)
    if res!=None:
        tree.setQID(chat_id,from_id,txt,topic)
        bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"answer",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
        add_id(from_id,chat_id,4)
    else:
        bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"error"),reply_markup=ReplyKeyboardRemove(selective=True))

def case3(chat_id,from_id,txt,lang,topic,chat_type):
    global tree
    user=bot_teacher.getChat(from_id)
    tree.setBan(txt,lang,topic)
    topic_id=getIdByTopic(topic)
    vett=tree.getIdsArray(topic,lang,txt)
    bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"banned_q",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
    for elem in vett:
        bot_student[topic_id]["bot"].sendMessage(elem,tree.getString(lang,"banned_q",xxx=txt))
    del_id(from_id,chat_id)

def case4(chat_id,from_id,txt,lang,topic,chat_type):
    global tree
    user=bot_teacher.getChat(from_id)
    question=tree.setRes(chat_id,from_id,txt,lang,topic)
    if question==None:
        return
    topic_id=getIdByTopic(topic)
    vett=tree.getIdsArray(topic,lang,question)
    bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"answer_q",xxx=question,yyy=txt),reply_markup=ReplyKeyboardRemove(selective=True))
    for elem in vett:
        bot_student[topic_id]["bot"].sendMessage(elem,tree.getString(lang,"answer_q",xxx=question,yyy=txt))
    del_id(from_id,chat_id)

def case5(chat_id,from_id,txt,lang,topic,chat_type):
    global tree
    user=bot_teacher.getChat(from_id)
    tree.setSban(txt,lang,topic)
    topic_id=getIdByTopic(topic)
    vett=tree.getIdsArray(topic,lang,txt)
    bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"banned_q",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
    for elem in vett:
        bot_student[topic_id]["bot"].sendMessage(elem,tree.getString(lang,"banned_q",xxx=txt))
    del_id(from_id,chat_id)

def case6(chat_id,from_id,txt,lang,topic,chat_type):
    global tree
    user=bot_teacher.getChat(from_id)
    splitted=txt[1:-1].split("\" -> \"")
    tree.add_question_by_hint(lang,splitted[0],splitted[1],chat_id,from_id,topic)
    bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"answer_q",xxx=splitted[0],yyy=splitted[1]),reply_markup=ReplyKeyboardRemove(selective=True))
    del_id(from_id,chat_id)

def getBot(msg):
    global bot_student
    global i
    for bot in bot_student:
        elem=bot_student[bot]["bot"].getUpdates(i)
        i+=1
        for subelem in elem:
            if msg == subelem["message"]:
                return bot_student[bot]["bot"]
            if i>1000000:
                i=0
    return None

def del_id(from_id,chat_id):
    if from_id==chat_id:
        if chat_id in id_command:
            del id_command[chat_id]
    else :
        if chat_id in id_command:
            if from_id in id_command[chat_id]:
                del id_command[chat_id][from_id]
            if len(id_command[chat_id])==0:
                del id_command[chat_id]

def add_id(from_id,chat_id,val):
    if from_id==chat_id:
        id_command[chat_id]=val
    else :
        if chat_id not in id_command:
            id_command[chat_id]={}
            id_command[chat_id][from_id]=val
        else :
            id_command[chat_id][from_id]=val

def delete_bug(t,time,lang):
    data={}
    global bot_student
    if lang in bug_array:
        if t in bug_array[lang]:
            data[t]={}
            for elem in bug_array[lang][t]:
                if time<bug_array[lang][t][elem]:
                    data[t][elem]=bug_array[lang][t][elem]
    print(data)
    bug_array[lang]=data

def dict_to_key(d):
    a=[]
    for index in d:
        a.append(index)
    return a

def seg_bug(chat_id,from_id,txt,lang,chat_type,bot_id=None):
    global bot_student
    global bug_array
    time=datetime.datetime.today()
    if lang not in bug_array:
        bug_array[lang]={}
    if bot_id == None:
        if "teacher" not in bug_array[lang]:
            bug_array[lang]["teacher"]={}
        user=bot_teacher.getChat(from_id)
        delete_bug("teacher",time,lang)
        if tree.matchArray(txt,lang,bug_array[lang]["teacher"]) == None:
            bug_array[lang]["teacher"][txt]=time+datetime.timedelta(days=14)
            list_admins=tree.getAdmins(lang)
            for a_id in list_admins:
                bot_admin.sendMessage(a_id,"Teacher: "+txt)
        bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"bug"),reply_markup=ReplyKeyboardRemove(selective=True))
    else:
        if "student" not in bug_array[lang]:
            bug_array[lang]["student"]={}
        user=bot_student[bot_id]["bot"].getChat(from_id)
        delete_bug("student",time,lang)
        if tree.matchArray(txt,lang,bug_array[lang]["student"]) == None:
            bug_array[lang]["student"][txt]=time+datetime.timedelta(days=14)
            list_admins=tree.getAdmins(lang)
            for a_id in list_admins:
                bot_admin.sendMessage(a_id,"Student: "+txt)
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"bug"),reply_markup=ReplyKeyboardRemove(selective=True))
    write_bug()

def list_to_str(data):
    stringa=""
    for elem in data:
        stringa+=elem+"\n"
    return stringa

def list_sel(chat_id,from_id,lang,condition,topic,chat_type,bot_id=None):
    list1=[]
    bot=None
    global bot_student
    global tree
    user=""
    if bot_id==None:
        bot=bot_teacher
        user=bot_teacher.getChat(from_id)
    else:
        bot=bot_student[bot_id]["bot"]
    list1=tree.getResArray(topic,lang,condition)
    if list1 ==[] :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
    else :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+list_to_str(list1),reply_markup=ReplyKeyboardRemove(selective=True))

def selection(chat_id,from_id,lang,condition,topic,chat_type,bot_id=None):
    list1=[]
    bot=None
    global bot_student
    global tree
    user=""
    if bot_id==None:
        bot=bot_teacher
        user=bot_teacher.getChat(from_id)
    else:
        bot=bot_student[bot_id]["bot"]
        user=bot.getChat(from_id)
    list1=tree.getResArray(topic,lang,condition)   
    data=[]
    for elem in list1:
        data.append([elem])
        createReplyKeyboard(data)
    keyboard1 = createReplyKeyboard(data)
    if list1 ==[] :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
    else :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"select"),reply_markup=keyboard1)

def switch_teacher(chat_id,from_id,txt,lang,topic,chat_type):
    global id_command
    global tree
    tree.set_nlp(lang)
    if check_id(from_id,chat_id)==1:
        case1(chat_id,from_id,txt,lang,topic,chat_type)
    elif check_id(from_id,chat_id)==2:
        seg_bug(chat_id,from_id,txt,lang,chat_type)
        del_id(from_id,chat_id)
    elif check_id(from_id,chat_id)==3:
        case3(chat_id,from_id,txt,lang,topic,chat_type)
    elif check_id(from_id,chat_id)==4:
        case4(chat_id,from_id,txt,lang,topic,chat_type)
    elif check_id(from_id,chat_id)==5:
        case5(chat_id,from_id,txt,lang,topic,chat_type)
    elif check_id(from_id,chat_id)==6:
        case6(chat_id,from_id,txt,lang,topic,chat_type)

def teacher_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    global id_command
    global bot_student
    global tree
    global query_bool
    chat_id=msg["message"]["chat"]["id"]
    chat_type=msg["message"]["chat"]["type"]
    topic=tree.getTopic(chat_id)
    user=bot_teacher.getChat(from_id)
    print(msg)
    if str(chat_id) in banned_user:
        if banned_user[str(chat_id)]>99:
            bot_teacher.sendMessage(chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
            return
    if chat_id not in query_bool:
        query_bool[chat_id]=False
    if topic==None:
        bot_teacher.sendMessage(chat_id,"Please select the topic:",reply_markup=topicKeyboard())
        isLogged[chat_id]=True
        return
    lang=tree.getSuperUserLang(chat_id,topic)
    if query_data=='s':
        bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=topic), reply_markup=ReplyKeyboardRemove(selective=True))
        bot_teacher.sendMessage(chat_id, tree.getString(lang,"command"), reply_markup=key_te)
        del_id(from_id,chat_id)
    elif query_data=='a':
        selection(chat_id,from_id,lang,"FREE",topic,chat_type)
        add_id(from_id,chat_id,1)
    elif query_data=='b':
        selection(chat_id,from_id,lang,"FREE",topic,chat_type)
        add_id(from_id,chat_id,3)
    elif query_data=='r':
        bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
        add_id(from_id,chat_id,2)
    elif query_data=='l':
        list_sel(chat_id,from_id,lang,"ANSWER",topic,chat_type)
        del_id(from_id,chat_id)
    elif query_data=='fl':
        list_sel(chat_id,from_id,lang,"FREE",topic,chat_type)
        del_id(from_id,chat_id)
    elif query_data=='bl':
        list_sel(chat_id,from_id,lang,"BANNED",topic,chat_type)
        del_id(from_id,chat_id)
    elif query_data=='sb':
        selection(chat_id,from_id,lang,"BANNED",topic,chat_type)
        add_id(from_id,chat_id,5)
    elif query_data=='c':
        selection(chat_id,from_id,lang,"ANSWER",topic,chat_type)
        add_id(from_id,chat_id,1)
    elif query_data=='d':
        tree.deleteTC(chat_id,bot_student[getIdByTopic(topic)]["bot"])
        bot_teacher.sendMessage(chat_id, "Permission deleted",reply_markup=ReplyKeyboardRemove())
        del_id(from_id,chat_id)
    elif query_data=='h':
        bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+vett_to_str(tree.getHint(topic,lang),lang),reply_markup=ReplyKeyboardRemove(selective=True))
        del_id(from_id,chat_id)
    elif query_data=='ah':
        hints=tree.getHint(topic,lang)
        if len(hints)>0:
            bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"select_hint"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
            add_id(from_id,chat_id,6)
        else :
            bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"empty"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
            del_id(from_id,chat_id)

def vett_to_str(vett,lang):
    string=""
    for elem in vett:
        if string != "":
            string+="\n"
        string+=elem
    if string=="":
        string=tree.getString(lang,"empty")
    return string

def getTopicList():
    global bot_student
    global unconfirmed_bot
    data=[]
    for elem in bot_student:
        data.append(bot_student[elem]["topic"])
    for elem in unconfirmed_bot:
        data.append(unconfirmed_bot[elem]["topic"])
    return data

def getTokenList():
    global bot_student
    global tokens
    data=[]
    for elem in bot_student:
        data.append(bot_student[elem]["token"])
    for elem in tokens:
        data.append(elem)
    return data

def tagGroup(chat_type,user):
    string=""
    if chat_type=="group" or chat_type=="supergroup":
        string="@"+user["username"]+": "
    return string

def teacher_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global id_command
    global bot_teacher
    global tree
    global query_bool
    from_id=msg["from"]["id"]
    topic=tree.getTopic(chat_id)
    user=bot_teacher.getChat(from_id)
    print(msg)
    if str(chat_id) in banned_user:
        if banned_user[str(chat_id)]>99:
            bot_teacher.sendMessage(chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
            return
    if chat_id not in lang_bool:
        lang_bool[chat_id]=False
    if chat_id not in query_bool:
        query_bool[chat_id]=False
    if lang_bool[chat_id]==True:
        if tree.checkTeach(prev_lang[chat_id],msg["text"]):
            lang=prev_lang[chat_id]
            bot_teacher.sendMessage(chat_id, tree.getString(lang,"teacher"),reply_markup=ReplyKeyboardRemove())
            tree.addTeachers([chat_id],topic_name[chat_id],lang,bot_student[getIdByTopic(topic_name[chat_id])]["bot"])
            del topic_name[chat_id]
            del prev_lang[chat_id]
        elif tree.checkColl(prev_lang[chat_id],msg["text"]):
            lang=prev_lang[chat_id]
            bot_teacher.sendMessage(chat_id, tree.getString(lang,"collaborator"),reply_markup=ReplyKeyboardRemove())
            tree.addCollaborators([chat_id],topic_name[chat_id],lang,bot_student[getIdByTopic(topic_name[chat_id])]["bot"])
            del topic_name[chat_id]
            del prev_lang[chat_id]
        query_bool[chat_id]=False
        lang_bool[chat_id]=False
        return
    if query_bool[chat_id]==True:
        if msg["text"] in flag_list:
            prev_lang[chat_id]=switcher.get(msg["text"],"")
            bot_teacher.sendMessage(chat_id, tree.getString(prev_lang[chat_id],"roles"), reply_markup=tree.getLangBoard(prev_lang[chat_id],["teacher","collaborator"]))
            lang_bool[chat_id]=True
        return
    if topic==None:
        if chat_id in isLogged:
            if isLogged[chat_id]:
                if msg["text"] in getTopicList():
                    bot_teacher.sendMessage(chat_id,"Copy/paste the password:",reply_markup=ReplyKeyboardRemove())
                    topic_name[chat_id]=msg["text"]
                    isLogged[chat_id]=False
                    return
            else:
                if verify_password(tree.getHash(topic_name[chat_id]), msg["text"]):
                    if str(chat_id) in banned_user:
                        del banned_user[str(chat_id)]
                    bot_teacher.sendMessage(chat_id,"Choose a language:",reply_markup=tree.setKeyboard(lang_array))
                    query_bool[chat_id]=True
                    write_ban()
                    return
            if str(chat_id) in banned_user:
                banned_user[str(chat_id)]+=1
            else:
                banned_user[str(chat_id)]=1
            bot_teacher.sendMessage(chat_id,"Error, retry:",reply_markup=ReplyKeyboardRemove())
            bot_teacher.sendMessage(chat_id,"Please select the topic:",reply_markup=topicKeyboard())
            isLogged[chat_id]=True
            write_ban()
            if chat_id in topic_name:
                del topic_name[chat_id]
        else:
            bot_teacher.sendMessage(chat_id,"Please select the topic:",reply_markup=topicKeyboard())
            isLogged[chat_id]=True
        return
    lang=tree.getSuperUserLang(chat_id,topic)
    if content_type == 'text':
        if tree.matchCommand(chat_id,'/start',msg,bot_teacher,lang):
            bot_teacher.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=topic), reply_markup=ReplyKeyboardRemove(selective=True))
            bot_teacher.sendMessage(chat_id, tree.getString(lang,"command"), reply_markup=key_te)
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/answer',msg,bot_teacher,lang):
            selection(chat_id,from_id,lang,"FREE",topic,chat_type)
            add_id(from_id,chat_id,1)
        elif tree.matchCommand(chat_id,'/ban',msg,bot_teacher,lang):
            selection(chat_id,from_id,lang,"FREE",topic,chat_type)
            add_id(from_id,chat_id,3)
        elif tree.matchCommand(chat_id,'/report',msg,bot_teacher,lang):
            bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
            add_id(from_id,chat_id,2)
        elif tree.matchCommand(chat_id,'/list',msg,bot_teacher,lang):
            list_sel(chat_id,from_id,lang,"ANSWER",topic,chat_type)
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/ban_list',msg,bot_teacher,lang):
            list_sel(chat_id,from_id,lang,"BANNED",topic,chat_type)
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/free_list',msg,bot_teacher,lang):
            list_sel(chat_id,from_id,lang,"FREE",topic,chat_type)
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/sban',msg,bot_teacher,lang):
            selection(chat_id,from_id,lang,"BANNED",topic,chat_type)
            add_id(from_id,chat_id,5)
        elif tree.matchCommand(chat_id,'/change',msg,bot_teacher,lang):
            selection(chat_id,from_id,lang,"ANSWER",topic,chat_type)
            add_id(from_id,chat_id,1)
        elif tree.matchCommand(chat_id,'/delete',msg,bot_teacher,lang):
            tree.deleteTC(chat_id,bot_student[getIdByTopic(topic)]["bot"])
            bot_teacher.sendMessage(chat_id, "Permission deleted",reply_markup=ReplyKeyboardRemove())
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/hints',msg,bot_teacher,lang):
            bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+vett_to_str(tree.getHint(topic,lang),lang),reply_markup=ReplyKeyboardRemove(selective=True))
            del_id(from_id,chat_id)
        elif tree.matchCommand(chat_id,'/add_hint',msg,bot_teacher,lang):
            bot_teacher.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"select_hint"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
            add_id(from_id,chat_id,6)
        elif check_id(from_id,chat_id) != 0:
            switch_teacher(chat_id,from_id,msg["text"],lang,topic,chat_type)

def seg_rev(chat_id,from_id,txt,lang,bot_id,chat_type):
    global tree
    user=bot_student[bot_id]["bot"].getChat(from_id)
    bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"revision",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
    response=tree.getResponse(txt,lang,bot_student[bot_id]["topic"])
    if response != None and response != "":
        teacher_array=tree.getResID(lang,bot_student[bot_id]["topic"])
        for teacher_id in teacher_array:
            bot_teacher.sendMessage(teacher_id, tree.getString(lang,"revision",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))

def set_lang(chat_id,from_id,topic,lang,bot,chat_type):
    user=bot.getChat(from_id)
    if tree.bot_enabled(topic):
        bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"lang"),reply_markup=tree.setChooseLang(topic))
    else:
        bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"disable"),reply_markup=ReplyKeyboardRemove())

def match_speech(chat_id,from_id,txt,lang,bot_id,chat_type):
    global bot_student
    global tree
    is_new=tree.checkLangStr(txt,"new_q")
    if not is_new:
        tree.setQID(chat_id,from_id,txt,bot_student[bot_id]["topic"])
    user=bot_student[bot_id]["bot"].getChat(from_id)
    elem=tree.getQID(chat_id,from_id,bot_student[bot_id]["topic"])
    response=None
    if not is_new:
        response=tree.getResponse(elem,lang,bot_student[bot_id]["topic"],chat_id)
    if response == None:
        tree.setQuestion(elem,lang,bot_student[bot_id]["topic"],chat_id)
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"q_not_found",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
        teacher_array=tree.getResID(lang,bot_student[bot_id]["topic"])
        for teacher_id in teacher_array:
            bot_teacher.sendMessage(teacher_id, tree.getString(lang,"revision",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
    elif response == "BANNED":
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"banned_q",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
    elif response == "":
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"wait_q",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
    else:
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"answer_q",xxx=elem,yyy=response),reply_markup=ReplyKeyboardRemove(selective=True))
    tree.delQID(chat_id,from_id,bot_student[bot_id]["topic"])

def final_set(chat_id,from_id,txt,lang,bot_id,chat_type):
    global switcher
    global tree
    user=bot_student[bot_id]["bot"].getChat(from_id)
    set_lang=switcher.get(txt)
    tree.setUserLang(chat_id,set_lang,bot_student[bot_id]["topic"])
    bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(set_lang,"setted_lang"),reply_markup=ReplyKeyboardRemove(selective=True))

def sel_question(chat_id,from_id,txt,lang,bot_id,chat_type):
    global tree
    list_val=tree.getSent(lang,txt)
    user=bot_student[bot_id]["bot"].getChat(from_id)
    if len(list_val)!=1:
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"error_q"),reply_markup=ReplyKeyboardRemove(selective=True))
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
        return
    txt=list_val[0]
    BRes=tree.getBestResp(txt,lang,bot_student[bot_id]["topic"])
    tree.setQID(chat_id,from_id,txt,bot_student[bot_id]["topic"])
    if BRes==[]:
        match_speech(chat_id,from_id,tree.getString(lang,"new_q"),lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif txt in BRes:
        match_speech(chat_id,from_id,txt,lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    else:
        BRes.append(tree.getString(lang,"new_q"))
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"select_q"),reply_markup=createReplyKeyboard(array_to_matrix(BRes)))
        tree.add_id(from_id,chat_id,1,bot_student[bot_id]["topic"])

def switch_student(chat_id,from_id,txt,lang,bot_id,chat_type):
    global tree
    tree.set_nlp(lang)
    if tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==1:
        match_speech(chat_id,from_id,txt,lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==2:
        seg_bug(chat_id,from_id,txt,lang,chat_type,bot_id)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==3:
        seg_rev(chat_id,from_id,txt,lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==4:
        final_set(chat_id,from_id,txt,lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==5:
        sel_question(chat_id,from_id,txt,lang,bot_id,chat_type)

def list_by_user(chat_id,from_id,lang,bot_id,chat_type):
    list1=[]
    bot=None
    global bot_student
    global tree
    bot=bot_student[bot_id]["bot"]
    user=bot.getChat(from_id)
    list1=tree.getQArray(chat_id,lang,bot_student[bot_id]["topic"])
    if list1 ==[] :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
    else :
        bot.sendMessage(chat_id,tagGroup(chat_type,user)+list_to_str(list1),reply_markup=ReplyKeyboardRemove(selective=True))

def student_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    global bot_student
    global tree
    chat_id=msg["message"]["chat"]["id"]
    bot_id=msg["message"]["from"]["id"]
    chat_type=msg["message"]["chat"]["type"]
    user=bot_student[bot_id]["bot"].getChat(from_id)
    lang=tree.getUserLang(chat_id,bot_student[bot_id]["topic"])
    if lang==None and not tree.check_id(from_id,chat_id,bot_student[bot_id]["topic"])==4:
        set_lang(chat_id,from_id,bot_student[bot_id]["topic"],msg['from']['language_code'],bot_student[bot_id]["bot"],chat_type)
        tree.add_id(from_id,chat_id,4,bot_student[bot_id]["topic"])
    elif query_data=='s':
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=bot_student[bot_id]["topic"]), reply_markup=ReplyKeyboardRemove(selective=True))
        bot_student[bot_id]["bot"].sendMessage(chat_id, tree.getString(lang,"command"), reply_markup=key_st)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])
    elif query_data=='q':
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"question"),reply_markup=ReplyKeyboardRemove(selective=True))
        tree.add_id(from_id,chat_id,5,bot_student[bot_id]["topic"])
    elif query_data=='r':
        bot_student[bot_id]["bot"].sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
        tree.add_id(from_id,chat_id,2,bot_student[bot_id]["topic"])
    elif query_data=='rv':
        selection(chat_id,from_id,lang,"ANSWER",bot_student[bot_id]["topic"],chat_type,bot_id)
        tree.add_id(from_id,chat_id,3,bot_student[bot_id]["topic"])
    elif query_data=='cl':
        set_lang(chat_id,from_id,bot_student[bot_id]["topic"],lang,bot_student[bot_id]["bot"],chat_type)
        tree.add_id(from_id,chat_id,4,bot_student[bot_id]["topic"])
    elif query_data=='l':
        list_by_user(chat_id,from_id,lang,bot_id,chat_type)
        tree.del_id(from_id,chat_id,bot_student[bot_id]["topic"])

def student_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global id_command
    global bot_student
    global tree
    from_id=msg["from"]["id"]
    print(msg)
    txt=""
    if content_type == 'text':
        bot=getBot(msg)
        user=bot.getChat(from_id)
        lang=tree.getUserLang(chat_id,bot_student[bot.getMe()["id"]]["topic"])
        if lang==None and not tree.check_id(from_id,chat_id,bot_student[bot.getMe()["id"]]["topic"])==4:
            set_lang(chat_id,from_id,bot_student[bot.getMe()["id"]]["topic"],msg['from']['language_code'],bot_student[bot.getMe()["id"]]["bot"],chat_type)
            tree.add_id(from_id,chat_id,4,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/start',msg,bot_student[bot.getMe()["id"]],lang):
            bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=bot_student[bot.getMe()["id"]]["topic"]), reply_markup=ReplyKeyboardRemove(selective=True))
            bot.sendMessage(chat_id, tree.getString(lang,"command"), reply_markup=key_st)
            tree.del_id(from_id,chat_id,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/question',msg,bot_student[bot.getMe()["id"]],lang):
            bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"question"),reply_markup=ReplyKeyboardRemove(selective=True))
            tree.add_id(from_id,chat_id,5,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/report',msg,bot_student[bot.getMe()["id"]],lang):
            bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
            tree.add_id(from_id,chat_id,2,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/revision',msg,bot_student[bot.getMe()["id"]],lang):
            selection(chat_id,from_id,lang,"ANSWER",bot_student[bot.getMe()["id"]]["bot"],chat_type,bot.getMe()["id"])
            tree.add_id(from_id,chat_id,3,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/change_lang',msg,bot_student[bot.getMe()["id"]],lang):
            set_lang(chat_id,from_id,bot_student[bot.getMe()["id"]]["topic"],lang,bot_student[bot.getMe()["id"]]["bot"],chat_type)
            tree.add_id(from_id,chat_id,4,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.matchCommand(chat_id,'/list',msg,bot_student[bot.getMe()["id"]],lang):
            list_by_user(from_id,chat_id,lang,bot.getMe()["id"],chat_type)
            tree.del_id(from_id,chat_id,bot_student[bot.getMe()["id"]]["topic"])
        elif tree.check_id(chat_id,from_id,bot_student[bot.getMe()["id"]]["topic"]) != 0:
            switch_student(chat_id,from_id,msg["text"],lang,bot.getMe()["id"],chat_type)

def create_hash(chat_id,pwd,topic=None):
    h=hash_password(pwd)
    if topic==None:
        tree.createNode(unconfirmed_bot[chat_id]["topic"])
        tree.setHash(unconfirmed_bot[chat_id]["topic"],h)
    else:
        tree.setHash(topic,h)
    return h

def token_valid(token):
    url="https://api.telegram.org/bot"+token+"/getMe"
    try:
        response = urlopen(url)
        data = json.loads(response.read())
        if data['ok'] and token not in getTokenList():
            return True
        else:
            return False
    except:
        return False

def topic_used(txt):
    global bot_student
    for elem in bot_student:
        if bot_student[elem]["topic"]==txt:
            return True
    return False

def save_token(chat_id,txt):
    global bot_student
    global unconfirmed_bot
    global id_creation
    global tree
    bot=None
    try:
        if token_valid(txt):
            bot=telepot.Bot(txt)
            unconfirmed_bot[chat_id]["token"]=txt
        else:
            bot_creation.sendMessage(chat_id,"The token is already used or is not valid. Retry with another token. Please retry.",reply_markup=ReplyKeyboardRemove())
            return
    except:
        bot_creation.sendMessage(chat_id,"The token is already used or is not valid. Retry with another token. Please retry.",reply_markup=ReplyKeyboardRemove())
        return
    tree.createNode(unconfirmed_bot[chat_id]["topic"],True)
    pwd=randomStringwithDigitsAndSymbols()
    changePwdNotifier(pwd,unconfirmed_bot[chat_id]["topic"])
    create_hash(chat_id,pwd)
    bot_creation.sendMessage(chat_id,"This is the password to be enabled to answer questions: "+randomStringwithDigitsAndSymbols(),reply_markup=ReplyKeyboardRemove())
    bot_id=bot.getMe()['id']
    bot_student[bot_id]={}
    bot_student[bot_id]["bot"]=bot
    bot_student[bot_id]["token"]=txt
    bot_student[bot_id]["topic"]=unconfirmed_bot[chat_id]["topic"]
    bot_student[bot_id]["bot"].message_loop({'chat':student_message,'callback_query':student_query})
    write_bot(chat_id)
    del id_creation[chat_id]
    del unconfirmed_bot[chat_id]

def empty(msg):
    return

def write_bot(chat_id):
    result=database.put('/bots/students/'+unconfirmed_bot[chat_id]["topic"],name='token',data=unconfirmed_bot[chat_id]["token"])
    #data={}
    #with open("tokens.txt","r") as jfile:
        #data=json.load(jfile)
    #data["student"][unconfirmed_bot[chat_id]["topic"]]=unconfirmed_bot[chat_id]["token"]
    #with open("tokens.txt","w") as jfile:
        #json.dump(data,jfile)

def delPastCreation(chat_id):
    global unconfirmed_bot
    global id_creation
    global unc_del
    if chat_id in unconfirmed_bot:
        del unconfirmed_bot[chat_id]
    if chat_id in id_creation:
        del id_creation[chat_id]
    if chat_id in unc_del:
        del unc_del[chat_id]

def select_topic(chat_id,text):
    global tree
    global unconfirmed_bot
    global id_creation
    if not re.search("^[a-zA-Z0-9][a-zA-Z0-9 ]{3}[a-zA-Z0-9 ]*[a-zA-Z0-9]$", text):
        bot_creation.sendMessage(chat_id,"The name of the topic is not valid, it must have at least 5 characters and contain only letters, numbers and spaces. The name cannot begin or end with a space. Please retry",reply_markup=ReplyKeyboardRemove())
        return
    if text in getTopicList():
        bot_creation.sendMessage(chat_id,"The topic name has already been used. Please retry",reply_markup=ReplyKeyboardRemove())
        return
    unconfirmed_bot[chat_id]={}
    unconfirmed_bot[chat_id]["topic"]=text
    bot_creation.sendMessage(chat_id,"Paste the token created with the @BotFather bot:",reply_markup=ReplyKeyboardRemove())
    id_creation[chat_id]=2

def write_del_bot(topic):
    result=database.delete('/bots/students/'+topic,'token')
    #data={}
    #with open("tokens.txt","r") as jfile:
        #data=json.load(jfile)
    #del data["student"][topic]
    #with open("tokens.txt","w") as jfile:
        #json.dump(data,jfile)

def getIdByTopic(txt):
    global bot_student
    for elem in bot_student:
        if bot_student[elem]["topic"]==txt:
            return elem
    return None

def del_bot(topic):
    global bot_student
    bot_id=getIdByTopic(topic)
    if bot_id==None:
        return
    del bot_student[bot_id]
    write_del_bot(topic)

def cond_hash(chat_id,text):
    global tree
    global unc_del
    global id_creation
    if text=="Forgot password?":
        user=bot_creation.getChat(chat_id)
        bot_pwd.sendMessage(admin_pwd,"The user "+user['last_name']+" "+user['first_name']+" (@"+user['username']+") lost password for the topic "+unc_del[chat_id])
        bot_creation.sendMessage(chat_id,"A request was sent to the administrator",reply_markup=ReplyKeyboardRemove())
        del unc_del[chat_id]
        del id_creation[chat_id]
        return
    if boolvett[chat_id]:
        if verify_password(tree.getHash(unc_del[chat_id]), text):
            if str(chat_id) in banned_user:
                del banned_user[str(chat_id)]
            pwd=randomStringwithDigitsAndSymbols()
            changePwdNotifier(pwd,unc_del[chat_id])
            create_hash(chat_id,pwd,unc_del[chat_id])
            bot_creation.sendMessage(chat_id,"This is the password to be enabled to answer questions: "+pwd,reply_markup=ReplyKeyboardRemove())
        else :
            if str(chat_id) in banned_user:
                banned_user[str(chat_id)]+=1
            else:
                banned_user[str(chat_id)]=1
            bot_creation.sendMessage(chat_id,"Incorrect password. Command aborted.",reply_markup=ReplyKeyboardRemove())
        del unc_del[chat_id]
        del id_creation[chat_id]
    else:
        if verify_password(tree.getHash(unc_del[chat_id]), text):
            if str(chat_id) in banned_user:
                del banned_user[str(chat_id)]
            tree.deleteNode(unc_del[chat_id])
            del_bot(unc_del[chat_id])
            bot_creation.sendMessage(chat_id,"Topic deleted",reply_markup=ReplyKeyboardRemove())
        else :
            if str(chat_id) in banned_user:
                banned_user[str(chat_id)]+=1
            else:
                banned_user[str(chat_id)]=1
            bot_creation.sendMessage(chat_id,"Incorrect password. Command aborted.",reply_markup=ReplyKeyboardRemove())
        del unc_del[chat_id]
        del id_creation[chat_id]
    write_ban()

def choose_topic(chat_id,text):
    global unc_del
    global id_creation
    if topic_used(text):
        bot_creation.sendMessage(chat_id,"Enter the password relating to the topic:", reply_markup=createReplyKeyboard([["Forgot password?"]],only_one=False))
        unc_del[chat_id]=text
        id_creation[chat_id]=3
    else :
        bot_creation.sendMessage(chat_id,"Topic don't found, command aborted",reply_markup=ReplyKeyboardRemove())
        del id_creation[chat_id]

def switch_creation(chat_id,text):
    global id_creation
    if id_creation[chat_id]==1:
        select_topic(chat_id,text)
    elif id_creation[chat_id]==2:
        save_token(chat_id,text)
    elif id_creation[chat_id]==3:
        cond_hash(chat_id,text)
    elif id_creation[chat_id]==4:
        choose_topic(chat_id,text)

def creation_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    global unc_del
    global id_creation
    global admin_pwd
    chat_id=msg["message"]["chat"]["id"]
    if str(chat_id) in banned_user:
        if banned_user[str(chat_id)]>99:
            bot_creation.sendMessage(chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
            return
    if query_data=='s':
        bot_creation.sendMessage(chat_id,"Hi, this is the bot to create a new subject.", reply_markup=ReplyKeyboardRemove())
        bot_creation.sendMessage(chat_id,"Click on a command below:", reply_markup=key_cr)
        delPastCreation(chat_id)
    elif query_data=='n':
        bot_creation.sendMessage(chat_id,"Please select a new topic, please write the name in english:",reply_markup=ReplyKeyboardRemove())
        delPastCreation(chat_id)
        id_creation[chat_id]=1
    elif query_data=='d':
        bot_creation.sendMessage(chat_id,"Please select a topic:", reply_markup=topicKeyboard())
        delPastCreation(chat_id)
        id_creation[chat_id]=4
        boolvett[chat_id]=False
    elif query_data=='c':
        if not req_pwd(chat_id):
            bot_creation.sendMessage(chat_id,"You made too many requests, command aborted",reply_markup=ReplyKeyboardRemove())
            return
        bot_creation.sendMessage(chat_id,"Please select a topic:", reply_markup=topicKeyboard())
        delPastCreation(chat_id)
        id_creation[chat_id]=4
        boolvett[chat_id]=True

def createButton(topic):
    return InlineKeyboardButton(text=topic,callback_data=topic)

def topicKeyboard():
    data=[]
    for elem in bot_student:
        data.append([bot_student[elem]["topic"]])
    return createReplyKeyboard(data,only_one=False)

def creation_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    global  id_creation
    from_id=msg["from"]["id"]
    print(msg)
    if str(chat_id) in banned_user:
        if banned_user[str(chat_id)]>99:
            bot_creation.sendMessage(chat_id,"You are banned from this bot", reply_markup=topicKeyboard())
            return
    if content_type == 'text' and chat_type=="private":
        if msg["text"]=='/start':
            bot_creation.sendMessage(chat_id,"Hi, this is the bot to create a new subject.", reply_markup=ReplyKeyboardRemove())
            bot_creation.sendMessage(chat_id,"Click on a command below:", reply_markup=key_cr)
            delPastCreation(chat_id)
        elif msg["text"]=='/delete_bot':
            bot_creation.sendMessage(chat_id,"Please select a topic:", reply_markup=topicKeyboard())
            delPastCreation(chat_id)
            id_creation[chat_id]=4
            boolvett[chat_id]=False
        elif msg["text"]=='/new_bot':
            bot_creation.sendMessage(chat_id,"Please select a new topic, please write the name in english:", reply_markup=topicKeyboard())
            delPastCreation(chat_id)
            id_creation[chat_id]=1
        elif msg["text"]=='/change_pwd':
            if not req_pwd(chat_id):
                bot_creation.sendMessage(chat_id,"You made too many requests, command aborted", reply_markup=topicKeyboard())
                return
            bot_creation.sendMessage(chat_id,"Please select a topic:", reply_markup=topicKeyboard())
            delPastCreation(chat_id)
            id_creation[chat_id]=4
            boolvett[chat_id]=True
        elif chat_id in id_creation:
            switch_creation(chat_id,msg["text"])
        else :
            bot_creation.sendMessage(chat_id,"Unknown command or bot restarted.", reply_markup=topicKeyboard())

def createUrlButton(bot_id):
    return InlineKeyboardButton(text=bot_student[bot_id]["topic"],url="https://t.me/"+bot_student[bot_id]["bot"].getMe()["username"]+"?start=foo")

def createUrlInlineQuery():
    data=[]
    for elem in bot_student:
        data.append([createUrlButton(elem)])
    return  InlineKeyboardMarkup(inline_keyboard=data)

def link_message(msg):
    global bot_getlink
    content_type, chat_type, chat_id = telepot.glance(msg)
    if content_type == 'text' and chat_type=="private":
        if msg["text"]=='/start':
            bot_getlink.sendMessage(chat_id,"Select a bot:",reply_markup=createUrlInlineQuery())

def read_tokens():
    global database
    global lang_array
    data={}
    data["teacher"]=database.get('/bots/teachers/token','')
    stud_dict=database.get('/bots/students','')
    data["student"]={}
    for elem in stud_dict:
        data["student"][elem]=stud_dict[elem]["token"]
    data["admin"]={}
    data["admin"]["token"]=database.get('/bots/admin/token','')
    for lang in lang_array:
        data["admin"][lang]=database.get('/bots/admin/'+lang+'/ids','')
    data["creation"]=database.get('/bots/creation','')
    data["getlink"]=database.get('/bots/getlink','')
    data["pwd"]={}
    data["pwd"]["bot"]=database.get('/bots/pwd/bot','')
    data["pwd"]["admin"]=database.get('/bots/pwd/admin','')
    return data

def initialize():
    global bot_admin
    global bot_student
    global bot_teacher
    global bot_creation
    global bot_getlink
    global tree
    global admin_pwd
    global bot_pwd
    global user_request
    global tokens
    global bug_array
    bug_array=database.read_bug()
    user_request=database.read_pwd()
    banned_user=database.read_ban()
    data={}
    data=read_tokens()
    bot_admin=telepot.Bot(data["admin"]["token"])
    tokens.append(data["admin"]["token"])
    bot_admin.message_loop({'chat':empty,'callback_query':empty})
    print("admin: "+str(bot_admin.getMe()["id"]))
    for lang in lang_array:
        tree.addAdmins(lang,data["admin"][lang])
    bot_teacher=telepot.Bot(data["teacher"])
    tokens.append(data["teacher"])
    bot_teacher.message_loop({'chat':teacher_message,'callback_query':teacher_query})
    print("teacher: "+str(bot_teacher.getMe()["id"]))
    bot_creation=telepot.Bot(data["creation"])
    tokens.append(data["creation"])
    bot_creation.message_loop({'chat':creation_message,'callback_query':creation_query})
    print("creation: "+str(bot_creation.getMe()["id"]))
    bot_getlink=telepot.Bot(data["getlink"])
    tokens.append(data["getlink"])
    bot_getlink.message_loop({'chat':link_message,'callback_query':empty})
    print("link: "+str(bot_creation.getMe()["id"]))
    admin_pwd=int(data["pwd"]["admin"])
    bot_pwd=telepot.Bot(data["pwd"]["bot"])
    tokens.append(data["pwd"]["bot"])
    bot_pwd.message_loop({'chat':empty,'callback_query':empty})
    print("pwd: "+str(bot_pwd.getMe()["id"]))
    for elem in data["student"]:
        bot=None
        bot=telepot.Bot(data["student"][elem])
        bot_id=bot.getMe()['id']
        bot_student[bot_id]={}
        bot_student[bot_id]["bot"]=bot
        bot_student[bot_id]["topic"]=elem
        bot_student[bot_id]["token"]=data["student"][elem]
        bot_student[bot_id]["bot"].message_loop({'chat':student_message,'callback_query':student_query})
    sendNotification()
    print(type(bot_student))

if __name__=='__main__':
    initialize()
    print("Bot inizializzato")
    while True:
        time.sleep(10)
