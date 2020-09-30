from node_class import Node
from language_class import Language
from library import array_to_matrix, create_reply_keyboard
import json
import telepot
import operator
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from bot_student_class import BotStudent 
from database_class import Database

class Tree:
    class Singleton:

        def __init__(self):
            self.lang=Language()
            self.array={}
            self.num=0
            self.database=Database()
            data=self.database.get('/bots/students','')
            for topic in data:
                self.array[topic]=BotStudent(topic)

        def set_super_user_lang(self,chat_id,topic,new_lang):
            self.array[topic].set_super_user_lang(chat_id,new_lang)

        def send_notification_teacher(self,bot):
            for topic in self.array:
                self.array[topic].send_notification(bot,self.lang)

        def read_ban(self):
            return self.database.read_ban()

        def get_lang(self):
            return self.lang

        def get_database(self):
            return self.database

        def check_lang_str(self,txt,string):
            return self.lang.check_lang_str(txt,string)

        def get_best_resp(self,txt,lang,topic):
            list1={}
            json_array=self.array[topic].get_json_array(self.lang,lang)
            for question in json_array:
                num=self.lang.calculate_similarity(txt,question,lang)
                if num>0.8:
                    list1[question]=num
            return self.normalize_vect(list1)

        def normalize_vect(self,vect):
            array = sorted(vect.items(), key=operator.itemgetter(1), reverse=True)
            i=0
            list1=[]
            for elem in array:
                if i==4:
                    break
                for e in elem:
                    list1.append(e)
                    break
                i+=1
            return list1

        def delete_bot(self,topic):
            self.database.del_bot(topic)
            del self.array[topic]

        def write_pwd(self,array):
            self.database.write_pwd(array)

        def get_banned_users(self):
            return self.database.get_banned_users()

        def get_username_by_topic(self,topic):
            return self.array[topic].get_username()

        def get_creation_keyboard(self,topic):
            return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Go to the teacher bot", url="https://t.me/"+self.database.get_bot_teacher().get_bot().getMe()["username"]+"?start=foo")],[InlineKeyboardButton(text="Go to the student "+topic+" bot", url="https://t.me/"+self.get_username_by_topic(topic)+"?start=foo")]])

        def read_pwd(self):
            return self.database.read_pwd()

        def change_pwd(self,topic,pwd):
            self.array[topic].change_pwd(pwd)

        def send_notification(self,teacher,student,topic):
            self.array[topic].sendRestartNotify(teacher,student,self.lang)

        def add_collaborators(self,vett,topic,lang):
            self.array[topic].add_collaborators(lang,vett)

        def change_role(self,chat_id,topic):
            return self.array[topic].change_role(chat_id)

        def get_hint(self,topic,lang):
            vett=[]
            for elem in ["it","de","en","es","fr"]:
                if elem != lang:
                    vett+=self.array[topic].get_trans_array(elem,lang)
            return vett

        def get_student_id(self):
            data={}
            for elem in self.array:
                vett=self.array[elem].get_student_id()
                if len(vett)>0:
                    data[elem]=vett
            return data

        def new_bot(self,token,topic,hash):
            self.database.new_topic(token,topic,hash)
            self.array[topic]=BotStudent(topic)

        def get_pwd_admin(self):
            return self.database.get_pwd_admin()

        def get_token_list(self):
            list1=[]
            for topic in self.array:
                list1.append(self.array[topic].get_token())
            return list1

        def get_topic_list(self):
            list1=[]
            for topic in self.array:
                list1.append(topic)
            return list1

        def get_flag_list(self):
            return self.lang.get_flag_list()

        def switcherflag(self,flag):
            return self.lang.get_lang_by_flag(flag)

        def set_student_id(self,vett):
            for elem in vett:
                self.array[elem].set_student_id(vett[elem])

        def verify_password(self,topic,password):
            return self.array[topic].verify_password(password)

        def add_question_by_hint(self,lang,question,response,chat_id,from_id,topic):
            self.set_question(question,lang,topic,chat_id)
            self.set_qid(chat_id,from_id,question,topic)
            self.set_res(chat_id,from_id,response,lang,topic)

        def topic_keyboard(self):
            return create_reply_keyboard(array_to_matrix(self.get_topic_list()))

        def delete_tc(self,chat_id,topic):
            self.array[topic].del_teachers([chat_id])
            self.array[topic].del_collaborators([chat_id])

        def add_teachers(self,vett,topic,lang):
            self.array[topic].add_teachers(lang,vett)

        def get_bot_by_topic(self,topic):
            return self.array[topic].get_bot()

        def get_bot_pwd(self):
            return self.database.get_bot_pwd().get_bot()

        def get_ids_array(self,topic,lang,txt):
            array=self.array[topic].get_json_array(lang)
            return array[txt]["ids"]

        def add_admins(self,lang,vett):
            self.lang.add_admins(lang,vett)

        def get_admins(self,lang):
            return self.lang.get_admins(lang)

        def set_hash(self,topic,hash):
            self.array[topic].set_hash(hash)
            self.write_data()

        def set_qid(self,chat_id,from_id,txt,topic):
            self.array[topic].set_qid(chat_id,from_id,txt)

        def get_hash(self,topic):
            return self.array[topic].get_hash()

        def get_sent(self,lang,text):
            return self.lang.question_sent(lang,text)

        def get_q_array(self,chat_id,lang,topic):
            list_q=self.array[topic].get_json_array(self.lang,lang,True)
            list_u=[]
            for elem in list_q:
                if chat_id in list_q[elem]["id"]:
                    list_u.append(elem)
            return list_u

        def get_qid(self,chat_id,from_id,topic):
            return self.array[topic].get_qid(chat_id,from_id)
        
        def del_qid(self,chat_id,from_id,topic):
            self.array[topic].del_qid(chat_id,from_id)

        def set_res(self,chat_id,from_id,txt,lang,topic):
            question=self.array[topic].get_qid(chat_id,from_id)
            if question != None:
                return self.array[topic].set_response(lang,question,txt)
            return None

        def set_ban(self,txt,lang,topic):
            jarray=self.array[topic].get_json_array(lang)
            e=self.lang.match_array(txt,lang,jarray)
            if e != None and jarray[e]["answer"]=="":
                self.array[topic].set_response(lang,e,"BANNED")
            self.array[topic].set_banned_stud()

        def set_sban(self,txt,lang,topic):
            jarray=self.array[topic].get_json_array(lang)
            e=self.lang.match_array(txt,lang,jarray)
            if e != None and jarray[e]["answer"]=="BANNED":
                self.array[topic].set_response(lang,e,"")
            self.array[topic].set_banned_stud()

        def set_nlp(self,lang):
            self.lang.set_nlp(lang)

        def set_lang_resp(self,id,lang,bot):
            self.lang.set_lang_resp(id,lang,bot)

        def add_id(self,from_id,chat_id,num,topic):
            return self.array[topic].add_id(from_id,chat_id,num)

        def get_res_array(self,topic,lang,condition):
            return self.array[topic].get_res_array(lang,condition)

        def check_id(self,from_id,chat_id,topic):
            return self.array[topic].check_id(from_id,chat_id)

        def del_id(self,from_id,chat_id,topic):
            return self.array[topic].del_id(from_id,chat_id)

        def get_topic(self,chat_id):
            for node in self.array:
                if chat_id in self.array[node].get_teach_coll():
                    return node
            return None

        def write_data(self):
            for elem in self.array:
                self.array[elem].set_formatted_data()

        def set_question(self,txt,lang,topic,chat_id):
            self.array[topic].add_question(txt,lang)
            self.array[topic].add_chat_id(txt,lang,chat_id)

        def get_response(self,txt,lang,topic,chat_id=None):
            json_array=self.array[topic].get_json_array(lang)
            val=0
            q=""
            for question in json_array:
                num=self.lang.calculate_similarity(txt,question,lang)
                if num > val:
                    val=num
                    q=question
            if val>0.8:
                if chat_id != None:
                    self.array[topic].add_chat_id(q,lang,chat_id)
                    self.write_data()
                return json_array[q]["answer"]
            else:
                return None

        def get_lang_board(self,lang,array):
            return self.lang.get_lang_board(lang,array)

        def set_keyboard(self,lang_array):
            return self.lang.set_keyboard(lang_array,False)

        def get_string(self, lang, string, xxx=None, yyy=None):
            return self.lang.get_string(lang,string,xxx,yyy)

        def get_user_lang(self,id,topic):
            return self.array[topic].getStudentLang(id)

        def get_super_user_lang(self,id,topic):
            return self.array[topic].get_toc_lang(id)

        def check_coll(self,lang,text):
            return self.lang.check_coll(lang,text)

        def check_teach(self,lang,text):
            return self.lang.check_teach(lang,text)
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Tree.instance:
            Tree.instance = Tree.Singleton()
        return Tree.instance