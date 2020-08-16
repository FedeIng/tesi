import telepot
import re
import hashlib, binascii, os
from urllib.request import urlopen
from library import createReplyKeyboard
import json
import datetime
import string
import random
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class BotCreation:

    def __init__(self,token,tree):
        self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/new_bot", callback_data='n')],[InlineKeyboardButton(text="/delete_bot", callback_data='d')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/change_pwd", callback_data='c')]])
        self.id_creation={}
        self.boolvett={}
        self.unconfirmed_bot={}
        self.unc_del={}
        self.user_request=tree.read_pwd()
        self.tree=tree
        self.banned_user=self.get_banned_dict()
        self.admin_pwd=self.tree.get_pwd_admin()
        self.select_str="Please select a topic:"
        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':self.message,'callback_query':self.query})

    def message(self,msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        if chat_id in self.banned_user and self.banned_user[chat_id]>99:
            self.bot.sendMessage(chat_id,"You are banned from this bot", reply_markup=self.tree.topicKeyboard())
            return
        if content_type == 'text' and chat_type=="private":
            if msg["text"]=='/start':
                self.bot.sendMessage(chat_id,"Hi, this is the bot to create a new subject.", reply_markup=ReplyKeyboardRemove())
                self.bot.sendMessage(chat_id,"Click on a command below:", reply_markup=self.keyboard)
                self.del_past_creation(chat_id)
            elif msg["text"]=='/delete_bot':
                self.bot.sendMessage(chat_id,self.select_str, reply_markup=self.tree.topicKeyboard())
                self.del_past_creation(chat_id)
                self.id_creation[chat_id]=4
                self.boolvett[chat_id]=False
            elif msg["text"]=='/new_bot':
                self.bot.sendMessage(chat_id,"Please select a new topic, please write the name in english:", reply_markup=self.tree.topicKeyboard())
                self.del_past_creation(chat_id)
                self.id_creation[chat_id]=1
            elif msg["text"]=='/change_pwd':
                if not self.req_pwd(chat_id):
                    self.bot.sendMessage(chat_id,"You made too many requests, command aborted", reply_markup=self.tree.topicKeyboard())
                    return
                self.bot.sendMessage(chat_id,self.select_str, reply_markup=self.tree.topicKeyboard())
                self.del_past_creation(chat_id)
                self.id_creation[chat_id]=4
                self.boolvett[chat_id]=True
            elif chat_id in self.id_creation:
                self.switch_creation(chat_id,msg["text"])
            else :
                self.bot.sendMessage(chat_id,"Unknown command or bot restarted.", reply_markup=self.tree.topicKeyboard())

    def query(self,msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
        chat_id=msg["message"]["chat"]["id"]
        if chat_id in self.banned_user and self.banned_user[chat_id]>99:
            self.bot.sendMessage(chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
            return
        if query_data=='s':
            self.bot.sendMessage(chat_id,"Hi, this is the bot to create a new subject.", reply_markup=ReplyKeyboardRemove())
            self.bot.sendMessage(chat_id,"Click on a command below:", reply_markup=self.keyboard)
            self.del_past_creation(chat_id)
        elif query_data=='n':
            self.bot.sendMessage(chat_id,"Please select a new topic, please write the name in english:",reply_markup=ReplyKeyboardRemove())
            self.del_past_creation(chat_id)
            self.id_creation[chat_id]=1
        elif query_data=='d':
            self.bot.sendMessage(chat_id,self.select_str, reply_markup=self.tree.topicKeyboard())
            self.del_past_creation(chat_id)
            self.id_creation[chat_id]=4
            self.boolvett[chat_id]=False
        elif query_data=='c':
            if not self.req_pwd(chat_id):
                self.bot.sendMessage(chat_id,"You made too many requests, command aborted",reply_markup=ReplyKeyboardRemove())
                return
            self.bot.sendMessage(chat_id,self.select_str, reply_markup=self.tree.topicKeyboard())
            self.del_past_creation(chat_id)
            self.id_creation[chat_id]=4
            self.boolvett[chat_id]=True

    def teach_board_topic(self,topic,chat_id):
        self.bot.sendMessage(chat_id,"If you want go to a bot",reply_markup=self.tree.get_creation_keyboard(topic))

    def delete_req(self,time,vett):
        data=[]
        for elem in vett:
            if time < elem:
                data.append(elem)
        return data

    def get_banned_dict(self):
        data={}
        for chat_id in self.user_request:
            data[chat_id]=len(self.user_request)
        return data

    def select_topic(self,chat_id,text):
        if not re.search("^[a-zA-Z0-9][a-zA-Z0-9 ]{3}[a-zA-Z0-9 ]*[a-zA-Z0-9]$", text):
            self.bot.sendMessage(chat_id,"The name of the topic is not valid, it must have at least 5 characters and contain only letters, numbers and spaces. The name cannot begin or end with a space. Please retry",reply_markup=ReplyKeyboardRemove())
            return
        if text in self.tree.get_topic_list():
            self.bot.sendMessage(chat_id,"The topic name has already been used. Please retry",reply_markup=ReplyKeyboardRemove())
            return
        self.unconfirmed_bot[chat_id]={}
        self.unconfirmed_bot[chat_id]["topic"]=text
        self.bot.sendMessage(chat_id,"Paste the token created with the @BotFather bot:",reply_markup=ReplyKeyboardRemove())
        self.id_creation[chat_id]=2

    def token_valid(self,token):
        url="https://api.telegram.org/bot"+token+"/getMe"
        try:
            response = urlopen(url)
            data = json.loads(response.read())
            if data['ok'] and token not in self.tree.getTokenList():
                return True
            else:
                return False
        except telepot.exception:
            return False

    def rand_string(self,string_length=10):
        password_characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(password_characters) for _ in range(string_length))

    def hash_password(self,password):
        """Hash a password for storing."""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), 
                                    salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')

    def save_token(self,chat_id,txt):
        try:
            if self.token_valid(txt):
                self.unconfirmed_bot[chat_id]["token"]=txt
            else:
                self.bot.sendMessage(chat_id,"The token is already used or is not valid. Retry with another token. Please retry.",reply_markup=ReplyKeyboardRemove())
                return
        except telepot.exception:
            self.bot.sendMessage(chat_id,"The token is already used or is not valid. Retry with another token. Please retry.",reply_markup=ReplyKeyboardRemove())
            return
        pwd=self.rand_string()
        self.bot.sendMessage(chat_id,"This is the password to be enabled to answer questions: "+pwd,reply_markup=ReplyKeyboardRemove())
        self.tree.new_bot(txt,self.unconfirmed_bot[chat_id]["topic"],self.hash_password(pwd))
        self.teach_board_topic(self.unconfirmed_bot[chat_id]["topic"],chat_id)
        del self.id_creation[chat_id]
        del self.unconfirmed_bot[chat_id]

    def cond_hash_first_branch(self,chat_id,text):
        if self.tree.verify_password(self.unc_del[chat_id], text):
            if chat_id in self.banned_user:
                del self.banned_user[chat_id]
            pwd=self.rand_string()
            self.tree.change_pwd(self.unc_del[chat_id],self.hash_password(pwd))
            bot_pwd=self.tree.get_bot_pwd()
            bot_pwd.sendMessage(self.admin_pwd,"The new password for the "+self.unc_del[chat_id]+" topic is "+pwd)
            self.bot.sendMessage(chat_id,"This is the password to be enabled to answer questions: "+pwd,reply_markup=ReplyKeyboardRemove())
            self.teach_board_topic(self.unc_del[chat_id],chat_id)
        else :
            if chat_id in self.banned_user:
                self.banned_user[chat_id]+=1
            else:
                self.banned_user[chat_id]=1
            self.bot.sendMessage(chat_id,"Incorrect password. Command aborted.",reply_markup=ReplyKeyboardRemove())
        del self.unc_del[chat_id]
        del self.id_creation[chat_id]

    def cond_hash_second_branch(self,chat_id,text):
        if self.tree.verify_password(self.unc_del[chat_id], text):
            if chat_id in self.banned_user:
                del self.banned_user[chat_id]
            self.tree.delete_bot(self.unc_del[chat_id])
            self.bot.sendMessage(chat_id,"Topic deleted",reply_markup=ReplyKeyboardRemove())
        else :
            if chat_id in self.banned_user:
                self.banned_user[chat_id]+=1
            else:
                self.banned_user[chat_id]=1
            self.bot.sendMessage(chat_id,"Incorrect password. Command aborted.",reply_markup=ReplyKeyboardRemove())
        del self.unc_del[chat_id]
        del self.id_creation[chat_id]

    def cond_hash(self,chat_id,text):
        if text=="Forgot password?":
            user=self.bot.getChat(chat_id)
            bot_pwd=self.tree.get_bot_pwd()
            bot_pwd.sendMessage(self.admin_pwd,"The user "+user['last_name']+" "+user['first_name']+" (@"+user['username']+") lost password for the topic "+self.unc_del[chat_id])
            self.bot.sendMessage(chat_id,"A request was sent to the administrator",reply_markup=ReplyKeyboardRemove())
            del self.unc_del[chat_id]
            del self.id_creation[chat_id]
            return
        if self.boolvett[chat_id]:
            self.cond_hash_first_branch(chat_id,text)
        else:
            self.cond_hash_second_branch(chat_id,text)
        #self.tree.write_ban()

    def choose_topic(self,chat_id,text):
        if text in self.tree.get_topic_list():
            self.bot.sendMessage(chat_id,"Enter the password relating to the topic:", reply_markup=createReplyKeyboard([["Forgot password?"]],only_one=False))
            self.unc_del[chat_id]=text
            self.id_creation[chat_id]=3
        else :
            self.bot.sendMessage(chat_id,"Topic don't found, command aborted",reply_markup=ReplyKeyboardRemove())
            del self.id_creation[chat_id]

    def switch_creation(self,chat_id,text):
        if self.id_creation[chat_id]==1:
            self.select_topic(chat_id,text)
        elif self.id_creation[chat_id]==2:
            self.save_token(chat_id,text)
        elif self.id_creation[chat_id]==3:
            self.cond_hash(chat_id,text)
        elif self.id_creation[chat_id]==4:
            self.choose_topic(chat_id,text)

    def req_pwd(self,chat_id):
        time=datetime.datetime.today()
        if chat_id not in self.user_request:
            self.user_request[chat_id]=[]
        self.user_request[chat_id]=self.delete_req(time,self.user_request[chat_id])
        self.user_request[chat_id].append(time+datetime.timedelta(days=30))
        self.tree.write_pwd(self.user_request)
        if len(self.user_request[chat_id]) > 10:
            return False
        return True

    def del_past_creation(self,chat_id):
        if chat_id in self.unconfirmed_bot:
            del self.unconfirmed_bot[chat_id]
        if chat_id in self.id_creation:
            del self.id_creation[chat_id]
        if chat_id in self.unc_del:
            del self.unc_del[chat_id]
