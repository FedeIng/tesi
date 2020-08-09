from language_class import Language
import json
import telepot
import operator
import hashlib, binascii, os
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Node:

    def __init__(self,nodeName,database,lang_class):
        self.name=nodeName
        self.JSON_array=database.get_questions_array(nodeName)
        print(self.JSON_array)
        self.lang=lang_class
        self.questions={}
        self.hash=database.get_hash(nodeName)
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

    def getJSONArray(self,lang):
        if lang not in self.JSON_array:
            return None
        return self.JSON_array[lang]

    def getResponse(self,txt,lang):
        if lang in self.JSON_array:
            if txt in self.JSON_array[lang]:
                return self.JSON_array[lang][txt]
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

    def getBestResp(self,txt,lang):
        list1={}
        for question in self.JSON_array:
            num=self.lang.calculate_similarity(txt,question,lang)
            if num>0.8:
                list1[question]=num
        return self.normalize_vect(list1)

    def get_bot_teacher(self):
        return self.database.get_bot_teacher()

    def setQuestion(self,question,lang,chat_id):
        if lang not in self.JSON_array:
            self.JSON_array[lang]={}
        self.JSON_array[lang][question]={}
        self.JSON_array[lang][question]["ids"]=[chat_id]
        self.JSON_array[lang][question]["answer"]=""
        self.database.set_questions_array(self.JSON_array[lang],self.name,lang)

    def getSent(self,lang,txt):
        print("1")
        return self.lang.question_sent(lang,txt)

    def checkLangStr(self,txt,string):
        return self.lang.checkLangStr(txt,string)

    def set_nlp(self,lang):
        self.lang.set_nlp(lang)

    def get_lang_by_flag(self,flag):
        return self.lang.get_lang_by_flag(flag)

    def getQArray(self,chat_id,lang):
        data=[]
        for elem in self.JSON_array[lang]:
            if chat_id in self.JSON_array[lang][elem]["ids"]:
                data.append(elem)
        return data

    def set_lang_keyboard(self,array):
        return self.lang.setKeyboard(array)

    def writeData(self):
        self.database.writeData()

    def write_stud_lang(self,students,lang):
        self.database.write_stud_lang(self.name,students,lang)

    def get_lang(self):
        return self.lang

    def get_database(self):
        return self.database

    def getString(self,lang,string,xxx=None,yyy=None):
        return self.lang.getString(lang,string,xxx,yyy)

    def get_questions_array(self,array):
        data={}
        lang_array=["it","de","en","es","fr"]
        for lang in lang_array:
            if lang in array:
                data[lang]=array[lang]["questions"]
        return data

    def matchArray(self,txt,lang,vett,lang_class):
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

    def getrealnode(self,lang,question,lang_class):
        if lang in self.JSON_array:
            elem=self.matchArray(question,lang,self.JSON_array[lang],lang_class)
            if elem!=None:
                return self.name,elem
        for node in self.parents:
            node.getrealnode(lang,question,lang_class)
        return None,None

    def sendRestartNotify(self,bot_t,bot_s,lang_class):
        for lang in self.teachers:
            for t in self.teachers[lang]:
                bot_t.sendMessage(t,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove())
        for lang in self.collaborators:
            for c in self.collaborators[lang]:
                bot_t.sendMessage(c,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove())
        for lang in self.students:
            for s in self.students[lang]:
                bot_s.sendMessage(s,lang_class.getString(lang,"restart"),reply_markup=ReplyKeyboardRemove())

    def add_chat_id(self,question,lang,id):
        if lang in self.JSON_array:
            if question in self.JSON_array[lang]:
                if id not in self.JSON_array[lang][question]["ids"]:
                    self.JSON_array[lang][question]["ids"].append(id)
                return True
        for p in self.parents:
            if p.add_chat_id(question,lang,id):
                return True
        return False

    def setstudentID(self,vett):
        self.id_commands=vett

    def getstudentID(self):
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
            data[lang]["questions"]=self.JSON_array[lang]
        self.database.put("/bots/students", name=self.nodeName, data=data)


    def setBannedUsers(self,lang):
        users={}
        for lang_str in self.JSON_array:
            for elem in self.JSON_array[lang_str]:
                if "answer" in self.JSON_array[lang_str][elem]:
                    if self.JSON_array[lang_str][elem]["answer"]=="BANNED":
                        for chat_id in self.JSON_array[lang_str][elem]["ids"]:
                            if chat_id in users:
                                users[chat_id]+=1
                            else:
                                users[chat_id]=1
        for chat_id in users:
            if users[chat_id]>10:
                self.bannedUser.append(chat_id)
        
    def setQID(self,chat_id,from_id,txt):
        if chat_id not in self.questions:
            self.questions[chat_id]={}
        self.questions[chat_id][from_id]=txt

    def setResponse(self,lang,question,txt):
        print("Question : "+question)
        print("Lang : "+lang)
        print("Array : "+str(self.JSON_array))
        if lang not in self.JSON_array:
            print("2")
            return None
        if question not in self.JSON_array[lang]:
            print("3")
            return None
        self.JSON_array[lang][question]["answer"]=txt
        self.database.set_questions_array(self.JSON_array[lang],self.name,lang)
        print("4")
        return question

    def getQID(self,chat_id,from_id):
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

    def delQID(self,chat_id,from_id):
        del self.questions[chat_id][from_id]
        if len(self.questions[chat_id])==0:
            del self.questions[chat_id]

    def getLangTCArray(self):
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
        
    def getAncestors(self):
        data=[]
        data.append(self)
        for elem in self.parents:
            data+=elem.getAncestors()
        return data

    def getHeirs(self):
        data=[]
        data.append(self)
        for elem in self.sons:
            data+=elem.getHeirs()
        return data

    def getTeachColl(self):
        data=[]
        for lang in self.teachers:
            data+=self.teachers[lang]
        for lang in self.collaborators:
            data+=self.collaborators[lang]
        return data
        
    def getResArray(self,lang,condition):
        data=[]
        if lang not in self.JSON_array:
            return data
        for elem in self.JSON_array[lang]:
            if condition=="FREE" and self.JSON_array[lang][elem]["answer"]=='':
                data.append(elem)
            elif condition=="BANNED" and self.JSON_array[lang][elem]["answer"]=="BANNED":
                data.append(elem)
            elif condition=="ANSWER" and self.JSON_array[lang][elem]["answer"]!='' and self.JSON_array[lang][elem]["answer"]!="BANNED":
                data.append(elem)
        return data

    def getTeachers(self,lang):
        if lang in self.teachers:
            return self.teachers[lang]
        return []

    def getBannedUser(self):
        return self.bannedUser

    def getArrayLang(self):
        lang_vett=[]
        for elem in self.JSON_array:
            lang_vett.append(elem)
        print("Lang: "+str(lang_vett))
        return lang_vett

    def delTeachers(self,vett,lang_class,bot):
        for elem in vett:
            data={}
            for lang in self.teachers:
                if elem not in self.teachers[lang] and len(self.teachers[lang])>0:
                    data[lang]=self.teachers[lang]
                if elem in self.teachers[lang]:
                    if len(self.teachers[lang])>1:
                        data[lang]=[]
                        for id in self.teachers[lang]:
                            if id!=elem:
                                data[lang].append(id)
                    else:
                        self.sendNotification(lang_class,lang,bot,False)
            self.teachers=data

    def delCollaborators(self,vett,lang_class,bot):
        for elem in vett:
            data={}
            for lang in self.collaborators:
                if elem not in self.collaborators[lang] and len(self.collaborators[lang])>0:
                    data[lang]=self.collaborators[lang]
                if elem in self.collaborators[lang]:
                    if len(self.collaborators[lang])>1:
                        data[lang]=[]
                        for id in self.collaborators[lang]:
                            if id!=elem:
                                data[lang].append(id)
                    else:
                        self.sendNotification(lang_class,lang,bot,False)
            self.collaborators=data
        
    
    def delStudents(self,vett):
        data={}
        for elem in vett:
            for lang in self.students:
                if elem not in self.students[lang] and len(self.students[lang])>0:
                    data[lang]=self.students[lang]
                if elem in self.students[lang] and len(self.students[lang])>1:
                    data[lang]=[]
                    for id in self.students[lang]:
                        if id!=elem:
                            data[lang].append(id)
        self.students={}
        self.students=data

    def addTeachers(self,vett,lang_str,lang,bot=None):
        if bot != None:
            self.delTeachers(vett,lang,bot)
            self.delCollaborators(vett,lang,bot)
        if len(vett)==0:
            return
        if bot!=None:
            self.sendNotification(lang,lang_str,bot)
        if lang_str not in self.teachers:
            self.teachers[lang_str]=[]
        for elem in vett:
            if elem not in self.teachers[lang_str]:
                self.teachers[lang_str].append(elem)

    def addCollaborators(self,vett,lang_str,lang,bot=None):
        if bot != None:
            self.delTeachers(vett,lang,bot)
            self.delCollaborators(vett,lang,bot)
        if len(vett)==0:
            return
        if bot!=None:
            self.sendNotification(lang,lang_str,bot)
        if lang_str not in self.collaborators:
            self.collaborators[lang_str]=[]
        for elem in vett:
            if elem not in self.collaborators[lang_str]:
                self.collaborators[lang_str].append(elem)
    
    def addStudents(self,vett,lang):
        self.delStudents(vett)
        if len(vett)==0:
            return
        if lang not in self.students:
            self.students[lang]=[]
        for elem in vett:
            if elem not in self.students[lang]:
                self.students[lang].append(elem)

    def getStudentLang(self,id):
        for lang in self.students:
            if id in self.students[lang]:
                return lang
        return None
    
    def getToCLang(self,id):
        for lang in self.collaborators:
            if id in self.collaborators[lang]:
                return lang
        for lang in self.teachers:
            if id in self.teachers[lang]:
                return lang
        return None

    def setHash(self,hash):
        self.hash=hash

    def getHash(self):
        return self.hash

    def addParent(self,node):
        self.parents.append(node)
    
    def addSon(self,node):
        self.sons.append(node)

    def delSon(self,node):
        self.sons.remove(node)

    def delParent(self,node):
        self.parents.remove(node)

    def addJSON(self,node,lang):
        for lang_str in ["it","de","en","es","fr"]:
            data={}
            data=node.getJSONArray(lang,lang_str,recursive=False)
            if len(data)>0:
                if lang_str not in self.JSON_array:
                    self.JSON_array[lang]=data
                else:
                    self.JSON_array[lang].update(data)

    def retStruct(self):
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

    def getArrays(self):
        return sorted(self.parents), sorted(self.sons)

    def change(self,node1,node2):
        for num in range(0,len(self.sons)):
            if self.sons[num] == node1:
                self.sons[num] = node2
        for num in range(0,len(self.sons)):
            if self.parents[num] == node1:
                self.parents[num] = node2

    def getName(self):
        return self.name

    def getMultipleLangArray(self):
        return self.JSON_array

    def setMergedArray(self,obj,lang):
        data={}
        data1=obj.getMultipleLangArray()
        for lang_str in self.JSON_array:
            data[lang_str]={}
            if lang not in data1:
                data[lang_str]=self.mergeArrays(self.JSON_array[lang_str],data1,lang,lang_str)
            else:
                data[lang_str]=self.JSON_array[lang_str]
        for lang_str in data1:
            if lang_str not in data:
                data[lang_str]=data1[lang_str]
        self.JSON_array=data

    def getSecondSon(self,obj):
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

    def isParent(self,obj):
        return obj in self.parents

    def delParent(self,obj):
        self.parents.remove(obj)

    def delSon(self,obj):
        self.sons.remove(obj)

    def isSon(self,obj):
        return obj in self.sons

    def addParents(self,array):
        self.parents=array

    def addSons(self,array):
        self.sons=array

    def is_in_array(self,string,array,lang,lang_str):
        for elem in array:
            if lang.calculate_similarity(string,elem,lang_str) > 0.8:
                return True
        return False

    def mergeArrays(self,array1,array2,lang,lang_str):
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

    def sendNotification(self,lang,lang_str,bot,new=True):
        string=""
        if new:
            string="new_lang"
        else:
            string="del_lang"
        if (lang_str not in self.collaborators or len(self.collaborators[lang_str])==0) and (lang_str not in self.teachers or len(self.teachers[lang_str])==0):
            for elem in self.students:
                for chat_id in self.students[elem]:
                    bot.sendMessage(chat_id,lang.getString(elem,string,xxx=lang.getString(elem,lang_str)))

    def calc_distance(self,lang,lang_str):
        data={}
        if lang_str in self.JSON_array:
            data[0]=self.JSON_array[lang_str]
        for elem in self.parents:
            array=elem.calc_distance(lang_str)
            for num in array:
                if num+1 not in array:
                    data[num+1]={}
                data[num+1]=self.mergeArrays(data[num+1],array[num],lang,lang_str)
        return data
    
    def add_response(self,question,lang,txt):
        self.JSON_array[lang][question]["answer"]=txt
        
    def delete_question(self,question,lang):
        del self.JSON_array[lang][question]

    def deleteDoubleQuestion(self,lang,lang_str):
        if lang_str not in self.JSON_array:
            return
        data={}
        data=self.calc_distance(lang,lang_str)
        for elem in data:
            if elem==0:
                continue
            for question in data[elem]:
                vett=[]
                for question1 in self.JSON_array[lang_str]:
                    if lang.calculate_similarity(question,question1,lang_str) > 0.8:
                        vett.append(question1)
                for question1 in vett:
                    del self.JSON_array[lang_str][question1]
        return

    def add_question(self,txt,lang,res=""):
        if lang not in self.JSON_array:
            self.JSON_array[lang]={}
        self.JSON_array[lang][txt]={}
        self.JSON_array[lang][txt]["answer"]=res
        self.JSON_array[lang][txt]["ids"]=[]
        self.JSON_array[lang][txt]["code"]=len(self.JSON_array[lang])

    def crossMatch(self,obj,lang,lang_str):
        tot={}
        tot[0]=0
        tot[1]=0
        num={}
        val={}
        if lang_str not in self.JSON_array:
            tot[0]=1.0
            tot[1]=1.0
            return tot
        l=len(self.JSON_array[lang_str])
        if l==0:
            tot[0]=1.0
            tot[1]=1.0
            return tot
        obj_array=obj.getJSONArray(lang,lang_str,recursive=False)
        for elem in self.JSON_array[lang_str]:
            num[0]=0
            num[1]=0
            for elem1 in obj_array:
                val[0]=lang.calculate_similarity(elem,elem1,lang_str)
                val[1]=lang.calculate_similarity(self.JSON_array[lang_str][elem]['a'],obj_array[elem1]['a'],lang_str)
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

    def crossLang(self,obj,lang,lang_vett):
        for elem in lang_vett:
            vett=self.crossMatch(obj,lang,elem)
            print(vett)
            for i in vett:
                if vett[i]< 0.8:
                    return False
        return True

    def getLang(self):
        array=[]
        for elem in self.teachers:
            array.append(elem)
        for elem in self.collaborators:
            if elem not in array:
                array.append(elem)
        return sorted(array)

    def __eq__(self,obj):
        p1, s1 = self.getArrays()
        p2, s2 = obj.getArrays()
        if len(p1)!=len(p2) or len(s1)!=len(s2):
            return False
        for num in range(0,len(p1)):
            if p1[num]!=p2[num]:
                return False
        for num in range(0,len(s1)):
            if s1[num]!=s2[num]:
                return False
        return True

    def retQVett(self,lang):
        vett=[]
        if lang in self.JSON_array:
            vett=self.JSON_array[lang]
        return vett

    def getTransArray(self,src,dst):
        vett=self.retQVett(src)
        vett1=self.retQVett(dst)
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
        return self.getName() < obj.getName()
    
    def __gt__(self,obj):
        return self.getName() > obj.getName()

    def __le__(self,obj):
        return self.getName() <= obj.getName()
    
    def __ge__(self,obj):
        return self.getName() >= obj.getName()

    def __de__(self):
        print("Nodo "+self.name+" eliminato")
