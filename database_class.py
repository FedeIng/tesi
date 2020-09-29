from firebase import firebase
import datetime

class Database:
    class Singleton:

        def __init__(self):
            self.db = firebase.FirebaseApplication('https://tesi-database.firebaseio.com/',None)
            self.lang_array=["it","de","en","es","fr"]
            self.bot_admin=None
            self.bot_pwd=None
            self.bot_teacher=None
            self.stud_str="/bots/students/"
            self.admin_str="/bots/admin/"

        def get_key_id(self):
            data={}
            res=self.db.get('/bots/key_id','')
            if res==None:
                return {}
            for name in res:
                data[name]={}
                for chat_id in res[name]:
                    data[name][int(chat_id)]=res[name][chat_id]
            return data

        def del_key_id(self,name):
            self.db.delete('/bots/key_id', name)

        def set_key_id(self,name,array):
            data={}
            for chat_id in array:
                data[str(chat_id)]=array[chat_id]
            self.db.put('/bots/key_id', name=name, data=data)          

        def get_banned_users(self):
            data=self.db.get('/bots/teachers/banned','')
            if data==None:
                return {}
            else:
                return data

        def new_topic(self,token,topic,hash):
            data={}
            data["token"]=token
            data["hash"]=hash
            self.db.put(self.stud_str, name=topic, data=data)

        def get_trans(self):
            return self.db.get('/translate','')

        def set_bot_admin(self,bot):
            self.bot_admin=bot

        def set_bot_pwd(self,bot):
            self.bot_pwd=bot

        def set_bot_teacher(self,bot):
            self.bot_teacher=bot

        def get_bot_admin(self):
            return self.bot_admin

        def get_bot_pwd(self):
            return self.bot_pwd

        def get_bot_teacher(self):
            return self.bot_teacher

        def write_ban(self,banned_user):
            data={}
            for elem in banned_user:
                data[str(elem)]=banned_user[elem]
            self.db.put('/bots/teachers', name="banned", data=data)
            #with open("ban.txt","w") as jfile:
                #json.dump(banned_user,jfile)
            
        def read_ban(self):
            #with open("ban.txt","r") as json_file:
                #banned_user=json.load(json_file)
            result=self.db.get('/bots/teachers/banned','')
            if result==None:
                return {}
            data={}
            for elem in result:
                data[int(elem)]=result[elem]
            return data

        def write_stud_lang(self,topic,students,lang):
            self.db.put(self.stud_str+topic+'/'+lang,name="students",data=students)

        def write_bug(self,bug_array):
            for lang in bug_array:
                for role in bug_array[lang]:
                    data={}
                    for e in bug_array[lang][role]:
                        data[e]=bug_array[lang][role][e].isoformat()
                    if len(data)>0:
                        self.db.put(self.admin_str+lang, name=role, data=data)
        
        def get_admins(self,lang):
            return self.db.get(self.admin_str+lang+'/ids','')

        def write_pwd(self,user_request):
            data={}
            for elem in user_request:
                if len(user_request[elem])>0:
                    data[str(elem)]=[]
                    for e in user_request[elem]:
                        data[str(elem)].append(e.isoformat())
            self.db.put('/bots/pwd',name='requests',data=data)

        def sub_read_bug(self,data,lang,role):
            result=self.db.get(self.admin_str+lang+'/'+role+'','')
            if result!=None:
                if lang not in data:
                    data[lang]={}
                if role not in data[lang]:
                    data[lang][role]={}
                for e in result:
                    date=datetime.datetime.fromisoformat(result[e])
                    data[lang][role][e]=date
            return data

        def read_bug(self):
            role_array=["students","teachers"]
            data={}
            for lang in self.lang_array:
                for role in role_array:
                    data=self.sub_read_bug(data,lang,role)
            return data

        def get_array_by_topic(self,topic):
            data={}
            result=self.db.get(self.stud_str+topic,'')
            for lang in self.lang_array:
                if lang in result:
                    data[lang]=result[lang]
            data["banned"]=result["banned"]
            data["hash"]=result["hash"]
            return data

        def get_stud_ids(self,topic):
            data={}
            for lang in self.lang_array:
                result=self.db.get(self.stud_str+topic+'/'+lang+'/students','')
                if result!=None:
                    data[lang]=result
            return data

        def set_coll_ids(self,array,topic,lang):
            self.db.put(self.stud_str+topic+'/'+lang,name='collaborators',data=array)

        def get_coll_ids(self,topic):
            data={}
            for lang in self.lang_array:
                result=self.db.get(self.stud_str+topic+'/'+lang+'/collaborators','')
                if result!=None:
                    data[lang]=result
            return data

        def get_hash(self,topic):
            return self.db.get(self.stud_str+topic+'/hash','')

        def get_questions_array(self,topic):
            data={}
            for lang in self.lang_array:
                result=self.db.get(self.stud_str+topic+'/'+lang+'/questions','')
                if result!=None:
                    data[lang]=result
            return data
        
        def set_questions_array(self,array,topic,lang):
            self.db.put(self.stud_str+topic+'/'+lang,name='questions',data=array)

        def set_teach_ids(self,array,topic,lang):
            self.db.put(self.stud_str+topic+'/'+lang,name='teachers',data=array)

        def get_teach_ids(self,topic):
            data={}
            for lang in self.lang_array:
                result=self.db.get(self.stud_str+topic+'/'+lang+'/teachers','')
                if result!=None:
                    data[lang]=result
            return data

        def get_topic_token(self,topic):
            return self.db.get(self.stud_str+topic+'/token','')

        def get_banned_stud(self,topic):
            result=self.db.get(self.stud_str+topic+'/banned','')
            if result==None:
                return []
            return result

        def set_banned_stud(self,topic,array):
            self.db.put(self.stud_str+topic,name='banned',data=array)

        def get_admin(self):
            data={}
            result=self.db.get(self.admin_str,'')
            data["token"]=result["token"]
            data["admins"]={}
            for lang in self.lang_array:
                if lang in result:
                    data["admins"][lang]=result[lang]["ids"]
            return data

        def get_creation(self):
            return self.db.get('/bots/creation','')

        def del_bot(self,topic):
            self.db.delete(self.stud_str,topic)

        def get_getlink(self):
            return self.db.get('/bots/getlink','')

        def get_pwd(self):
            return self.db.get('/bots/pwd/bot','')

        def get_pwd_admin(self):
            return self.db.get('/bots/pwd/admin','')

        def get_teacher(self):
            return self.db.get('/bots/teachers/token','')

        def read_pwd(self):
            data={}
            result=self.db.get('/bots/pwd/requests','')
            if result==None:
                return {}
            for elem in result:
                data[int(elem)]=[]
                for e in result[elem]:
                    date=datetime.datetime.fromisoformat(e)
                    data[int(elem)].append(date)
            return data

        def set_new_pwd(self,topic,pwd):
            self.db.put(self.stud_str+topic,name='hash',data=pwd)

        def get(self,string,string1):
            return self.db.get(string,string1)
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Database.instance:
            Database.instance = Database.Singleton()
        return Database.instance