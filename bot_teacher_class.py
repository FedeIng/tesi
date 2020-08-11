import telepot
from library import add_id, check_id, matchCommand, tagGroup, del_id, selection, list_to_str, array_to_matrix, createReplyKeyboard, seg_bug
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class BotTeacher:

    def __init__(self,token,tree):

        self.keyboard = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="/answer", callback_data='a')],[InlineKeyboardButton(text="/report", callback_data='r')],[InlineKeyboardButton(text="/start", callback_data='s')],[InlineKeyboardButton(text="/list", callback_data='l')],[InlineKeyboardButton(text="/free_list", callback_data='fl')],[InlineKeyboardButton(text="/ban", callback_data='b')],[InlineKeyboardButton(text="/ban_list", callback_data='bl')],[InlineKeyboardButton(text="/sban", callback_data='sb')],[InlineKeyboardButton(text="/change", callback_data='c')],[InlineKeyboardButton(text="/delete", callback_data='d')],[InlineKeyboardButton(text="/hints", callback_data='h')],[InlineKeyboardButton(text="/add_hint", callback_data='ah')]])

        def message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            topic=self.tree.getTopic(chat_id)
            user=self.bot.getChat(from_id)
            txt=msg["text"]
            if content_type == 'text' and self.verify_user(msg,chat_id,from_id,topic):
                lang=self.tree.getSuperUserLang(chat_id,topic)
                if matchCommand('/start',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=topic), reply_markup=ReplyKeyboardRemove(selective=True))
                    self.bot.sendMessage(chat_id, self.tree.getString(lang,"command"), reply_markup=self.keyboard)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/answer',txt,chat_type,self.bot.getMe()["username"]):
                    selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type,self.bot,self.tree.get_lang())
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,1)
                elif matchCommand('/ban',txt,chat_type,self.bot.getMe()["username"]):
                    selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type,self.bot,self.tree.get_lang())
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,3)
                elif matchCommand('/report',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,2)
                elif matchCommand('/list',txt,chat_type,self.bot.getMe()["username"]):
                    self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"ANSWER"),chat_type)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/ban_list',txt,chat_type,self.bot.getMe()["username"]):
                    self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"BANNED"),chat_type)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/free_list',txt,chat_type,self.bot.getMe()["username"]):
                    self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type)
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/sban',txt,chat_type,self.bot.getMe()["username"]):
                    selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"BANNED"),chat_type,self.bot,self.tree.get_lang())
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,5)
                elif matchCommand('/change',txt,chat_type,self.bot.getMe()["username"]):
                    selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"ANSWER"),chat_type,self.bot,self.tree.get_lang())
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,1)
                elif matchCommand('/delete',txt,chat_type,self.bot.getMe()["username"]):
                    self.tree.deleteTC(chat_id,self.node.get_topic_name())
                    self.bot.sendMessage(chat_id, "Permission deleted",reply_markup=ReplyKeyboardRemove())
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/hints',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+list_to_str(self.tree.getHint(topic,lang)),reply_markup=ReplyKeyboardRemove(selective=True))
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
                elif matchCommand('/add_hint',txt,chat_type,self.bot.getMe()["username"]):
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"select_hint"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,6)
                elif check_id(from_id,chat_id,self.id_commands) != 0:
                    self.switcher(chat_id,from_id,txt,lang,topic,chat_type)

        def query(msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
            chat_id=msg["message"]["chat"]["id"]
            chat_type=msg["message"]["chat"]["type"]
            topic=self.tree.getTopic(chat_id)
            user=self.bot.getChat(from_id)
            print(msg)
            if not self.verify_user(msg,chat_id,from_id,topic):
                return
            lang=self.tree.getSuperUserLang(chat_id,topic)
            if query_data=='s':
                self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+tree.getString(lang,"start",xxx=topic), reply_markup=ReplyKeyboardRemove(selective=True))
                self.bot.sendMessage(chat_id, self.tree.getString(lang,"command"), reply_markup=self.keyboard)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='a':
                selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type,self.bot,self.tree.get_lang())
                self.id_commands=add_id(from_id,chat_id,self.id_commands,1)
            elif query_data=='b':
                selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type,self.bot,self.tree.get_lang())
                self.id_commands=add_id(from_id,chat_id,self.id_commands,3)
            elif query_data=='r':
                self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"report"),reply_markup=ReplyKeyboardRemove(selective=True))
                self.id_commands=add_id(from_id,chat_id,self.id_commands,2)
            elif query_data=='l':
                self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"ANSWER"),chat_type)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='fl':
                self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"FREE"),chat_type)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='bl':
                self.list_sel(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"BANNED"),chat_type)
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='sb':
                selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"BANNED"),chat_type,self.bot,self.tree.get_lang())
                self.id_commands=add_id(from_id,chat_id,self.id_commands,5)
            elif query_data=='c':
                selection(chat_id,from_id,lang,self.tree.getResArray(topic,lang,"ANSWER"),chat_type,self.bot,self.tree.get_lang())
                self.id_commands=add_id(from_id,chat_id,self.id_commands,1)
            elif query_data=='d':
                self.tree.deleteTC(chat_id,topic)
                self.bot.sendMessage(chat_id, "Permission deleted",reply_markup=ReplyKeyboardRemove())
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='h':
                vett=self.tree.getHint(topic,lang)
                if vett!=[]:
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+list_to_str(vett),reply_markup=ReplyKeyboardRemove(selective=True))
                else:
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
                self.id_commands=del_id(from_id,chat_id,self.id_commands)
            elif query_data=='ah':
                hints=self.tree.getHint(topic,lang)
                if len(hints)>0:
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"select_hint"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
                    self.id_commands=add_id(from_id,chat_id,self.id_commands,6)
                else :
                    self.bot.sendMessage(chat_id, tagGroup(chat_type,user)+self.tree.getString(lang,"empty"),reply_markup=createReplyKeyboard(array_to_matrix(tree.getHint(topic,lang))))
                    self.id_commands=del_id(from_id,chat_id,self.id_commands)
        
        print("Token: "+token)
        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':message,'callback_query':query})
        self.tree=tree
        self.id_commands={}
        self.query_bool={}
        self.lang_bool={}
        self.query_bool={}
        self.prev_lang={}
        self.topic_name={}
        self.is_logged={}
        self.banned_user=self.tree.read_ban()
        self.tree.send_notification(self.bot)

    def list_sel(self,chat_id,from_id,lang,list1,chat_type):
        user=self.bot.getChat(from_id)
        if list1 ==[] :
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"empty"),reply_markup=ReplyKeyboardRemove(selective=True))
        else :
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+list_to_str(list1),reply_markup=ReplyKeyboardRemove(selective=True))

    def branch_one(self,msg,chat_id,from_id,topic):
        if self.tree.checkTeach(self.prev_lang[chat_id],msg["text"]):
            print("10")
            lang=self.prev_lang[chat_id]
            self.bot.sendMessage(chat_id, self.tree.getString(lang,"teacher"),reply_markup=ReplyKeyboardRemove())
            self.tree.addTeachers([chat_id],self.topic_name[chat_id],lang)
            del self.topic_name[chat_id]
            del self.prev_lang[chat_id]
        elif self.tree.checkColl(self.prev_lang[chat_id],msg["text"]):
            print("11")
            lang=self.prev_lang[chat_id]
            self.bot.sendMessage(chat_id, self.tree.getString(lang,"collaborator"),reply_markup=ReplyKeyboardRemove())
            self.tree.addCollaborators([chat_id],self.topic_name[chat_id],lang)
            del self.topic_name[chat_id]
            del self.prev_lang[chat_id]
        print("12")
        self.query_bool[chat_id]=False
        self.lang_bool[chat_id]=False

    def branch_two(self,msg,chat_id,from_id,topic):
        if msg["text"] in self.tree.get_flag_list():
            print("15")
            self.prev_lang[chat_id]=self.tree.switcherflag(msg["text"])
            self.bot.sendMessage(chat_id, self.tree.getString(self.prev_lang[chat_id],"roles"), reply_markup=self.tree.getLangBoard(self.prev_lang[chat_id],["teacher","collaborator"]))
            self.lang_bool[chat_id]=True
        print("16")

    def sub_branch_three(self,msg,chat_id,from_id,topic):
        lang_array=["it","de","en","es","fr"]
        if self.is_logged[chat_id]:
            print("20")
            if msg["text"] in self.tree.get_topic_list():
                print("21")
                self.bot.sendMessage(chat_id,"Copy/paste the password:",reply_markup=ReplyKeyboardRemove())
                self.topic_name[chat_id]=msg["text"]
                self.is_logged[chat_id]=False
                return False
        else:
            print("22")
            if self.tree.verify_password(self.topic_name[chat_id], msg["text"]):
                print("23")
                if chat_id in self.banned_user:
                    print("24")
                    del self.banned_user[chat_id]
                print("25")
                self.bot.sendMessage(chat_id,"Choose a language:",reply_markup=self.tree.setKeyboard(lang_array))
                self.query_bool[chat_id]=True
                self.tree.write_ban()
                return False
        return True

    def branch_three(self,msg,chat_id,from_id,topic):
        if chat_id in self.is_logged:
            print("19")
            if self.sub_branch_three(msg,chat_id,from_id,topic)==False:
                return False
            print("26")
            if chat_id in self.banned_user:
                print("27")
                self.banned_user[chat_id]+=1
            else:
                print("28")
                self.banned_user[chat_id]=1
            print("29")
            self.bot.sendMessage(chat_id,"Error, retry:",reply_markup=ReplyKeyboardRemove())
            self.bot.sendMessage(chat_id,"Please select the topic:",reply_markup=self.tree.topicKeyboard())
            self.is_logged[chat_id]=True
            self.tree.write_ban()
            if chat_id in self.topic_name:
                print("30")
                del self.topic_name[chat_id]
        else:
            print("31")
            self.bot.sendMessage(chat_id,"Please select the topic:",reply_markup=self.tree.topicKeyboard())
            self.is_logged[chat_id]=True
        print("32")

    def verify_user(self,msg,chat_id,from_id,topic):
        print("1")
        if chat_id in self.banned_user:
            print("2")
            if self.banned_user[chat_id]>99:
                print("3")
                self.bot.sendMessage(chat_id,"You are banned from this bot",reply_markup=ReplyKeyboardRemove())
                return False
        print("4")
        if chat_id not in self.lang_bool:
            print("5")
            self.lang_bool[chat_id]=False
        print("6")
        if chat_id not in self.query_bool:
            print("7")
            self.query_bool[chat_id]=False
        print("8")
        if self.lang_bool[chat_id]==True:
            print("9")
            self.branch_one(msg,chat_id,from_id,topic)
            return False
        print("13")
        if self.query_bool[chat_id]==True:
            print("14")
            self.branch_two(msg,chat_id,from_id,topic)
            return False
        print("17")
        if topic==None:
            print("18")
            self.branch_three(msg,chat_id,from_id,topic)
            return False
        return True

    def case1(self,chat_id,from_id,txt,lang,topic,chat_type):
        user=self.bot.getChat(from_id)
        res=self.tree.getResponse(txt,lang,topic)
        if res!=None:
            self.tree.setQID(chat_id,from_id,txt,topic)
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"answer",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
            self.id_commands=add_id(from_id,chat_id,self.id_commands,4)
            print("case 1 : "+str(self.id_commands))
        else:
            self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"error"),reply_markup=ReplyKeyboardRemove(selective=True))

    def case3(self,chat_id,from_id,txt,lang,topic,chat_type):
        user=self.bot.getChat(from_id)
        self.tree.setBan(txt,lang,topic)
        vett=self.tree.getIdsArray(topic,lang,txt)
        self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"banned_q",xxx=txt),reply_markup=ReplyKeyboardRemove(selective=True))
        for elem in vett:
            self.tree.get_bot_by_topic(topic).sendMessage(elem,self.tree.getString(lang,"banned_q",xxx=txt))
        self.id_commands=del_id(from_id,chat_id,self.id_commands)

    def case4(self,chat_id,from_id,txt,lang,topic,chat_type):
        print("case 4")
        user=self.bot.getChat(from_id)
        question=self.tree.setRes(chat_id,from_id,txt,lang,topic)
        if question==None:
            print("Oh no")
            return
        vett=self.tree.getIdsArray(topic,lang,question)
        print(str(vett))
        self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"answer_q",xxx=question,yyy=txt),reply_markup=ReplyKeyboardRemove(selective=True))
        for elem in vett:
            self.tree.get_bot_by_topic(topic).sendMessage(elem,self.tree.getString(lang,"answer_q",xxx=question,yyy=txt))
        self.id_commands=del_id(from_id,chat_id,self.id_commands)

    def case5(self,chat_id,from_id,txt,lang,topic,chat_type):
        user=self.bot.getChat(from_id)
        self.tree.setSban(txt,lang,topic)
        vett=self.tree.getIdsArray(topic,lang,txt)
        self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"banned_q",xxx=txt).replace("ban", "sban"),reply_markup=ReplyKeyboardRemove(selective=True))
        for elem in vett:
            self.tree.get_bot_by_topic(topic).sendMessage(elem,self.tree.getString(lang,"banned_q",xxx=txt).replace("ban", "sban"))
        self.id_commands=del_id(from_id,chat_id,self.id_commands)

    def case6(self,chat_id,from_id,txt,lang,topic,chat_type):
        user=self.bot.getChat(from_id)
        splitted=txt[1:-1].split("\" -> \"")
        self.tree.add_question_by_hint(lang,splitted[0],splitted[1],chat_id,from_id,topic)
        self.bot.sendMessage(chat_id,tagGroup(chat_type,user)+self.tree.getString(lang,"answer_q",xxx=splitted[0],yyy=splitted[1]),reply_markup=ReplyKeyboardRemove(selective=True))
        self.id_commands=del_id(from_id,chat_id,self.id_commands)

    def get_bot(self):
        return self.bot

    def switcher(self,chat_id,from_id,txt,lang,topic,chat_type):
        self.tree.set_nlp(lang)
        if check_id(from_id,chat_id,self.id_commands)==1:
            self.case1(chat_id,from_id,txt,lang,topic,chat_type)
        elif check_id(from_id,chat_id,self.id_commands)==2:
            seg_bug(chat_id,from_id,txt,lang,chat_type,"teachers",self.bot,self.tree.get_database(),self.tree.get_lang())
            self.id_commands=del_id(from_id,chat_id,self.id_commands)
        elif check_id(from_id,chat_id,self.id_commands)==3:
            self.case3(chat_id,from_id,txt,lang,topic,chat_type)
        elif check_id(from_id,chat_id,self.id_commands)==4:
            self.case4(chat_id,from_id,txt,lang,topic,chat_type)
        elif check_id(from_id,chat_id,self.id_commands)==5:
            self.case5(chat_id,from_id,txt,lang,topic,chat_type)
        elif check_id(from_id,chat_id,self.id_commands)==6:
            self.case6(chat_id,from_id,txt,lang,topic,chat_type)
