import telepot
import re
import hashlib, binascii, os
from urllib.request import urlopen
from library import create_reply_keyboard, send_message
from urllib.error import HTTPError
import json
import datetime
import string
import random
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

from bot_id_class import BotId
from user_banned_class import UserBanned
from bot_class import Bot
from tree_class import Tree
from database_class import Database

class BotCreation:
    class Singleton(Bot):

        def __init__(self):
            self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/new_bot", callback_data='n')],[InlineKeyboardButton(text="/delete_bot", callback_data='d')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/change_pwd", callback_data='c')]])
            self.boolvett={}
            self.unconfirmed_bot={}
            self.unc_del={}
            self.tree=Tree()
            self.user_request=self.tree.read_pwd()
            self.admin_pwd=self.tree.get_pwd_admin()
            self.select_str="Please select a topic:"
            self.singleton_id=BotId()
            self.singleton_ban=UserBanned()
            super().__init__(Database().get_creation(),self.message,self.query)
            self.singleton_id.set_bot("creation",super().get_bot())
            self.singleton_id.reset_key_id("creation")

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if self.singleton_ban.check_ban(chat_id):
                send_message(super().get_bot(),chat_id,"You are banned from this bot","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                return
            if content_type == 'text' and chat_type=="private":
                if msg["text"]=='/start' or (self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0 and msg["text"]=="Cancel"):
                    self.del_past_creation(chat_id)
                    send_message(super().get_bot(),chat_id,"Hi, this is the bot to create a new subject.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                    self.singleton_id.set_key_id(telepot.message_identifier(send_message(super().get_bot(),chat_id,"Click on a command below:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.keyboard)),"creation")
                elif msg["text"]=='/delete_bot':
                    self.del_past_creation(chat_id)
                    self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,4,"creation")
                    send_message(super().get_bot(),chat_id,self.select_str,"Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                    self.boolvett[chat_id]=False
                elif msg["text"]=='/new_bot':
                    self.del_past_creation(chat_id)
                    self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,1,"creation")
                    send_message(super().get_bot(),chat_id,"Please select a new topic, please write the name in english:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                elif msg["text"]=='/change_pwd':
                    self.del_past_creation(chat_id)
                    if not self.req_pwd(chat_id):
                        send_message(super().get_bot(),chat_id,"You made too many requests, command aborted","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                        return
                    self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,4,"creation")
                    send_message(super().get_bot(),chat_id,self.select_str,"Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                    self.boolvett[chat_id]=True
                elif self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation") != 0:
                    self.switch_creation(chat_id,msg["text"])
                else :
                    send_message(super().get_bot(),chat_id,"Unknown command or bot restarted.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())

        def query(self,msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
            chat_id=msg["message"]["chat"]["id"]
            if self.singleton_ban.check_ban(chat_id):
                send_message(super().get_bot(),chat_id,"You are banned from this bot","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                return
            if query_data=='s':
                self.del_past_creation(chat_id)
                send_message(super().get_bot(),chat_id,"Hi, this is the bot to create a new subject.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                self.singleton_id.set_key_id(telepot.message_identifier(send_message(super().get_bot(),chat_id,"Click on a command below:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.keyboard)),"creation")
            elif query_data=='n':
                self.del_past_creation(chat_id)
                self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,1,"creation")
                send_message(super().get_bot(),chat_id,"Please select a new topic, please write the name in english:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
            elif query_data=='d':
                self.del_past_creation(chat_id)
                self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,4,"creation")
                send_message(super().get_bot(),chat_id,self.select_str,"Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                self.boolvett[chat_id]=False
            elif query_data=='c':
                self.del_past_creation(chat_id)
                if not self.req_pwd(chat_id):
                    send_message(super().get_bot(),chat_id,"You made too many requests, command aborted","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                    return
                self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,4,"creation")
                send_message(super().get_bot(),chat_id,self.select_str,"Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.topic_keyboard())
                self.boolvett[chat_id]=True

        def teach_board_topic(self,topic,chat_id):
            send_message(super().get_bot(),chat_id,"If you want go to a bot","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=self.tree.get_creation_keyboard(topic))

        def delete_req(self,time,vett):
            data=[]
            for elem in vett:
                if time < elem:
                    data.append(elem)
            return data

        def select_topic(self,chat_id,text):
            if not re.search("^[a-zA-Z0-9][a-zA-Z0-9 ]{3}[a-zA-Z0-9 ]*[a-zA-Z0-9]$", text):
                send_message(super().get_bot(),chat_id,"The name of the topic is not valid, it must have at least 5 characters and contain only letters, numbers and spaces. The name cannot begin or end with a space. Please retry","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                return
            if text in self.tree.get_topic_list():
                send_message(super().get_bot(),chat_id,"The topic name has already been used. Please retry","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                return
            self.unconfirmed_bot[chat_id]={}
            self.unconfirmed_bot[chat_id]["topic"]=text
            self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,2,"creation")
            send_message(super().get_bot(),chat_id,"Paste the token created with the @BotFather bot:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())

        def token_valid(self,token):
            url="https://api.telegram.org/bot"+token+"/getMe"
            #try:
            try:
                response = urlopen(url)
                data = json.loads(response.read())
                if data['ok'] and token not in self.tree.get_token_list():
                    return True
                else:
                    return False
            except HTTPError:
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

        def send_notify(self,chat_id,pwd,name_bot):
            bot_pwd=self.tree.get_bot_pwd()
            send_message(bot_pwd,self.admin_pwd,"The new password for the "+name_bot+" topic is "+pwd,self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0)
            send_message(super().get_bot(),chat_id,"This is the password to be enabled to answer questions: "+pwd,"Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())

        def save_token(self,chat_id,txt):
            #try:
            if self.token_valid(txt):
                self.unconfirmed_bot[chat_id]["token"]=txt
            else:
                send_message(super().get_bot(),chat_id,"The token is already used or is not valid. Retry with another token. Please retry.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                return
            #except telepot.exception:
                #send_message(super().get_bot(),chat_id,"The token is already used or is not valid. Retry with another token. Please retry.",reply_markup=ReplyKeyboardRemove())
                #return
            pwd=self.rand_string()
            self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
            self.send_notify(chat_id,pwd,self.unconfirmed_bot[chat_id]["topic"])
            self.tree.new_bot(txt,self.unconfirmed_bot[chat_id]["topic"],self.hash_password(pwd))
            self.teach_board_topic(self.unconfirmed_bot[chat_id]["topic"],chat_id)
            del self.unconfirmed_bot[chat_id]

        def cond_hash_first_branch(self,chat_id,text):
            self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
            if self.tree.verify_password(self.unc_del[chat_id], text):
                self.singleton_ban.del_ban(chat_id)
                pwd=self.rand_string()
                self.send_notify(chat_id,pwd,self.unc_del[chat_id])
                self.tree.change_pwd(self.unc_del[chat_id],self.hash_password(pwd))
                self.teach_board_topic(self.unc_del[chat_id],chat_id)
            else :
                self.singleton_ban.add_ban(chat_id)
                send_message(super().get_bot(),chat_id,"Incorrect password. Command aborted.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
            del self.unc_del[chat_id]

        def cond_hash_second_branch(self,chat_id,text):
            self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
            if self.tree.verify_password(self.unc_del[chat_id], text):
                self.singleton_ban.del_ban(chat_id)
                self.tree.delete_bot(self.unc_del[chat_id])
                send_message(super().get_bot(),chat_id,"Topic deleted","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
            else :
                self.singleton_ban.add_ban(chat_id)
                send_message(super().get_bot(),chat_id,"Incorrect password. Command aborted.","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
            del self.unc_del[chat_id]

        def cond_hash(self,chat_id,text):
            if text=="Forgot password?":
                user=super().get_bot().getChat(chat_id)
                bot_pwd=self.tree.get_bot_pwd()
                self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
                send_message(bot_pwd,self.admin_pwd,"The user "+user['last_name']+" "+user['first_name']+" (@"+user['username']+") lost password for the topic "+self.unc_del[chat_id],self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0)
                send_message(super().get_bot(),chat_id,"A request was sent to the administrator","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())
                del self.unc_del[chat_id]
                return
            if self.boolvett[chat_id]:
                self.cond_hash_first_branch(chat_id,text)
            else:
                self.cond_hash_second_branch(chat_id,text)
            #self.tree.write_ban()

        def choose_topic(self,chat_id,text):
            if text in self.tree.get_topic_list():
                self.singleton_id.add_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,3,"creation")
                send_message(super().get_bot(),chat_id,"Enter the password relating to the topic:","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=create_reply_keyboard([["Forgot password?"]],only_one=False))
                self.unc_del[chat_id]=text
            else :
                self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
                send_message(super().get_bot(),chat_id,"Topic don't found, command aborted","Cancel",self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")!=0,reply_markup=ReplyKeyboardRemove())

        def switch_creation(self,chat_id,text):
            if self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")==1:
                self.select_topic(chat_id,text)
            elif self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")==2:
                self.save_token(chat_id,text)
            elif self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")==3:
                self.cond_hash(chat_id,text)
            elif self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")==4:
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
            if self.singleton_id.check_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation") != 0:
                self.singleton_id.del_time_id("private",self.tree.get_lang(),"en",chat_id,chat_id,"creation")
            if chat_id in self.unc_del:
                del self.unc_del[chat_id]
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotCreation.instance:
            BotCreation.instance = BotCreation.Singleton()
        return BotCreation.instance
