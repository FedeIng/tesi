from language_class import Language
import json
import telepot
import operator
import hashlib, binascii, os
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Node:

    def __init__(self,node_name,database,lang_class):
        self.name=node_name
        self.json_array=database.get_questions_array(node_name)
        print(self.json_array)
        self.lang=lang_class
        self.questions={}
        self.hash=database.get_hash(node_name)
        self.database=database

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

    def set_teach_ids(self,array,topic,lang):
        self.database.set_teach_ids(array,topic,lang)

    def set_coll_ids(self,array,topic,lang):
        self.database.set_coll_ids(array,topic,lang)

    def get_topic_name(self):
        return self.name

    def get_json_array(self,lang):
        if lang not in self.json_array:
            return None
        return self.json_array[lang]

    def get_response(self,txt,lang):
        if lang in self.json_array:
            if txt in self.json_array[lang]:
                return self.json_array[lang][txt]
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
        for question in self.json_array:
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
        print("1")
        return self.lang.question_sent(lang,txt)

    def check_lang_str(self,txt,string):
        return self.lang.check_lang_str(txt,string)

    def set_nlp(self,lang):
        self.lang.set_nlp(lang)

    def get_lang_by_flag(self,flag):
        return self.lang.get_lang_by_flag(flag)

    def get_q_array(self,chat_id,lang):
        data=[]
        for elem in self.json_array[lang]:
            if chat_id in self.json_array[lang][elem]["ids"]:
                data.append(elem)
        return data

    def set_lang_keyboard(self,array):
        return self.lang.setKeyboard(array)

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

    def match_array(self,txt,lang,vett,lang_class):
        print(vett)
        e=''
        val=0
        for elem in vett:
            num=lang_class.calculate_similarity(txt,elem,lang)
            if num > val:
                val=num
                e=elem
                print(elem)
        if val>0.8:
            return e
        else:
            return None

    def get_real_node(self,lang,question,lang_class):
        if lang in self.json_array:
            elem=self.match_array(question,lang,self.json_array[lang],lang_class)
            if elem!=None:
                return self.name,elem
        for node in self.parents:
            node.get_real_node(lang,question,lang_class)
        return None,None

    def send_restart_notify(self,bot_t,bot_s,lang_class):
        for lang in self.teachers:
            for t in self.teachers[lang]:
                bot_t.sendMessage(t,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove())
        for lang in self.collaborators:
            for c in self.collaborators[lang]:
                bot_t.sendMessage(c,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove())
        for lang in self.students:
            for s in self.students[lang]:
                bot_s.sendMessage(s,lang_class.get_string(lang,"restart"),reply_markup=ReplyKeyboardRemove())

    def add_chat_id(self,question,lang,id):
        if lang in self.json_array:
            if question in self.json_array[lang]:
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

    def sub_set_banned_users(self,lang,lang_str,elem,users):
        if "answer" in self.json_array[lang_str][elem]:
            if self.json_array[lang_str][elem]["answer"]=="BANNED":
                for chat_id in self.json_array[lang_str][elem]["ids"]:
                    if chat_id in users:
                        users[chat_id]+=1
                    else:
                        users[chat_id]=1
        return users

    def set_banned_users(self,lang):
        users={}
        for lang_str in self.json_array:
            for elem in self.json_array[lang_str]:
                users=self.sub_set_banned_users(lang,lang_str,elem,users)
        for chat_id in users:
            if users[chat_id]>10:
                self.bannedUser.append(chat_id)
        
    def set_qid(self,chat_id,from_id,txt):
        if chat_id not in self.questions:
            self.questions[chat_id]={}
        self.questions[chat_id][from_id]=txt

    def set_response(self,lang,question,txt):
        print("Question : "+question)
        print("Lang : "+lang)
        print("Array : "+str(self.json_array))
        if lang not in self.json_array:
            print("2")
            return None
        if question not in self.json_array[lang]:
            print("3")
            return None
        self.json_array[lang][question]["answer"]=txt
        self.database.set_questions_array(self.json_array[lang],self.name,lang)
        print("4")
        return question

    def get_qid(self,chat_id,from_id):
        print("Chat_id : "+str(chat_id))
        print("From_id : "+str(from_id))
        print("Array : "+str(self.questions))
        if chat_id not in self.questions:
            print("1")
            return None
        if from_id not in self.questions[chat_id]:
            print("2")
            return None
        print("3")
        return self.questions[chat_id][from_id]

    def del_qid(self,chat_id,from_id):
        del self.questions[chat_id][from_id]
        if len(self.questions[chat_id])==0:
            del self.questions[chat_id]

    def get_lang_tc_array(self):
        data={}
        for lang in self.teachers:
            if lang not in data:
                data[lang]=[]
            data[lang]=self.teachers[lang]
        for lang in self.collaborators:
            if lang not in data:
                data[lang]=[]
            data[lang]+=self.collaborators[lang]
        return data
        
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
            if condition=="FREE" and self.json_array[lang][elem]["answer"]=='':
                data.append(elem)
            elif condition=="BANNED" and self.json_array[lang][elem]["answer"]=="BANNED":
                data.append(elem)
            elif condition=="ANSWER" and self.json_array[lang][elem]["answer"]!='' and self.json_array[lang][elem]["answer"]!="BANNED":
                data.append(elem)
        return data

    def get_teachers(self,lang):
        if lang in self.teachers:
            return self.teachers[lang]
        return []

    def get_banned_user(self):
        return self.bannedUser

    def get_array_lang(self):
        lang_vett=[]
        for elem in self.json_array:
            lang_vett.append(elem)
        print("Lang: "+str(lang_vett))
        return lang_vett

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

    def get_student_lang(self,id):
        for lang in self.students:
            if id in self.students[lang]:
                return lang
        return None
    
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

    def add_parent(self,node):
        self.parents.append(node)
    
    def add_son(self,node):
        self.sons.append(node)

    def del_son(self,node):
        self.sons.remove(node)

    def del_parent(self,node):
        self.parents.remove(node)

    def add_json(self,node,lang):
        for lang_str in ["it","de","en","es","fr"]:
            data={}
            data=node.get_json_array(lang,lang_str,recursive=False)
            if len(data)>0:
                if lang_str not in self.json_array:
                    self.json_array[lang]=data
                else:
                    self.json_array[lang].update(data)

    def ret_struct(self):
        data={}
        data["hash"]=self.hash
        for lang in self.teachers:
            if lang not in data:
                data[lang]={}
            data[lang]["teachers"]=self.teachers[lang]
        for lang in self.collaborators:
            if lang not in data:
                data[lang]={}
            data[lang]["collaborators"]=self.collaborators[lang]
        for lang in self.students:
            if lang not in data:
                data[lang]={}
            data[lang]["students"]=self.students[lang]
        return data

    def get_arrays(self):
        return sorted(self.parents), sorted(self.sons)

    def change(self,node1,node2):
        for num in range(0,len(self.sons)):
            if self.sons[num] == node1:
                self.sons[num] = node2
        for num in range(0,len(self.sons)):
            if self.parents[num] == node1:
                self.parents[num] = node2

    def get_name(self):
        return self.name

    def get_multiple_lang_array(self):
        return self.json_array

    def set_merged_array(self,obj,lang):
        data={}
        data1=obj.get_multiple_lang_array()
        for lang_str in self.json_array:
            data[lang_str]={}
            if lang not in data1:
                data[lang_str]=self.merge_arrays(self.json_array[lang_str],data1,lang,lang_str)
            else:
                data[lang_str]=self.json_array[lang_str]
        for lang_str in data1:
            if lang_str not in data:
                data[lang_str]=data1[lang_str]
        self.json_array=data

    def get_second_son(self,obj):
        for son in self.sons:
            if son != obj:
                return son
        return None

    def substite(self,obj):
        for son in self.sons:
            if son!=obj:
                son.change(self,obj)
        for parent in self.parents:
            if parent!=obj:
                parent.change(self,obj)

    def is_parent(self,obj):
        return obj in self.parents

    def del_parent(self,obj):
        self.parents.remove(obj)

    def del_son(self,obj):
        self.sons.remove(obj)

    def is_son(self,obj):
        return obj in self.sons

    def add_parents(self,array):
        self.parents=array

    def add_sons(self,array):
        self.sons=array

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
    
    def add_response(self,question,lang,txt):
        self.json_array[lang][question]["answer"]=txt
        
    def delete_question(self,question,lang):
        del self.json_array[lang][question]

    def sub_delete_double_question(self,lang,lang_str,data,elem):
        for question in data[elem]:
            vett=[]
            for question1 in self.json_array[lang_str]:
                if lang.calculate_similarity(question,question1,lang_str) > 0.8:
                    vett.append(question1)
            for question1 in vett:
                del self.json_array[lang_str][question1]

    def delete_double_question(self,lang,lang_str):
        if lang_str not in self.json_array:
            return
        data={}
        data=self.calc_distance(lang,lang_str)
        for elem in data:
            if elem==0:
                continue
            self.sub_delete_double_question(lang,lang_str,data,elem)
        return

    def add_question(self,txt,lang,res=""):
        if lang not in self.json_array:
            self.json_array[lang]={}
        self.json_array[lang][txt]={}
        self.json_array[lang][txt]["answer"]=res
        self.json_array[lang][txt]["ids"]=[]
        self.json_array[lang][txt]["code"]=len(self.json_array[lang])

    def cross_match(self,obj,lang,lang_str):
        tot={}
        tot[0]=0
        tot[1]=0
        num={}
        val={}
        if lang_str not in self.json_array:
            tot[0]=1.0
            tot[1]=1.0
            return tot
        l=len(self.json_array[lang_str])
        if l==0:
            tot[0]=1.0
            tot[1]=1.0
            return tot
        obj_array=obj.get_json_array(lang,lang_str,recursive=False)
        for elem in self.json_array[lang_str]:
            num[0]=0
            num[1]=0
            for elem1 in obj_array:
                val[0]=lang.calculate_similarity(elem,elem1,lang_str)
                val[1]=lang.calculate_similarity(self.json_array[lang_str][elem]['a'],obj_array[elem1]['a'],lang_str)
                for i in range(0,2):
                    if num[i]<val[i]:
                        num[i]=val[i]
            for i in range(0,2):
                tot[i]+=num[i]
        for i in range(0,2):
            tot[i]/=l
        return tot
    
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

    def cross_lang(self,obj,lang,lang_vett):
        for elem in lang_vett:
            vett=self.cross_match(obj,lang,elem)
            print(vett)
            for i in vett:
                if vett[i]< 0.8:
                    return False
        return True

    def get_lang(self):
        array=[]
        for elem in self.teachers:
            array.append(elem)
        for elem in self.collaborators:
            if elem not in array:
                array.append(elem)
        return sorted(array)

    def __eq__(self,obj):
        p1, s1 = self.get_arrays()
        p2, s2 = obj.get_arrays()
        if len(p1)!=len(p2) or len(s1)!=len(s2):
            return False
        for num in range(0,len(p1)):
            if p1[num]!=p2[num]:
                return False
        for num in range(0,len(s1)):
            if s1[num]!=s2[num]:
                return False
        return True

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

    def __ne__(self,obj):
        return not self==obj

    def __lt__(self,obj):
        return self.get_name() < obj.get_name()
    
    def __gt__(self,obj):
        return self.get_name() > obj.get_name()

    def __le__(self,obj):
        return self.get_name() <= obj.get_name()
    
    def __ge__(self,obj):
        return self.get_name() >= obj.get_name()

    def __de__(self):
        print("Nodo "+self.name+" eliminato")
