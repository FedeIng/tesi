import telepot
from library import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from node_class import *

class BotStudent:

    def __init__(self,token,topic,database,lang_class):

        self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/question", callback_data='q')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/revision", callback_data='rv')],[InlineKeyboardButton(text="/change_lang", callback_data='cl')]])

        def message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            print(msg)
            txt=msg["text"]
            if content_type == 'text':
                user=self.bot.getChat(from_id)
                lang=self.getUserLang(chat_id)
                if lang==None and not check_id(from_id,chat_id,self.id_commands)==4:
                    self.set_lang(chat_id,from_id,msg['from']['language_code'],chat_type)
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,4)
                elif matchCommand('/start',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"start",xxx=self.node.get_topic_name()), reply_markup=ReplyKeyboardRemove(selective=True))
                    self.bot.sendMessage(chat_id, self.node.getString(lang,"command"), reply_markup=self.keyboard)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/question',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"question"),reply_markup=ReplyKeyboardRemove(selective=True))
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,5)
                elif matchCommand('/report',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,2)
                elif matchCommand('/revision',txt,chat_type,self.bot.getMe()["username"]):
                    selection(chat_id,from_id,lang,self.node.getResArray(lang,"ANSWER"),chat_type,self.bot,self.node.get_lang())
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,3)
                elif matchCommand('/change_lang',txt,chat_type,self.bot.getMe()["username"]):
                    self.set_lang(chat_id,from_id,lang,chat_type)
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,4)
                elif matchCommand('/list',txt,chat_type,self.bot.getMe()["username"]):
                    self.list_by_user(from_id,chat_id,lang,chat_type)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif check_id(from_id,chat_id,self.id_commands) != 0:
                    self.switcher(chat_id,from_id,msg["text"],lang,chat_type)

        def query(msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
            chat_id=msg["message"]["chat"]["id"]
            chat_type=msg["message"]["chat"]["type"]
            user=self.bot.getChat(from_id)
            lang=self.getUserLang(chat_id)
            if lang==None and not check_id(from_id,chat_id,self.id_commands)==4:
                self.set_lang(chat_id,from_id,msg['from']['language_code'],chat_type)
                self.id_commands=add_id(from_id,chat_id,self.id_commands,4)
            elif query_data=='s':
                self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"start",xxx=self.node.get_topic_name()), reply_markup=ReplyKeyboardRemove(selective=True))
                self.bot.sendMessage(chat_id, self.node.getString(lang,"command"), reply_markup=self.keyboard)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='q':
                self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"question"),reply_markup=ReplyKeyboardRemove(selective=True))
                self.id_commands=add_id(from_id,chat_id,self.id_commands,5)
            elif query_data=='r':
                self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
                self.id_commands=add_id(from_id,chat_id,self.id_commands,2)
            elif query_data=='rv':
                selection(chat_id,from_id,lang,self.node.getResArray(lang,"ANSWER"),chat_type,self.bot,self.node.get_lang())
                self.id_commands=add_id(from_id,chat_id,self.id_commands,3)
            elif query_data=='cl':
                self.set_lang(chat_id,from_id,lang,chat_type)
                self.id_commands=add_id(from_id,chat_id,self.id_commands,4)
            elif query_data=='l':
                self.list_by_user(chat_id,from_id,lang,chat_type)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)

        self.id_commands={}
        self.students=database.get_stud_ids(topic)
        print(self.students)
        self.teachers=database.get_teach_ids(topic)
        self.collaborators=database.get_coll_ids(topic)
        self.node=Node(topic,database,lang_class)
        self.bot=telepot.Bot(token)
        self.token=token
        self.bannedUser=database.get_banned_user(topic)
        self.bot.message_loop({'chat':message,'callback_query':query})

    def get_token(self):
        return self.token

    def get_username(self):
        return self.bot.getMe()["username"]

    def change_pwd(self,password):
        self.node.change_pwd(password)

    def verify_password(self,password):
        return self.node.verify_password(password)

    def getTeachColl(self):
        data=[]
        for lang in self.teachers:
            data+=self.teachers[lang]
        for lang in self.collaborators:
            data+=self.collaborators[lang]
        return data

    def getToCLang(self,id):
        for lang in self.collaborators:
            if id in self.collaborators[lang]:
                return lang
        for lang in self.teachers:
            if id in self.teachers[lang]:
                return lang
        return None

    def addTeachers(self,lang,array):
        for chat_id in array:
            if chat_id not in self.teachers[lang]:
                self.teachers[lang].append(chat_id)
                self.node.set_teach_ids(self.teachers[lang],self.node.get_topic_name(),lang)

    def addCollaborators(self,lang,array):
        for chat_id in array:
            if chat_id not in self.collaborators[lang]:
                self.collaborators[lang].append(chat_id)
                self.node.set_coll_ids(self.collaborators[lang],self.node.get_topic_name(),lang)

    def delTeachers(self,array):
        for chat_id in array:
            for lang in self.teachers:
                if chat_id in self.teachers[lang]:
                    self.teachers[lang].remove(chat_id)
                    self.node.set_teach_ids(self.teachers[lang],self.node.get_topic_name(),lang)

    def delCollaborators(self,array):
        for chat_id in array:
            for lang in self.collaborators:
                if chat_id in self.collaborators[lang]:
                    self.collaborators[lang].remove(chat_id)
                    self.node.set_coll_ids(self.collaborators[lang],self.node.get_topic_name(),lang)

    def getResArray(self,lang,condition):
        return self.node.getResArray(lang,condition)

    def send_notification(self,bot_teacher,lang_class):
        for lang in self.students:
            if lang in self.students:
                for stud in self.students[lang]:
                    print("Stud:"+str(stud))
                    self.bot.sendMessage(stud,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))
            if lang in self.teachers:
                for teach in self.teachers[lang]:
                    print("Teach:"+str(teach))
                    bot_teacher.sendMessage(teach,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))
            if lang in self.collaborators:
                for coll in self.collaborators[lang]:
                    print("Coll:"+str(coll))
                    bot_teacher.sendMessage(coll,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))

    def list_by_user(self,chat_id,from_id,lang,chat_type):
        user=self.bot.getChat(from_id)
        list1=self.node.getQArray(chat_id,lang)
        if list1 ==[] :
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.node.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
        else :
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+list_to_str(list1),reply_markup=ReplyKeyboardRemove(selective=True))

    def getTransArray(self,src,dst):
        return self.node.getTransArray(src,dst)

    def getUserLang(self,chat_id):
        for lang in self.students:
            if chat_id in self.students[lang]:
                return lang
        return None

    def setBannedUsers(self,lang):
        self.node.setBannedUsers(lang)

    def setResponse(self,lang,question,txt):
        return self.node.setResponse(lang,question,txt)

    def getJSONArray(self,lang):
        return self.node.getJSONArray(lang)

    def setQID(self,chat_id,from_id,txt):
        self.node.setQID(chat_id,from_id,txt)

    def getQID(self,chat_id,from_id):
        return self.node.getQID(chat_id,from_id)

    def set_lang(self,chat_id,from_id,lang,chat_type):
        user=self.bot.getChat(from_id)
        lang_array=self.get_lang_array()
        if len(lang_array)>0:
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"lang"),reply_markup=self.node.set_lang_keyboard(lang_array))
        else:
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"disable"),reply_markup=ReplyKeyboardRemove())

    def get_lang_array(self):
        data=[]
        lang_array=["it","de","en","es","fr"]
        for lang in lang_array:
            if lang in self.teachers or lang in self.collaborators:
                data.append(lang)
        return data

    def lang_teach_coll(self):
        data=[]
        for lang in self.teachers:
            data.append(lang)
        for lang in self.collaborators:
            if lang not in data:
                data.append(lang)
        return data

    def get_bot(self):
        return self.bot

    def match_speech(self,chat_id,from_id,txt,lang,chat_type):
        is_new=self.node.checkLangStr(txt,"new_q")
        print("Boolean : "+str(is_new))
        if not is_new:
            self.node.setQID(chat_id,from_id,txt)
        user=self.bot.getChat(from_id)
        elem=self.node.getQID(chat_id,from_id)
        response=None
        if not is_new:
            response=self.node.getResponse(elem,lang,chat_id)
        if response == None and lang in self.lang_teach_coll():
            print("1")
            self.node.setQuestion(elem,lang,chat_id)
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"q_not_found",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
            if lang in self.teachers:
                for teacher_id in self.teachers[lang]:
                    self.node.get_bot_teacher().get_bot().sendMessage(teacher_id, self.node.getString(lang,"new_q",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
        elif response == "BANNED":
            print("2")
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"banned_q",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
        elif response == "":
            print("3")
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"wait_q",xxx=elem),reply_markup=ReplyKeyboardRemove(selective=True))
        else:
            print("4")
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"answer_q",xxx=elem,yyy=response),reply_markup=ReplyKeyboardRemove(selective=True))
        self.node.delQID(chat_id,from_id)

    def seg_rev(self,chat_id,from_id,txt,lang,chat_type):
        user=self.bot.getChat(from_id)
        self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"revision",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
        response=self.node.getResponse(txt,lang)
        for teacher_id in self.teachers[lang]:
            if response != None and response != "" and lang in self.teachers:
                self.node.get_bot_teacher().get_bot().sendMessage(teacher_id, tagGroup(chat_type,user)+self.node.getString(lang,"revision",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
            else:
                self.node.get_bot_teacher().get_bot().sendMessage(teacher_id, tagGroup(chat_type,user)+self.node.getString(lang,"error"),reply_markup=ReplyKeyboardRemove(selective=True))

    def remove_stud_lang(self,chat_id):
        for lang in self.students:
            self.students[lang].remove(chat_id)

    def remove_coll_lang(self,chat_id):
        for lang in self.collaborators:
            self.collaborators[lang].remove(chat_id)

    def remove_teach_lang(self,chat_id):
        for lang in self.teachers:
            self.teachers[lang].remove(chat_id)

    def final_set(self,chat_id,from_id,txt,lang,chat_type):
        user=self.bot.getChat(from_id)
        txt=self.node.get_lang_by_flag(txt)
        if txt==None:
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"error"),reply_markup=ReplyKeyboardRemove(selective=True))
            return
        self.remove_stud_lang(chat_id)
        if txt not in self.students:
            self.students=[]
        self.students[txt].append(chat_id)
        self.node.write_stud_lang(self.students[lang],txt)
        self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(txt,"setted_lang"),reply_markup=ReplyKeyboardRemove(selective=True))

    def sel_question(self,chat_id,from_id,txt,lang,chat_type):
        list_val=self.node.getSent(lang,txt)
        print("List_q : "+str(list_val))
        user=self.bot.getChat(from_id)
        if len(list_val)!=1:
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"error_q"),reply_markup=ReplyKeyboardRemove(selective=True))
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
            return
        txt=list_val[0]
        BRes=self.node.getBestResp(txt,lang)
        print("array : "+str(BRes))
        self.node.setQID(chat_id,from_id,txt)
        if BRes==[]:
            print("1")
            self.match_speech(chat_id,from_id,self.node.getString(lang,"new_q"),lang,chat_type)
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif txt in BRes:
            print("2")
            self.match_speech(chat_id,from_id,txt,lang,chat_type)
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        else:
            print("3")
            BRes.append(self.node.getString(lang,"new_q"))
            self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.node.getString(lang,"select_q"),reply_markup=createReplyKeyboard(array_to_matrix(BRes)))
            self.id_commands=add_id(from_id,chat_id,self.id_commands,1)

    def switcher(self,chat_id,from_id,txt,lang,chat_type):
        self.node.set_nlp(lang)
        if check_id(from_id,chat_id,self.id_commands)==1:
            self.match_speech(chat_id,from_id,txt,lang,chat_type)
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif check_id(from_id,chat_id,self.id_commands)==2:
            seg_bug(chat_id,from_id,txt,lang,chat_type,"students",self.bot,self.node.get_database(),self.node.get_lang())
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif check_id(from_id,chat_id,self.id_commands)==3:
            self.seg_rev(chat_id,from_id,txt,lang,chat_type)
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif check_id(from_id,chat_id,self.id_commands)==4:
            self.final_set(chat_id,from_id,txt,lang,chat_type)
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif check_id(from_id,chat_id,self.id_commands)==5:
            self.sel_question(chat_id,from_id,txt,lang,chat_type)
