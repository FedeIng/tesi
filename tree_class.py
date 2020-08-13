from node_class import Node
from language_class import Language
from library import *
import json
import telepot
import operator
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from bot_student_class import * 

class Tree:

    def __init__(self,database):
        print(1)
        self.lang=Language(database)
        print(2)
        self.array={}
        print(3)
        self.num=0
        print(4)
        self.database=database
        print(5)
        #with open(fileName,'r') as json_file:
            #data=json.load(json_file)
        data=database.get('/bots/students','')
        print(6)
        for topic in data:
            print("Begin bot "+topic)
            self.array[topic]=BotStudent(database.get_topic_token(topic),topic,database,self.lang)
            print("Bot "+topic+" created")
        #for down in data:
            #for up in data[down]:
                #node1=self.array[down]
                #if up not in self.array:
                    #self.create_node(up)
                #node2=self.array[up]
                #node1.addParent(node2)
                #node2.addSon(node1)
        #with open(authName,'r') as json_file:
            #data=json.load(json_file)
        #for elem in data:
            #self.array[elem].set_hash(data[elem]["hash"])
            #for lang in data[elem]:
                #if lang=="hash":
                    #continue
                #if "students" in data[elem][lang]:
                    #self.array[elem].addStudents(data[elem][lang]["students"],lang)
                #if "teachers" in data[elem][lang]:
                    #self.array[elem].add_teachers(data[elem][lang]["teachers"],lang,self.lang)
                #if "collaborators" in data[elem][lang]:
                    #self.array[elem].add_collaborators(data[elem][lang]["collaborators"],lang,self.lang)
        #self.setnum()
        #self.write_data()

    def send_notification(self,bot):
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

    def setnum(self):
        while "STATE"+str(self.num) in self.array:
            self.num+=1

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

    def set_choose_lang(self,topic):
        return self.lang.set_keyboard(self.array[topic].getLang(),True)

    def add_collaborators(self,vett,topic,lang):
        self.array[topic].add_collaborators(lang,vett)

    def get_hint(self,topic,lang):
        vett=[]
        for elem in ["it","de","en","es","fr"]:
            if elem != lang:
                vett+=self.array[topic].getTransArray(elem,lang)
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
        self.array[topic]=BotStudent(token,topic,self.database,self.lang)
        print("Bot "+topic+" created")

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
        self.array[topic].delTeachers([chat_id])
        self.array[topic].delCollaborators([chat_id])

    def add_teachers(self,vett,topic,lang):
        self.array[topic].add_teachers(lang,vett)

    def get_bot_by_topic(self,topic):
        return self.array[topic].get_bot()

    def get_bot_pwd(self):
        return self.database.get_bot_pwd().get_bot()

    def get_ids_array(self,topic,lang,txt):
        array=self.array[topic].get_json_array(lang)
        print(array)
        print(array[txt])
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

    def get_hash_list(self):
        hashlist=[]
        for node in self.array:
            hashlist.append(self.array[node].get_hash())
        return hashlist

    def get_hash(self,topic):
        return self.array[topic].get_hash()

    def contains(self,node,question,txt,lang):
        vett=node.get_json_array(self.lang,lang,False)
        e=''
        val=0
        val1=0
        for elem in vett:
            num=self.lang.calculate_similarity(question,elem,lang)
            num1=self.lang.calculate_similarity(txt,vett[elem]["answer"],lang)
            if (num+num1)/2 > (val+val1)/2:
                val=num
                val1=num1
                e=elem
        if val>0.8 and val1>0.8:
            return e
        else:
            return None

    def exist(self,vett):
        for node in self.array:
            sons=self.array[node].getArrays()[1]
            if len(sons)==2 and sons[0]==vett[0] and sons[1]==vett[1]:
                return node
        return None

    def get_sent(self,lang,text):
        return self.lang.question_sent(lang,text)

    def state_exist(self,node1,node2):
        p1=self.array[node1].getArrays()[0]
        p2=self.array[node2].getArrays()[0]
        for node in list(set(p1).intersection(p2)):
            if sorted(p1,p2)==node.getArrays()[1]:
                return node.getName(), True
        return None, False

    def normalize_tree(self,node1,node2):
        bool_var=False
        p,s=self.array[node1].getArrays()
        if len(p)==1 and len(s)==1:
            p[0].addSon(s[0])
            p[0].delSon(self.array[node1])
            s[0].addParent(p[0])
            s[0].delParent(self.array[node1])
            s[0].addJSON(self.array[node1],self.lang)
            del self.array[node1]
            bool_var=True
        p1,s1=self.array[node2].getArrays()
        if len(p1)==1 and len(s1)==1:
            p1[0].addSon(s1[0])
            p1[0].delSon(self.array[node2])
            s1[0].addParent(p1[0])
            s1[0].delParent(self.array[node2])
            s1[0].addJSON(self.array[node2],self.lang)
            del self.array[node2]
            bool_var=True
        if bool_var:
            return
        if len(p1)==len(list(set(p1).intersection(p))) and len(s1)==len(list(set(s1).intersection(s))) and len(p1)==len(p) and len(s1)==len(s):
            for elem in p1:
                elem.delSon(self.array[node2])
            for elem in s1:
                elem.delParent(self.array[node2])
            self.array[node1].addJSON(self.array[node2],self.lang)
            del self.array[node2]

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
            print("1")
            return self.array[topic].set_response(lang,question,txt)
        print("0")
        return None

    def set_ban(self,txt,lang,topic):
        jarray=self.array[topic].get_json_array(lang)
        e=self.match_array1(txt,lang,jarray)
        if e != None:
            if jarray[e]["answer"]=="":
                self.array[topic].set_response(lang,e,"BANNED")
        self.array[topic].set_bannedUsers(self.lang)
        #self.write_data()

    def set_sban(self,txt,lang,topic):
        jarray=self.array[topic].get_json_array(lang)
        e=self.match_array1(txt,lang,jarray)
        if e != None:
            if jarray[e]["answer"]=="BANNED":
                self.array[topic].set_response(lang,e,"")
        self.array[topic].set_bannedUsers(self.lang)
        #self.write_data()

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
            if chat_id in self.array[node].getTeachColl():
                return node
        return None

    def get_teacher_ids(self):
        teachers=[]
        for node in self.array:
            teachers+=self.array[node].getTeachColl()
        return teachers

    def bot_enabled(self,topic):
        if len(self.array[topic].getTeachColl())==0:
            return False
        return True

    def get_teachers_and_collaborators(self,topic):
        return self.array[topic].getLangTCArray()

    def get_res_id(self,lang,topic):
        return self.array[topic].getTeachers(lang)
        
    def match_array(self,txt,lang,vett):
        print(vett)
        e=''
        val=0
        for elem in vett:
            num=self.calculate_similarity(txt,elem,lang)
            if num > val:
                val=num
                e=elem
                print(elem)
        if val>0.8:
            return vett[e]
        else:
            return None

    def match_array1(self,txt,lang,vett):
        print(vett)
        e=''
        val=0
        for elem in vett:
            num=self.lang.calculate_similarity(txt,elem,lang)
            if num > val:
                val=num
                e=elem
                print(elem)
        if val>0.8:
            return e
        else:
            return None

    def write_data(self):
        for elem in self.array:
            self.array[elem].set_formatted_data()

    def set_question(self,txt,lang,topic,chat_id):
        self.array[topic].add_question(txt,lang)
        self.array[topic].add_chat_id(txt,lang,chat_id)
        self.write_data()

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

    def set_user_lang(self,id,lang,topic):
        self.array[topic].addStudents([id],lang)
        self.write_data()

    def get_string(self, lang, string, xxx=None, yyy=None):
        return self.lang.get_string(lang,string,xxx,yyy)

    def get_user_lang(self,id,topic):
        return self.array[topic].getStudentLang(id)

    def get_super_user_lang(self,id,topic):
        return self.array[topic].getToCLang(id)

    def delete_node(self,name):
        parents_array=self.array[name].getArrays()[0]
        if len(parents_array)>0:
            for parent in parents_array:
                name2=parent.getSecondSon(self.array[name])
                self.array[name2].setMergedArray(parent,self.lang)
                grandparents_array=parent.getArrays()[0]
                if len(grandparents_array)>0:
                    for grandparent in grandparents_array:
                        grandparent.delSon(parent)
                        grandparent.addSon(self.array[name])
                        self.array[name].addParent(grandparent)
                self.array[name].delParent(parent)
                del self.array[parent]
        del self.array[name]
        self.write_data()

    def check_coll(self,lang,text):
        return self.lang.check_coll(lang,text)

    def check_teach(self,lang,text):
        return self.lang.check_teach(lang,text)

    def create_node(self,new_name,w=False):
        if new_name in self.array:
            return False
        qa_array={}
        with open(self.dataName,'r') as json_file:
            qa_array=json.load(json_file)
        if new_name not in qa_array:
            qa_array[new_name]={}
        new_node=Node(new_name,qa_array[new_name])
        new_node.set_bannedUsers(self.lang)
        self.array[new_name]=new_node
        if w:
            self.write_data()
        return True

    def add_node(self,name1,name2,new_name):
        if name1 not in self.array or name2 not in self.array:
            return False
        if not self.create_node(new_name):
            return False
        node1=self.array[name1]
        node2=self.array[name2]
        new_node=self.array[new_name]
        node1.addParent(new_node)
        node2.addParent(new_node)
        new_node.addSon(node1)
        new_node.addSon(node2)
        self.write_data()
        return True

    def merge_node(self,name1,name2):
        node1=self.array[name1]
        node2=self.array[name2]
        if node1==node2:
            node1.substite(node2)
            del self.array[name1]
            return True
        return False

    def delete_link(self,name1,name2):
        node1=self.array[name1]
        node2=self.array[name2]
        if len(node1.getArrays()[0])==1 and len(node2.getArrays()[1])==1 and node1.isSon(node2) and node2.isParent(node1):
            node1.addParents(node2.getArrays()[0])
            node1.substite(node2)
            del self.array[name2]
            return True
        if len(node2.getArrays()[0])==1 and len(node1.getArrays()[1])==1 and node2.isSon(node1) and node1.isParent(node2):
            node2.addParents(node1.getArrays()[0])
            node2.substite(node1)
            del self.array[name1]
            return True
        return False
