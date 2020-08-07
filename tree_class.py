from node_class import *
from language_class import *
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
            self.array[topic]=Bot_student(database.get_topic_token(topic),topic,database,self.lang)
            print("Bot "+topic+" created")
        #for down in data:
            #for up in data[down]:
                #node1=self.array[down]
                #if up not in self.array:
                    #self.createNode(up)
                #node2=self.array[up]
                #node1.addParent(node2)
                #node2.addSon(node1)
        #with open(authName,'r') as json_file:
            #data=json.load(json_file)
        #for elem in data:
            #self.array[elem].setHash(data[elem]["hash"])
            #for lang in data[elem]:
                #if lang=="hash":
                    #continue
                #if "students" in data[elem][lang]:
                    #self.array[elem].addStudents(data[elem][lang]["students"],lang)
                #if "teachers" in data[elem][lang]:
                    #self.array[elem].addTeachers(data[elem][lang]["teachers"],lang,self.lang)
                #if "collaborators" in data[elem][lang]:
                    #self.array[elem].addCollaborators(data[elem][lang]["collaborators"],lang,self.lang)
        #self.setnum()
        #self.writeData()

    def send_notification(self,bot):
        for topic in self.array:
            self.array[topic].send_notification(bot,self.lang)

    def read_ban(self):
        return self.database.read_ban()

    def get_lang(self):
        return self.lang

    def get_database(self):
        return self.database

    def checkLangStr(self,txt,string):
        return self.lang.checkLangStr(txt,string)

    def getBestResp(self,txt,lang,topic):
        list1={}
        JSONarray=self.array[topic].getJSONArray(self.lang,lang)
        for question in JSONarray:
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

    def sendNotification(self,teacher,student,topic):
        self.array[topic].sendRestartNotify(teacher,student,self.lang)

    def setChooseLang(self,topic):
        return self.lang.setKeyboard(self.array[topic].getLang(),True)

    def addCollaborators(self,vett,topic,lang):
        self.array[topic].addCollaborators(lang,vett)

    def getHint(self,topic,lang):
        vett=[]
        for elem in ["it","de","en","es","fr"]:
            if elem != lang:
                vett+=self.array[topic].getTransArray(elem,lang)
        return vett

    def getstudentID(self):
        data={}
        for elem in self.array:
            vett=self.array[elem].getstudentID()
            if len(vett)>0:
                data[elem]=vett
        return data

    def new_bot(self,token,topic,hash):
        self.database.new_topic(token,topic,hash)
        self.array[topic]=Bot_student(token,topic,self.database,self.lang)
        print("Bot "+topic+" created")

    def get_pwd_admin(self):
        return self.database.get_pwd_admin()

    def getTokenList(self):
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

    def setstudentID(self,vett):
        for elem in vett:
            self.array[elem].setstudentID(vett[elem])

    def verify_password(self,topic,password):
        return self.array[topic].verify_password(password)

    def add_question_by_hint(self,lang,question,response,chat_id,from_id,topic):
        self.setQuestion(question,lang,topic,chat_id)
        self.setQID(chat_id,from_id,question,topic)
        self.setRes(chat_id,from_id,response,lang,topic)

    def topicKeyboard(self):
        return createReplyKeyboard(array_to_matrix(self.get_topic_list()))

    def deleteTC(self,chat_id,topic):
        self.array[topic].delTeachers([chat_id])
        self.array[topic].delCollaborators([chat_id])

    def addTeachers(self,vett,topic,lang):
        self.array[topic].addTeachers(lang,vett)

    def get_bot_by_topic(self,topic):
        return self.array[topic].get_bot()

    def get_bot_pwd(self):
        return self.database.get_bot_pwd().get_bot()

    def getIdsArray(self,topic,lang,txt):
        array=self.array[topic].getJSONArray(lang)
        print(array)
        print(array[txt])
        return array[txt]["ids"]

    def addAdmins(self,lang,vett):
        self.lang.addAdmins(lang,vett)

    def getAdmins(self,lang):
        return self.lang.getAdmins(lang)

    def setHash(self,topic,hash):
        self.array[topic].setHash(hash)
        self.writeData()

    def setQID(self,chat_id,from_id,txt,topic):
        self.array[topic].setQID(chat_id,from_id,txt)

    def gethashlist(self):
        hashlist=[]
        for node in self.array:
            hashlist.append(self.array[node].getHash())
        return hashlist

    def getHash(self,topic):
        return self.array[topic].getHash()

    def contains(self,node,question,txt,lang):
        vett=node.getJSONArray(self.lang,lang,False)
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

    def getSent(self,lang,text):
        return self.lang.question_sent(lang,text)

    def state_exist(self,node1,node2):
        p1=self.array[node1].getArrays()[0]
        p2=self.array[node2].getArrays()[0]
        for node in list(set(p1).intersection(p2)):
            if sorted(p1,p2)==node.getArrays()[1]:
                return node.getName(), True
        return None, False

    def normalizeTree(self,node1,node2):
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

    def getQArray(self,chat_id,lang,topic):
        list_q=self.array[topic].getJSONArray(self.lang,lang,True)
        list_u=[]
        for elem in list_q:
            if chat_id in list_q[elem]["id"]:
                list_u.append(elem)
        return list_u

    def getQID(self,chat_id,from_id,topic):
        return self.array[topic].getQID(chat_id,from_id)
    
    def delQID(self,chat_id,from_id,topic):
        self.array[topic].delQID(chat_id,from_id)

    def setRes(self,chat_id,from_id,txt,lang,topic):
        question=self.array[topic].getQID(chat_id,from_id)
        if question != None:
            print("1")
            return self.array[topic].setResponse(lang,question,txt)
        print("0")
        return None

    def setBan(self,txt,lang,topic):
        jarray=self.array[topic].getJSONArray(lang)
        for elem in jarray:
            e=self.matchArray1(txt,lang,jarray)
            if e != None:
                if jarray[e]["answer"]=="":
                    self.array[topic].setResponse(lang,e,"BANNED")
        self.array[topic].setBannedUsers(self.lang)
        #self.writeData()

    def setSban(self,txt,lang,topic):
        jarray=self.array[topic].getJSONArray(lang)
        for elem in jarray:
            e=self.matchArray1(txt,lang,jarray)
            if e != None:
                if jarray[e]["answer"]=="BANNED":
                    self.array[topic].setResponse(lang,e,"")
        self.array[topic].setBannedUsers(self.lang)
        #self.writeData()

    def set_nlp(self,lang):
        self.lang.set_nlp(lang)

    def setLangResp(self,id,lang,bot):
        self.lang.setLangResp(id,lang,bot)

    def add_id(self,from_id,chat_id,num,topic):
        return self.array[topic].add_id(from_id,chat_id,num)

    def getResArray(self,topic,lang,condition):
        return self.array[topic].getResArray(lang,condition)

    def check_id(self,from_id,chat_id,topic):
        return self.array[topic].check_id(from_id,chat_id)

    def del_id(self,from_id,chat_id,topic):
        return self.array[topic].del_id(from_id,chat_id)

    def getTopic(self,chat_id):
        for node in self.array:
            if chat_id in self.array[node].getTeachColl():
                return node
        return None

    def getTeacherIDs(self):
        teachers=[]
        for node in self.array:
            teachers+=self.array[node].getTeachColl()
        return teachers

    def bot_enabled(self,topic):
        if len(self.array[topic].getTeachColl())==0:
            return False
        return True

    def getTeachersAndCollaborators(self,topic):
        return self.array[topic].getLangTCArray()

    def getResID(self,lang,topic):
        return self.array[topic].getTeachers(lang)
        
    def matchArray(self,txt,lang,vett):
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

    def matchArray1(self,txt,lang,vett):
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

    def writeData(self):
        for elem in self.array:
            self.array[elem].set_formatted_data()

    def setQuestion(self,txt,lang,topic,chat_id):
        self.array[topic].add_question(txt,lang)
        self.array[topic].add_chat_id(txt,lang,chat_id)
        self.writeData()

    def getResponse(self,txt,lang,topic,chat_id=None):
        JSONarray=self.array[topic].getJSONArray(lang)
        val=0
        q=""
        for question in JSONarray:
            num=self.lang.calculate_similarity(txt,question,lang)
            if num > val:
                val=num
                q=question
        if val>0.8:
            if chat_id != None:
                self.array[topic].add_chat_id(q,lang,chat_id)
                self.writeData()
            return JSONarray[q]["answer"]
        else:
            return None

    def matchCommand(self,id,command,msg,bot,lang):
        name=""
        if type(bot) is dict:
            name=bot["bot"].getMe()["username"]
            if id in self.array[bot["topic"]].getBannedUser():
                if command=="/start":
                    bot["bot"].sendMessage(id,self.getString(lang,"stop"))
                return False
        elif type(bot) is telepot.Bot:
            name=bot.getMe()["username"]
            if id not in self.getTeacherIDs():
                if command=="/start":
                    bot.sendMessage(id,self.getString(lang,"stop"),reply_markup=ReplyKeyboardRemove(selective=True))
                return False
        if (msg["chat"]["type"]=="group" or msg["chat"]["type"]=="supergroup") and msg["text"]==command+"@"+name:
            return True
        elif msg["chat"]["type"]=="private" and msg["text"]==command:
            return True
        return False

    def getLangBoard(self,lang,array):
        return self.lang.getLangBoard(lang,array)

    def setKeyboard(self,lang_array):
        return self.lang.setKeyboard(lang_array,False)

    def setUserLang(self,id,lang,topic):
        self.array[topic].addStudents([id],lang)
        self.writeData()

    def getString(self, lang, string, xxx=None, yyy=None):
        return self.lang.getString(lang,string,xxx,yyy)

    def getUserLang(self,id,topic):
        return self.array[topic].getStudentLang(id)

    def getSuperUserLang(self,id,topic):
        return self.array[topic].getToCLang(id)

    def deleteNode(self,name):
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
        self.writeData()

    def checkColl(self,lang,text):
        return self.lang.checkColl(lang,text)

    def checkTeach(self,lang,text):
        return self.lang.checkTeach(lang,text)

    def createNode(self,new_name,w=False):
        if new_name in self.array:
            return False
        qa_array={}
        with open(self.dataName,'r') as json_file:
            qa_array=json.load(json_file)
        if new_name not in qa_array:
            qa_array[new_name]={}
        new_node=Node(new_name,qa_array[new_name])
        new_node.setBannedUsers(self.lang)
        self.array[new_name]=new_node
        if w:
            self.writeData()
        return True

    def addNode(self,name1,name2,new_name):
        if name1 not in self.array or name2 not in self.array:
            return False
        if not self.createNode(new_name):
            return False
        node1=self.array[name1]
        node2=self.array[name2]
        new_node=self.array[new_name]
        node1.addParent(new_node)
        node2.addParent(new_node)
        new_node.addSon(node1)
        new_node.addSon(node2)
        self.writeData()
        return True

    def mergeNode(self,name1,name2):
        node1=self.array[name1]
        node2=self.array[name2]
        if node1==node2:
            node1.substite(node2)
            del self.array[name1]
            return True
        return False

    def deleteLink(self,name1,name2):
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
