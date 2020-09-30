from language_class import Language
from database_class import Database
import json
import telepot
import operator
import hashlib, binascii, os
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Node:

    def __init__(self,node_name):
        self.name=node_name
        self.database=Database()
        self.json_array=self.database.get_questions_array(node_name)
        self.lang=Language()
        self.questions={}
        self.hash=self.database.get_hash(node_name)

    def verify_password(self,provided_password):
        stored_password=self.hash
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha512', 
                                    provided_password.encode('utf-8'), 
                                    salt.encode('ascii'), 
                                    100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password

    def change_pwd(self,password):
        self.hash=password
        self.database.set_new_pwd(self.name,password)

    def set_teach_ids(self,array,lang):
        self.database.set_teach_ids(array,self.name,lang)

    def set_coll_ids(self,array,lang):
        self.database.set_coll_ids(array,self.name,lang)

    def get_topic_name(self):
        return self.name

    def get_json_array(self,lang):
        if lang not in self.json_array:
            return None
        return self.json_array[lang]

    def get_response(self,txt,lang):
        if lang in self.json_array and txt in self.json_array[lang]:
            return self.json_array[lang][txt]["answer"]
        return None

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

    def get_best_resp(self,txt,lang):
        list1={}
        for question in self.json_array[lang]:
            num=self.lang.calculate_similarity(txt,question,lang)
            if num>0.8:
                list1[question]=num
        return self.normalize_vect(list1)

    def get_bot_teacher(self):
        return self.database.get_bot_teacher()

    def set_question(self,question,lang,chat_id):
        if lang not in self.json_array:
            self.json_array[lang]={}
        self.json_array[lang][question]={}
        self.json_array[lang][question]["ids"]=[chat_id]
        self.json_array[lang][question]["answer"]=""
        self.database.set_questions_array(self.json_array[lang],self.name,lang)

    def get_sent(self,lang,txt):
        return self.lang.question_sent(lang,txt)

    def check_lang_str(self,txt,string):
        return self.lang.check_lang_str(txt,string)

    def set_nlp(self,lang):
        self.lang.set_nlp(lang)

    def get_flag_list(self):
        return self.lang.get_flag_list()

    def get_lang_by_flag(self,flag):
        return self.lang.get_lang_by_flag(flag)

    def get_q_array(self,chat_id,lang):
        data=[]
        for elem in self.json_array[lang]:
            if chat_id in self.json_array[lang][elem]["ids"]:
                data.append(elem)
        return data

    def set_lang_keyboard(self,array):
        return self.lang.set_keyboard(array)

    def write_data(self):
        self.database.write_data()

    def write_stud_lang(self,students,lang):
        self.database.write_stud_lang(self.name,students,lang)

    def get_lang(self):
        return self.lang

    def get_database(self):
        return self.database

    def get_string(self,lang,string,xxx=None,yyy=None):
        return self.lang.get_string(lang,string,xxx,yyy)

    def get_questions_array(self,array):
        data={}
        lang_array=["it","de","en","es","fr"]
        for lang in lang_array:
            if lang in array:
                data[lang]=array[lang]["questions"]
        return data

    def get_real_node(self,lang,question,lang_class):
        if lang in self.json_array:
            elem=self.lang.match_array(question,lang,self.json_array[lang])
            if elem!=None:
                return self.name,elem
        for node in self.parents:
            node.get_real_node(lang,question,lang_class)
        return None,None

    def add_chat_id(self,question,lang,id):
        if lang in self.json_array and question in self.json_array[lang]:
            if id not in self.json_array[lang][question]["ids"]:
                self.json_array[lang][question]["ids"].append(id)
            return True
        for p in self.parents:
            if p.add_chat_id(question,lang,id):
                return True
        return False

    def set_student_id(self,vett):
        self.id_commands=vett

    def get_student_id(self):
        return self.id_commands

    def set_formatted_data(self):
        data={}
        data["banned"]=self.bannedUser
        data["hash"]=self.hash
        data["token"]=self.token
        lang_array=["it","de","en","es","fr"]
        for lang in lang_array:
            data[lang]={}
            if lang in self.students:
                data[lang]["students"]=self.students[lang]
            if lang in self.teachers:
                data[lang]["teachers"]=self.teachers[lang]
            if lang in self.collaborators:
                data[lang]["collaborators"]=self.collaborators[lang]
            data[lang]["questions"]=self.json_array[lang]
        self.database.put("/bots/students", name=self.node_name, data=data)

    def sub_set_banned_users(self,lang_str,elem,users):
        if "answer" in self.json_array[lang_str][elem] and self.json_array[lang_str][elem]["answer"]=="BANNED":
            for chat_id in self.json_array[lang_str][elem]["ids"]:
                if chat_id in users:
                    users[chat_id]+=1
                else:
                    users[chat_id]=1
        return users

    def set_banned_stud(self):
        users={}
        banned=[]
        for lang_str in self.json_array:
            for elem in self.json_array[lang_str]:
                users=self.sub_set_banned_users(lang_str,elem,users)
        for chat_id in users:
            if users[chat_id]>10:
                banned.append(chat_id)
        self.database.set_banned_stud(self.name,banned)
        return banned
        
    def set_qid(self,chat_id,from_id,txt):
        if chat_id not in self.questions:
            self.questions[chat_id]={}
        self.questions[chat_id][from_id]=txt

    def set_rv_comment(self,question,comment,lang):
        if lang not in self.json_array or question not in self.json_array[lang]:
            return False
        if "revision" not in self.json_array[lang][question]:
            self.json_array[lang][question]["revision"]=[]
        if self.lang.match_array(comment,lang,self.json_array[lang][question]["revision"]) == None:
            self.json_array[lang][question]["revision"].append(comment)
            self.database.set_questions_array(self.json_array[lang],self.name,lang)
            return True
        return False

    def set_response(self,lang,question,txt):
        if lang not in self.json_array:
            return None
        if question not in self.json_array[lang]:
            return None
        self.json_array[lang][question]["answer"]=txt
        self.database.set_questions_array(self.json_array[lang],self.name,lang)
        return question

    def get_qid(self,chat_id,from_id):
        if chat_id not in self.questions:
            return None
        if from_id not in self.questions[chat_id]:
            return None
        return self.questions[chat_id][from_id]

    def del_qid(self,chat_id,from_id):
        del self.questions[chat_id][from_id]
        if len(self.questions[chat_id])==0:
            del self.questions[chat_id]
        
    def get_ancestors(self):
        data=[]
        data.append(self)
        for elem in self.parents:
            data+=elem.get_ancestors()
        return data

    def get_heirs(self):
        data=[]
        data.append(self)
        for elem in self.sons:
            data+=elem.get_heirs()
        return data

    def get_teach_coll(self):
        data=[]
        for lang in self.teachers:
            data+=self.teachers[lang]
        for lang in self.collaborators:
            data+=self.collaborators[lang]
        return data
        
    def get_res_array(self,lang,condition):
        data=[]
        if lang not in self.json_array:
            return data
        for elem in self.json_array[lang]:
            if (condition=="FREE" and self.json_array[lang][elem]["answer"]=='') or (condition=="BANNED" and self.json_array[lang][elem]["answer"]=="BANNED") or (condition=="ANSWER" and self.json_array[lang][elem]["answer"]!='' and self.json_array[lang][elem]["answer"]!="BANNED"):
                data.append(elem)
        return data

    def sub_del_teachers(self,data,elem,lang,lang_class,bot):
        if elem not in self.teachers[lang] and len(self.teachers[lang])>0:
            data[lang]=self.teachers[lang]
        if elem in self.teachers[lang]:
            if len(self.teachers[lang])>1:
                data[lang]=[]
                for id in self.teachers[lang]:
                    if id!=elem:
                        data[lang].append(id)
            else:
                self.send_notification(lang_class,lang,bot,False)
        return data

    def del_teachers(self,vett,lang_class,bot):
        for elem in vett:
            data={}
            for lang in self.teachers:
                data=self.sub_del_teachers(data,elem,lang,lang_class,bot)
            self.teachers=data

    def sub_del_collaborators(self,data,elem,lang,lang_class,bot):
        if elem not in self.collaborators[lang] and len(self.collaborators[lang])>0:
            data[lang]=self.collaborators[lang]
        if elem in self.collaborators[lang]:
            if len(self.collaborators[lang])>1:
                data[lang]=[]
                for id in self.collaborators[lang]:
                    if id!=elem:
                        data[lang].append(id)
            else:
                self.send_notification(lang_class,lang,bot,False)
        return data

    def del_collaborators(self,vett,lang_class,bot):
        for elem in vett:
            data={}
            for lang in self.collaborators:
                data=self.sub_del_collaborators(data,elem,lang,lang_class,bot)
            self.collaborators=data
        
    def sub_del_students(self,data,elem,lang):
        if elem not in self.students[lang] and len(self.students[lang])>0:
            data[lang]=self.students[lang]
        if elem in self.students[lang] and len(self.students[lang])>1:
            data[lang]=[]
            for id in self.students[lang]:
                if id!=elem:
                    data[lang].append(id)
        return data

    def del_students(self,vett):
        for elem in vett:
            data={}
            for lang in self.students:
                data=self.sub_del_students(data,elem,lang)
            self.students=data

    def add_teachers(self,vett,lang_str,lang,bot=None):
        if bot != None:
            self.del_teachers(vett,lang,bot)
            self.del_collaborators(vett,lang,bot)
        if len(vett)==0:
            return
        if bot!=None:
            self.send_notification(lang,lang_str,bot)
        if lang_str not in self.teachers:
            self.teachers[lang_str]=[]
        for elem in vett:
            if elem not in self.teachers[lang_str]:
                self.teachers[lang_str].append(elem)

    def add_collaborators(self,vett,lang_str,lang,bot=None):
        if bot != None:
            self.del_teachers(vett,lang,bot)
            self.del_collaborators(vett,lang,bot)
        if len(vett)==0:
            return
        if bot!=None:
            self.send_notification(lang,lang_str,bot)
        if lang_str not in self.collaborators:
            self.collaborators[lang_str]=[]
        for elem in vett:
            if elem not in self.collaborators[lang_str]:
                self.collaborators[lang_str].append(elem)
    
    def add_students(self,vett,lang):
        self.del_students(vett)
        if len(vett)==0:
            return
        if lang not in self.students:
            self.students[lang]=[]
        for elem in vett:
            if elem not in self.students[lang]:
                self.students[lang].append(elem)
    
    def get_toc_lang(self,id):
        for lang in self.collaborators:
            if id in self.collaborators[lang]:
                return lang
        for lang in self.teachers:
            if id in self.teachers[lang]:
                return lang
        return None

    def set_hash(self,hash):
        self.hash=hash

    def get_hash(self):
        return self.hash

    def change(self,node1,node2):
        for num in range(0,len(self.sons)):
            if self.sons[num] == node1:
                self.sons[num] = node2
        for num in range(0,len(self.sons)):
            if self.parents[num] == node1:
                self.parents[num] = node2

    def is_in_array(self,string,array,lang,lang_str):
        for elem in array:
            if lang.calculate_similarity(string,elem,lang_str) > 0.8:
                return True
        return False

    def merge_arrays(self,array1,array2,lang,lang_str):
        if len(array1)==0:
            return array2
        data={}
        data=array1
        for elem in array2:
            val=[]
            for e_data in data:
                if lang.calculate_similarity(e_data,elem,lang_str) < 0.8:
                    val.append(elem)
            for e_val in val:
                data[e_val]=array2[e_val]
        return data

    def send_notification(self,lang,lang_str,bot,new=True):
        string=""
        if new:
            string="new_lang"
        else:
            string="del_lang"
        if (lang_str not in self.collaborators or len(self.collaborators[lang_str])==0) and (lang_str not in self.teachers or len(self.teachers[lang_str])==0):
            for elem in self.students:
                for chat_id in self.students[elem]:
                    bot.sendMessage(chat_id,lang.get_string(elem,string,xxx=lang.get_string(elem,lang_str)))

    def calc_distance(self,lang,lang_str):
        data={}
        if lang_str in self.json_array:
            data[0]=self.json_array[lang_str]
        for elem in self.parents:
            array=elem.calc_distance(lang_str)
            for num in array:
                if num+1 not in array:
                    data[num+1]={}
                data[num+1]=self.merge_arrays(data[num+1],array[num],lang,lang_str)
        return data

    def add_question(self,txt,lang,res=""):
        if lang not in self.json_array:
            self.json_array[lang]={}
        self.json_array[lang][txt]={}
        self.json_array[lang][txt]["answer"]=res
        self.json_array[lang][txt]["ids"]=[]
    
    def add_id(self,from_id,chat_id,num):
        if from_id==chat_id:
            self.id_commands[chat_id]=num
        else :
            if chat_id not in self.id_commands:
                self.id_commands[chat_id]={}
                self.id_commands[chat_id][from_id]=num
            else :
                self.id_commands[chat_id][from_id]=num

    def del_id(self,from_id,chat_id):
        if from_id==chat_id:
            if chat_id in self.id_commands:
                del self.id_commands[chat_id]
        else :
            if chat_id in self.id_commands and from_id in self.id_commands[chat_id]:
                del self.id_commands[chat_id][from_id]
            if len(self.id_commands[chat_id])==0:
                del self.id_commands[chat_id]

    def check_id(self,from_id,chat_id):
        ret_val=0
        if from_id==chat_id:
            if chat_id in self.id_commands:
                ret_val=self.id_commands[chat_id]
        else :
            if chat_id in self.id_commands and from_id in self.id_commands[chat_id]:
                ret_val=self.id_commands[chat_id][from_id]
        return ret_val

    def ret_q_vett(self,lang):
        vett=[]
        if lang in self.json_array:
            vett=self.json_array[lang]
        return vett

    def get_trans_array(self,src,dst):
        vett=self.ret_q_vett(src)
        vett1=self.ret_q_vett(dst)
        array=[]
        for elem in vett:
            string=self.lang.translate(elem,src,dst)
            if vett[elem]["answer"] != "BANNED" and vett[elem]["answer"] != "" and not self.is_in_array(string,vett1,self.lang,dst):
                string="\""+string+"\" -> \""+self.lang.translate(vett[elem]["answer"],src,dst)+"\""
                array.append(string)
        return array
