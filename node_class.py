from language_class import *
import json
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Node:

    def __init__(self,nodeName,array):
        self.name=nodeName
        self.JSON_array={}
        self.JSON_array=array
        self.parents=[]
        self.sons=[]
        self.id_commands={}
        self.teachers={}
        self.collaborators={}
        self.bannedUser=[]
        self.questions={}
        self.students={}
        self.hash=""

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
                if id not in self.JSON_array[lang][question]["id"]:
                    self.JSON_array[lang][question]["id"].append(id)
                return True
        for p in self.parents:
            if p.add_chat_id(question,lang,id):
                return True
        return False

    def setstudentID(self,vett):
        self.id_commands=vett

    def getstudentID(self):
        return self.id_commands

    def setBannedUsers(self,lang):
        users={}
        for lang_str in self.JSON_array:
            array=self.getJSONArray(self,lang,lang_str)
            for elem in array:
                if "a" in array[elem]:
                    if array[elem]["a"]=="BANNED":
                        for chat_id in array[elem]["id"]:
                            if chat_id in users:
                                users[chat_id]+=1
                            else:
                                users[chat_id]=1
        for chat_id in users:
            if users[chat_id]>10:
                self.bannedUser.append(chat_id)
        for p in self.parents:
            p.setBannedUsers(lang)
        
    def setQID(self,chat_id,txt):
        self.questions[chat_id]=txt

    def getQID(self,chat_id):
        if chat_id not in self.questions:
            return None
        return self.questions[chat_id]

    def delQID(self,chat_id):
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
        
    def getResArray(self,lang,lang_class,condition):
        data=[]
        if lang not in self.JSON_array:
            return data
        array=self.getJSONArray(self,lang,lang_class)
        for elem in self.JSON_array[lang]:
            if condition=="FREE" and self.JSON_array[lang][elem]["a"]=='':
                data.append(elem)
            elif condition=="BANNED" and self.JSON_array[lang][elem]["a"]=="BANNED":
                data.append(elem)
            elif condition=="ANSWER" and self.JSON_array[lang][elem]["a"]!='' and self.JSON_array[lang][elem]["a"]!="BANNED":
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

    def getJSONArray(self,lang,lang_str,recursive=True):
        data={}
        if not recursive:
            if lang_str in self.JSON_array:
                return self.JSON_array[lang_str]
            else :
                return data
        if lang_str in self.JSON_array:
            data=self.JSON_array[lang_str]
        for node in self.parents:
            data=self.mergeArrays(data,node.getJSONArray(lang,lang_str),lang,lang_str)
        print(self.name,data)
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
        self.JSON_array[lang][question]["a"]=txt
        
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
        self.JSON_array[lang][txt]["a"]=res
        self.JSON_array[lang][txt]["id"]=[]
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

    def getTransArray(self,lang,src,dst):
        vett=self.getJSONArray(lang,src)
        vett1=self.getJSONArray(lang,dst)
        array=[]
        for elem in vett:
            string=lang.translate(elem,src,dst)
            if vett[elem]["a"] != "BANNED" and vett[elem]["a"] != "" and not self.is_in_array(string,vett1,lang,dst):
                string="\""+string+"\" -> \""+lang.translate(vett[elem]["a"],src,dst)+"\""
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