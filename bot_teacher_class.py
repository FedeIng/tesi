import telepot
from library import match_command, tag_group, selection, list_to_str, array_to_matrix, create_reply_keyboard, seg_bug, send_message, send_doc
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

from bot_id_class import BotId
from user_banned_class import UserBanned
from bot_class import Bot
from database_class import Database
from tree_class import Tree

class BotTeacher:
    class Singleton(Bot):

        def __init__(self):
            self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/free_list", callback_data='fl')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')],[InlineKeyboardButton(text="/sban", callback_data='sb')],[InlineKeyboardButton(text="/change", callback_data='c')],[InlineKeyboardButton(text="/delete", callback_data='d')],[InlineKeyboardButton(text="/hints", callback_data='h')],[InlineKeyboardButton(text="/add_hint", callback_data='ah')],[InlineKeyboardButton(text="/change_lang", callback_data='cl')],[InlineKeyboardButton(text="/change_role", callback_data='cr')]])
            self.tree=Tree()
            self.query_bool={}
            self.lang_bool={}
            self.query_bool={}
            self.prev_lang={}
            self.topic_name={}
            self.is_logged={}
            self.singleton_id=BotId()
            self.singleton_ban=UserBanned()
            super().__init__(Database().get_teacher(),self.message,self.query)
            self.tree.send_notification_teacher(super().get_bot())
            self.singleton_id.set_bot("teacher",super().get_bot())
            self.singleton_id.reset_key_id("teacher")

        def condition(self,content_type,msg,chat_id,from_id,topic):
            return content_type == 'text' and self.verify_user(msg,chat_id,from_id,topic)

        def start_command(self,txt,chat_type,lang,from_id,chat_id):
            return match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]) or (self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0 and self.tree.check_lang_str(txt,"canc"))

        def sub_message(self,chat_type,chat_id,from_id,topic,user):
            txt=msg["text"]
            lang=self.tree.get_super_user_lang(chat_id,topic)
            if self.start_command(txt,chat_type,lang,from_id,chat_id):
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.singleton_id.start_fun(chat_id,from_id,chat_type,lang,self.tree.get_lang(),"teacher",topic,self.keyboard)
            elif match_command('/answer',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,1,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif match_command('/ban',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,3,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif match_command('/report',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,2,"teacher")
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"report"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            elif match_command('/list',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"ANSWER"),chat_type)
            elif match_command('/ban_list',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"BANNED"),chat_type)
            elif match_command('/free_list',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type)
            elif match_command('/sban',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,5,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"BANNED"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif match_command('/change',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,1,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"ANSWER"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif match_command('/delete',txt,chat_type,super().get_bot().getMe()["username"]):
                self.tree.delete_tc(chat_id,topic)
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                send_message(super().get_bot(),chat_id, "Permission deleted",self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=ReplyKeyboardRemove())
            elif match_command('/hints',txt,chat_type,super().get_bot().getMe()["username"]):
                self.hints(chat_id,from_id,topic,lang,chat_type,user)
            elif match_command('/add_hint',txt,chat_type,super().get_bot().getMe()["username"]):
                self.add_hints(chat_id,from_id,topic,lang,chat_type,user)
            elif match_command('/change_lang',txt,chat_type,super().get_bot().getMe()["username"]):
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,7,"teacher")
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"lang"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=self.tree.set_keyboard(["it","de","en","es","fr"]))
            elif match_command('/change_role',txt,chat_type,super().get_bot().getMe()["username"]):
                role=self.tree.change_role(chat_id,topic)
                send_message(super().get_bot(),chat_id, self.tree.get_string(lang,role),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=ReplyKeyboardRemove())
                self.singleton_id.start_fun(chat_id,from_id,chat_type,lang,self.tree.get_lang(),"teacher",topic,self.keyboard)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher") != 0:
                self.switcher(chat_id,from_id,txt,lang,topic,chat_type)

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            topic=self.tree.get_topic(chat_id)
            user=super().get_bot().getChat(from_id)
            if self.condition(content_type,msg,chat_id,from_id,topic):
                self.sub_message(chat_type,chat_id,from_id,topic,user)
                

        def hints(self,chat_id,from_id,topic,lang,chat_type,user):
            self.tree.set_nlp(lang)
            vett=self.tree.get_hint(topic,lang)
            self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
            if vett!=[]:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+list_to_str(vett),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            else:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"empty"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)

        def add_hints(self,chat_id,from_id,topic,lang,chat_type,user):
            self.tree.set_nlp(lang)
            hints=self.tree.get_hint(topic,lang)
            if len(hints)>0:
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,6,"teacher")
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"select_hint"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=create_reply_keyboard(array_to_matrix(self.tree.get_hint(topic,lang))))
            else :
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"empty"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=create_reply_keyboard(array_to_matrix(self.tree.get_hint(topic,lang))))

        def query(self,msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
            chat_id=msg["message"]["chat"]["id"]
            chat_type=msg["message"]["chat"]["type"]
            topic=self.tree.get_topic(chat_id)
            user=super().get_bot().getChat(from_id)
            if not self.verify_user(msg,chat_id,from_id,topic):
                return
            lang=self.tree.get_super_user_lang(chat_id,topic)
            if query_data=='s':
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.singleton_id.start_fun(chat_id,from_id,chat_type,lang,self.tree.get_lang(),"teacher",topic,self.keyboard)
            elif query_data=='a':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,1,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif query_data=='b':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,3,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif query_data=='r':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,2,"teacher")
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"report"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            elif query_data=='l':
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"ANSWER"),chat_type)
            elif query_data=='fl':
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"FREE"),chat_type)
            elif query_data=='bl':
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.list_sel(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"BANNED"),chat_type)
            elif query_data=='sb':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,5,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"BANNED"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif query_data=='c':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,1,"teacher")
                selection(chat_id,from_id,lang,self.tree.get_res_array(topic,lang,"ANSWER"),chat_type,super().get_bot(),self.tree.get_lang(),self.singleton_id,"teacher")
            elif query_data=='d':
                self.tree.delete_tc(chat_id,topic)
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                send_message(super().get_bot(),chat_id, "Permission deleted",self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=ReplyKeyboardRemove())
            elif query_data=='h':
                self.hints(chat_id,from_id,topic,lang,chat_type,user)
            elif query_data=='ah':
                self.add_hints(chat_id,from_id,topic,lang,chat_type,user)
            elif query_data=='cl':
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,7,"teacher")
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"lang"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=self.tree.set_keyboard(["it","de","en","es","fr"]))
            elif query_data=='cr':
                role=self.tree.change_role(chat_id,topic)
                send_message(super().get_bot(),chat_id, self.tree.get_string(lang,role),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0,reply_markup=ReplyKeyboardRemove())
                self.singleton_id.start_fun(chat_id,from_id,chat_type,lang,self.tree.get_lang(),"teacher",topic,self.keyboard)
            
        def list_sel(self,chat_id,from_id,lang,list1,chat_type):
            user=super().get_bot().getChat(from_id)
            if list1 ==[] :
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"empty"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            else :
                reply=telepot.message_identifier(send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"File:",self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0))[1]
                send_doc(super().get_bot(),chat_id,list_to_str(list1),reply)

        def branch_one(self,msg,chat_id,from_id):
            lang=self.prev_lang[chat_id]
            topic=self.topic_name[chat_id]
            if self.tree.check_teach(lang,msg["text"]):
                send_message(super().get_bot(),chat_id, self.tree.get_string(lang,"teacher"),reply_markup=ReplyKeyboardRemove())
                self.tree.add_teachers([chat_id],self.topic_name[chat_id],lang)
                del self.topic_name[chat_id]
                del self.prev_lang[chat_id]
            elif self.tree.check_coll(lang,msg["text"]):
                send_message(super().get_bot(),chat_id, self.tree.get_string(lang,"collaborator"),reply_markup=ReplyKeyboardRemove())
                self.tree.add_collaborators([chat_id],self.topic_name[chat_id],lang)
                del self.topic_name[chat_id]
                del self.prev_lang[chat_id]
            self.singleton_id.start_fun(chat_id,from_id,"private",lang,self.tree.get_lang(),"teacher",topic,self.keyboard)
            self.query_bool[chat_id]=False
            self.lang_bool[chat_id]=False

        def branch_two(self,msg,chat_id,from_id,topic):
            if msg["text"] in self.tree.get_flag_list():
                self.prev_lang[chat_id]=self.tree.switcherflag(msg["text"])
                send_message(super().get_bot(),chat_id, self.tree.get_string(self.prev_lang[chat_id],"roles"),reply_markup=self.tree.get_lang_board(self.prev_lang[chat_id],["teacher","collaborator"]))
                self.lang_bool[chat_id]=True

        def sub_branch_three(self,msg,chat_id,from_id,topic):
            if self.is_logged[chat_id]:
                if msg["text"] in self.tree.get_topic_list():
                    send_message(super().get_bot(),chat_id,"Copy/paste the password:",reply_markup=ReplyKeyboardRemove())
                    self.topic_name[chat_id]=msg["text"]
                    self.is_logged[chat_id]=False
                    return False
            else:
                if self.tree.verify_password(self.topic_name[chat_id], msg["text"]):
                    self.singleton_ban.del_ban(chat_id)
                    send_message(super().get_bot(),chat_id,"Choose a language:",reply_markup=self.tree.set_keyboard(["it","de","en","es","fr"]))
                    self.query_bool[chat_id]=True
                    #self.tree.write_ban()
                    return False
            return True

        def branch_three(self,msg,chat_id,from_id,topic):
            if chat_id in self.is_logged:
                if self.sub_branch_three(msg,chat_id,from_id,topic)==False:
                    return False
                self.singleton_ban.add_ban(chat_id)
                send_message(super().get_bot(),chat_id,"Error, retry:",reply_markup=ReplyKeyboardRemove())
                send_message(super().get_bot(),chat_id,"Please select the topic:",reply_markup=self.tree.topic_keyboard())
                self.is_logged[chat_id]=True
                #self.tree.write_ban()
                if chat_id in self.topic_name:
                    del self.topic_name[chat_id]
            else:
                send_message(super().get_bot(),chat_id,"Please select the topic:",reply_markup=self.tree.topic_keyboard())
                self.is_logged[chat_id]=True

        def verify_user(self,msg,chat_id,from_id,topic):
            if self.singleton_ban.check_ban(chat_id):
                send_message(super().get_bot(),chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
                return False
            if chat_id not in self.lang_bool:
                self.lang_bool[chat_id]=False
            if chat_id not in self.query_bool:
                self.query_bool[chat_id]=False
            if self.lang_bool[chat_id]==True:
                self.branch_one(msg,chat_id,from_id)
                return False
            if self.query_bool[chat_id]==True:
                self.branch_two(msg,chat_id,from_id,topic)
                return False
            if topic==None:
                self.branch_three(msg,chat_id,from_id,topic)
                return False
            return True

        def case1(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            res=self.tree.get_response(txt,lang,topic)
            if res!=None:
                self.tree.set_qid(chat_id,from_id,txt,topic)
                self.singleton_id.add_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,4,"teacher")
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"answer",xxx=txt),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"error"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)

        def case3(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            self.tree.set_ban(txt,lang,topic)
            vett=self.tree.get_ids_array(topic,lang,txt)
            self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"banned_q",xxx=txt),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            for elem in vett:
                send_message(self.tree.get_bot_by_topic(topic),elem,self.tree.get_string(lang,"banned_q",xxx=txt),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)

        def case4(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            question=self.tree.set_res(chat_id,from_id,txt,lang,topic)
            if question==None:
                return
            vett=self.tree.get_ids_array(topic,lang,question)
            self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"answer_q",xxx=question,yyy=txt),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            for elem in vett:
                send_message(self.tree.get_bot_by_topic(topic),elem,self.tree.get_string(lang,"answer_q",xxx=question,yyy=txt),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)

        def case5(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            self.tree.set_sban(txt,lang,topic)
            vett=self.tree.get_ids_array(topic,lang,txt)
            self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id)
            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"banned_q",xxx=txt).replace("ban", "sban"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            for elem in vett:
                send_message(self.tree.get_bot_by_topic(topic),elem,self.tree.get_string(lang,"banned_q",xxx=txt).replace("ban", "sban"))

        def case6(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            splitted=txt[1:-1].split("\" -> \"")
            self.tree.add_question_by_hint(lang,splitted[0],splitted[1],chat_id,from_id,topic)
            self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.tree.get_string(lang,"answer_q",xxx=splitted[0],yyy=splitted[1]),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)

        def case7(self,chat_id,from_id,txt,lang,topic,chat_type):
            user=super().get_bot().getChat(from_id)
            txt=self.tree.switcherflag(txt)
            if txt==None:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(lang,"error"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
                return
            self.tree.set_super_user_lang(chat_id,topic,txt)
            send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.tree.get_string(txt,"setted_lang"),self.tree.get_string(lang,"canc"),self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")!=0)
            self.singleton_id.start_fun(chat_id,from_id,chat_type,txt,self.tree.get_lang(),"teacher",topic,self.keyboard)

        def get_bot(self):
            return super().get_bot()

        def switcher(self,chat_id,from_id,txt,lang,topic,chat_type):
            self.tree.set_nlp(lang)
            if self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==1:
                self.case1(chat_id,from_id,txt,lang,topic,chat_type)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==2:
                chat={"chat":chat_id,"from":from_id}
                bot={"bot":super().get_bot(),"type":"teachers"}
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                seg_bug(chat,txt,lang,chat_type,bot,self.tree.get_database(),self.tree.get_lang())
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==3:
                self.case3(chat_id,from_id,txt,lang,topic,chat_type)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==4:
                self.case4(chat_id,from_id,txt,lang,topic,chat_type)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==5:
                self.case5(chat_id,from_id,txt,lang,topic,chat_type)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==6:
                self.case6(chat_id,from_id,txt,lang,topic,chat_type)
            elif self.singleton_id.check_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")==7:
                self.singleton_id.del_time_id(chat_type,self.tree.get_lang(),lang,from_id,chat_id,"teacher")
                self.case7(chat_id,from_id,txt,lang,topic,chat_type)

    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotTeacher.instance:
            BotTeacher.instance = BotTeacher.Singleton()
        return BotTeacher.instance            
