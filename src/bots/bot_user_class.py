import telepot
from library import match_command, tag_group, selection, list_to_str, array_to_matrix, create_reply_keyboard, seg_bug, send_message, send_doc

from bots.bot_class import Bot
from databases.database_class import Database

class BotUser:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="user"
            super().__init__(token,self.message,self.query)

        def start_command(self,txt,chat_type,lang,from_id,chat_id):
            return match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]) or (self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0 and self.node.check_lang_str(txt,"canc"))

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            if content_type == 'text':
                txt=msg["text"]
                user=super().get_bot().getChat(from_id)
                if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]):
                    send_message(super().get_bot(),chat_id,"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
                else:
                    status=super().get_status(self.bot_name,chat_id,from_id)
                    if status!=None:
                        match status.id:
                            case 1:
                                match txt:
                                    case "Vorrei vedere l'elenco dei giochi disponibili":
                                        pass
                                    case "Vorrei prendere un gioco":
                                        send_message(super().get_bot(),chat_id,"Che gioco vuoi prendere?")
                                        super().set_status(self.bot_name,chat_id,from_id,2,None)
                                    case _:
                                        send_message(super().get_bot(),chat_id,"Comando non trovato, si prega di rieseguire il comando start.")

        def query(self,msg):
            query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
            chat_id=msg["message"]["chat"]["id"]
            chat_type=msg["message"]["chat"]["type"]
            user=super().get_bot().getChat(from_id)
            lang=self.get_user_lang(chat_id)
            if lang==None and (not self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==4 or not txt in self.node.get_flag_list()):
                self.switch_lang(chat_id,from_id,msg,chat_type)
            elif chat_id in self.banned_user:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id,self.node.get_string(lang,"banned_user"))
            elif query_data=='s':
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.singleton.start_fun(chat_id,from_id,chat_type,lang,self.node.get_lang(),self.node.get_topic_name(),self.node.get_topic_name(),self.keyboard)
            elif query_data=='q':
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,5,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"question"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            elif query_data=='r':
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,2,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"report"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            elif query_data=='rv':
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,6,self.node.get_topic_name())
                selection(chat_id,from_id,lang,self.node.get_res_array(lang,"ANSWER"),chat_type,super().get_bot(),self.node.get_lang(),self.singleton,self.node.get_topic_name())
            elif query_data=='cl':
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,4,self.node.get_topic_name())
                self.set_lang(chat_id,from_id,lang,chat_type)
            elif query_data=='l':
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.list_by_user(chat_id,from_id,lang,chat_type)
            elif query_data=='ds':
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.del_students([chat_id])
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"delete_s"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)

        def add_question(self,question,lang):
            self.node.add_question(question,lang)

        def add_chat_id(self,question,lang,chat_id):
            self.node.add_chat_id(question,lang,chat_id)

        def change_role(self,chat_id):
            for lang in self.teachers:
                if chat_id in self.teachers[lang]:
                    self.del_collaborators([chat_id],False)
                    self.del_teachers([chat_id],False)
                    self.add_collaborators(lang,[chat_id],False)
                    self.node.set_teach_ids(self.collaborators[lang],lang)
                    return "collaborator"
            for lang in self.collaborators:
                if chat_id in self.collaborators[lang]:
                    self.del_collaborators([chat_id],False)
                    self.del_teachers([chat_id],False)
                    self.add_teachers(lang,[chat_id],False)
                    self.node.set_coll_ids(self.collaborators[lang],lang)
                    return "teacher"

        def set_super_user_lang(self,chat_id,new_lang):
            for lang in self.teachers:
                if chat_id in self.teachers[lang]:
                    self.del_collaborators([chat_id])
                    self.del_teachers([chat_id])
                    self.add_teachers(new_lang,[chat_id])
                    self.node.set_teach_ids(self.teachers[lang],lang)
                    return
            for lang in self.collaborators:
                if chat_id in self.collaborators[lang]:
                    self.del_collaborators([chat_id])
                    self.del_teachers([chat_id])
                    self.add_collaborators(new_lang,[chat_id])
                    self.node.set_coll_ids(self.collaborators[lang],lang)
                    return

        def switch_lang(self,chat_id,from_id,msg,chat_type):
            if "from" not in msg or "language_code" not in msg['from']:
                self.set_lang(chat_id,from_id,"en",chat_type)
            else:
                self.set_lang(chat_id,from_id,msg['from']['language_code'],chat_type)

        def get_token(self):
            return super().get_token()

        def get_username(self):
            return super().get_bot().getMe()["username"]

        def change_pwd(self,password):
            self.node.change_pwd(password)

        def verify_password(self,password):
            return self.node.verify_password(password)

        def get_teach_coll(self):
            data=[]
            for lang in self.teachers:
                data+=self.teachers[lang]
            for lang in self.collaborators:
                data+=self.collaborators[lang]
            return data

        def get_toc_lang(self,id):
            for lang in self.collaborators:
                if id in self.collaborators[lang]:
                    return lang
            for lang in self.teachers:
                if id in self.teachers[lang]:
                    return lang
            return None

        def send_new_lang_notification(self,lang):
            for lang_stud in self.students:
                for chat_id in self.students[lang_stud]:
                    send_message(super().get_bot(),chat_id,self.node.get_string(lang_stud,"new_lang",xxx=self.node.get_string(lang_stud,lang)),reply_markup=None)

        def add_teachers(self,lang,array,notification=True):
            if notification and (lang not in self.teachers or len(self.teachers[lang])==0) and (lang not in self.collaborators or len(self.collaborators[lang])==0):
                self.send_new_lang_notification(lang)
            if lang not in self.teachers or len(self.teachers[lang])==0:
                self.teachers[lang]=array
            else:
                for chat_id in array:
                    if chat_id not in self.teachers[lang]:
                        self.teachers[lang].append(chat_id)
            self.node.set_teach_ids(self.teachers[lang],lang)

        def add_collaborators(self,lang,array,notification=True):
            if notification and (lang not in self.teachers or len(self.teachers[lang])==0) and (lang not in self.collaborators or len(self.collaborators[lang])==0):
                self.send_new_lang_notification(lang)
            if lang not in self.collaborators or len(self.collaborators[lang])==0:
                self.collaborators[lang]=array
            else:
                for chat_id in array:
                    if chat_id not in self.collaborators[lang]:
                        self.collaborators[lang].append(chat_id)
            self.node.set_coll_ids(self.collaborators[lang],lang)

        def add_students(self,lang,array):
            if lang not in self.students or len(self.students[lang])==0:
                self.students[lang]=array
            else:
                for chat_id in array:
                    if chat_id not in self.students[lang]:
                        self.students[lang].append(chat_id)
            self.node.write_stud_lang(self.students[lang],lang)

        def send_del_lang_notification(self,lang):
            for lang_stud in self.students:
                for chat_id in self.students[lang_stud]:
                    send_message(super().get_bot(),chat_id,self.node.get_string(lang_stud,"del_lang",xxx=self.node.get_string(lang_stud,lang)),reply_markup=None)

        def del_teachers(self,array,notification=True):
            for chat_id in array:
                for lang in self.teachers:
                    while chat_id in self.teachers[lang]:
                        self.teachers[lang].remove(chat_id)
                        self.node.set_teach_ids(self.teachers[lang],lang)
                        if notification and (lang not in self.teachers or len(self.teachers[lang])==0) and (lang not in self.collaborators or len(self.collaborators[lang])==0):
                            self.send_del_lang_notification(lang)

        def del_collaborators(self,array,notification=True):
            for chat_id in array:
                for lang in self.collaborators:
                    while chat_id in self.collaborators[lang]:
                        self.collaborators[lang].remove(chat_id)
                        self.node.set_coll_ids(self.collaborators[lang],lang)
                        if notification and (lang not in self.teachers or len(self.teachers[lang])==0) and (lang not in self.collaborators or len(self.collaborators[lang])==0):
                            self.send_del_lang_notification(lang)

        def del_students(self,array):
            for chat_id in array:
                for lang in self.students:
                    while chat_id in self.students[lang]:
                        self.students[lang].remove(chat_id)
                        self.node.write_stud_lang(self.students[lang],lang)

        def get_res_array(self,lang,condition):
            return self.node.get_res_array(lang,condition)

        def send_not_stud(self,lang,lang_class):
            if lang in self.students:
                for stud in self.students[lang]:
                    send_message(super().get_bot(),stud,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))

        def send_not_teach(self,bot_teacher,lang,lang_class):
            if lang in self.teachers:
                for teach in self.teachers[lang]:
                    send_message(bot_teacher,teach,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))

        def send_not_coll(self,bot_teacher,lang,lang_class):
            if lang in self.collaborators:
                for coll in self.collaborators[lang]:
                    send_message(bot_teacher,coll,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove(selective=False))

        def send_notification(self,bot_teacher,lang_class):
            for lang in self.students:
                self.send_not_stud(lang,lang_class)
                self.send_not_teach(bot_teacher,lang,lang_class)
                self.send_not_coll(bot_teacher,lang,lang_class)

        def list_by_user(self,chat_id,from_id,lang,chat_type):
            user=super().get_bot().getChat(from_id)
            list1=self.node.get_q_array(chat_id,lang)
            if list1 ==[] :
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.node.get_string(lang,"empty"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            else :
                reply=telepot.message_identifier(send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"File:",self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0))[1]
                send_doc(super().get_bot(),chat_id,list_to_str(list1),reply)

        def get_trans_array(self,src,dst):
            return self.node.get_trans_array(src,dst)

        def get_user_lang(self,chat_id):
            for lang in self.students:
                if chat_id in self.students[lang]:
                    return lang
            return None

        def set_banned_stud(self):
            self.banned_user=self.node.set_banned_stud()

        def set_response(self,lang,question,txt):
            return self.node.set_response(lang,question,txt)

        def get_json_array(self,lang):
            return self.node.get_json_array(lang)

        def set_qid(self,chat_id,from_id,txt):
            self.node.set_qid(chat_id,from_id,txt)

        def get_qid(self,chat_id,from_id):
            return self.node.get_qid(chat_id,from_id)

        def set_lang(self,chat_id,from_id,lang,chat_type):
            user=super().get_bot().getChat(from_id)
            lang_array=self.get_lang_array()
            if len(lang_array)>0:
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,4,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"lang"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0,reply_markup=self.node.set_lang_keyboard(lang_array))
            else:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"disable"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0,reply_markup=ReplyKeyboardRemove())

        def get_lang_array(self):
            data=[]
            lang_array=["it","de","en","es","fr"]
            for lang in lang_array:
                if (lang in self.teachers and len(self.teachers[lang])>0) or (lang in self.collaborators and len(self.collaborators[lang])>0):
                    data.append(lang)
            return data

        def get_bot(self):
            return super().get_bot()

        def match_speech(self,chat_id,from_id,txt,lang,chat_type):
            is_new=self.node.check_lang_str(txt,"new_button")
            if not is_new:
                self.node.set_qid(chat_id,from_id,txt)
            user=super().get_bot().getChat(from_id)
            elem=self.node.get_qid(chat_id,from_id)
            response=None
            if not is_new:
                response=self.node.get_response(elem,lang)
            if response == None:
                self.node.set_question(elem,lang,chat_id)
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"q_not_found",xxx=elem),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
                if lang in self.teachers:
                    for teacher_id in self.teachers[lang]:
                        send_message(self.node.get_bot_teacher().get_bot(),teacher_id, self.node.get_string(lang,"new_q",xxx=elem),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            elif response == "BANNED":
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"banned_q",xxx=elem),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            elif response == "":
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"wait_q",xxx=elem),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            else:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"answer_q",xxx=elem,yyy=response),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            self.node.del_qid(chat_id,from_id)

        def new_seg_rev(self,question,lang,user,chat_type,from_id,chat_id):
            response=self.node.get_response(question,lang)
            if lang in self.teachers:
                for teacher_id in self.teachers[lang]:
                    if response != None and response != "" and lang in self.teachers:
                        send_message(self.node.get_bot_teacher().get_bot(),teacher_id, tag_group(chat_type,user)+self.node.get_string(lang,"revision",xxx=question),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)

        def old_seg_rev(self,question,lang,user,chat_type,from_id,chat_id):
            response=self.node.get_response(question,lang)
            if lang in self.teachers:
                for teacher_id in self.teachers[lang]:
                    if response != None and response != "" and lang in self.teachers:
                        send_message(self.node.get_bot_teacher().get_bot(),teacher_id, tag_group(chat_type,user)+self.node.get_string(lang,"revision",xxx=question)+" (\""+txt+"\")",self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)

        def seg_rev(self,chat_id,from_id,txt,lang,chat_type):
            question=self.node.get_qid(chat_id,from_id)
            self.node.del_qid(chat_id,from_id)
            user=super().get_bot().getChat(from_id)
            is_new=self.node.check_lang_str(txt,"comment") 
            if is_new:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"revision",xxx=question),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
                if not self.node.set_rv_comment(question,"",lang):
                    return
                self.new_seg_rev(question,lang,user,chat_type,from_id,chat_id)
            else:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"revision",xxx=question)+" (\""+txt+"\")",self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
                if not self.node.set_rv_comment(question,txt,lang):
                    return
                self.old_seg_rev(question,lang,user,chat_type,from_id,chat_id)

        def final_set(self,chat_id,from_id,txt,lang,chat_type):
            user=super().get_bot().getChat(from_id)
            txt=self.node.get_lang_by_flag(txt)
            if txt==None:
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"error"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
                return
            self.del_students([chat_id])
            self.add_students(txt,[chat_id])
            send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(txt,"setted_lang"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
            self.singleton.start_fun(chat_id,from_id,chat_type,txt,self.node.get_lang(),self.node.get_topic_name(),self.node.get_topic_name(),self.keyboard)

        def sel_question(self,chat_id,from_id,txt,lang,chat_type):
            list_val=self.node.get_sent(lang,txt)
            user=super().get_bot().getChat(from_id)
            print(list_val)
            if len(list_val)!=1:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"error_q"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)
                return
            txt=list_val[0].lower()
            bres=self.node.get_best_resp(txt,lang)
            self.node.set_qid(chat_id,from_id,txt)
            if bres==[]:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.match_speech(chat_id,from_id,self.node.get_string(lang,"new_button"),lang,chat_type)
            elif txt in bres:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.match_speech(chat_id,from_id,txt,lang,chat_type)
            else:
                bres.append(self.node.get_string(lang,"new_button"))
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,1,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"select_q"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0,reply_markup=create_reply_keyboard(array_to_matrix(bres)))

        def add_comment(self,chat_id,from_id,txt,lang,chat_type):
            user=super().get_bot().getChat(from_id)
            if txt in self.node.get_json_array(lang):
                self.node.set_qid(chat_id,from_id,txt)
                self.singleton.add_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,3,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"rv_comment"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0,reply_markup=create_reply_keyboard([[self.node.get_string(lang,"comment")]]))
            else:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                send_message(super().get_bot(),chat_id, tag_group(chat_type,user)+self.node.get_string(lang,"error_q"),self.node.get_string(lang,"canc"),self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())!=0)

        def switcher(self,chat_id,from_id,txt,lang,chat_type):
            self.node.set_nlp(lang)
            if self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==1:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.match_speech(chat_id,from_id,txt,lang,chat_type)
            elif self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==2:
                chat={"chat":chat_id,"from":from_id}
                bot={"bot":super().get_bot(),"type":"students"}
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                seg_bug(chat,txt,lang,chat_type,bot,self.node.get_database(),self.node.get_lang())
            elif self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==3:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.seg_rev(chat_id,from_id,txt,lang,chat_type)
            elif self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==4:
                self.singleton.del_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())
                self.final_set(chat_id,from_id,txt,lang,chat_type)
            elif self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==5:
                self.sel_question(chat_id,from_id,txt,lang,chat_type)
            elif self.singleton.check_time_id(chat_type,self.node.get_lang(),lang,from_id,chat_id,self.node.get_topic_name())==6:
                self.add_comment(chat_id,from_id,txt,lang,chat_type)
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUser.instance:
            BotUser.instance = BotUser.Singleton(token)
        return BotUser.instance 