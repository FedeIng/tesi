import datetime
import telepot
from telepot.exception import TelegramError, BotWasBlockedError
from library import tag_group, edit_message, send_message
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from database_class import Database

class BotId:
    class Singleton:

        def __init__(self):
            self.database=Database()
            self.id_commands={}
            self.id_times={}
            self.bot_array={}
            self.key_id=self.database.get_key_id()

        def reset_key_id(self,name):
            if name in self.key_id:
                for chat_id in self.key_id[name]:
                    edit_message(self.bot_array[name],(chat_id,self.key_id[name][chat_id]))
                del self.key_id[name]
                self.database.del_key_id(name)  

        def set_key_id(self,msg_id,name):
            chat_id=msg_id[0]
            if name in self.key_id:
                if chat_id in self.key_id[name]:
                    edit_message(self.bot_array[name],(chat_id,self.key_id[name][chat_id]))
            else:
                self.key_id[name]={}
            self.key_id[name][chat_id]=msg_id[1]
            self.database.set_key_id(name,self.key_id[name])

        def start_fun(self,chat_id,from_id,chat_type,lang,lang_class,name,topic,keyboard):
            user=self.bot_array[name].getChat(from_id)
            send_message(self.bot_array[name],chat_id, tag_group(chat_type,user)+lang_class.get_string(lang,"start",xxx=topic))
            try:
                self.set_key_id(telepot.message_identifier(send_message(self.bot_array[name],chat_id, lang_class.get_string(lang,"command"), reply_markup=keyboard)),name)
            except TypeError:
                pass

        def set_bot(self,name,bot):
            self.bot_array[name]=bot

        def add_elem_id(self,array,name,id1,id2):
            if name not in array:
                array[name]={}
            if id1 not in array[name]:
                array[name][id1]=[]
            array[name][id1].append(id2)
            return array

        def delete_elem_id(self,array,name,id1,id2):
            array[name][id1].remove(id2)
            if len(array[name][id1])==0:
                del array[name][id1]
            if len(array[name])==0:
                del array[name]
            return array

        def sub_smi():
            if elem == elem1:
                if time == None or time<self.id_times[name][elem]:
                    time=self.id_times[name][elem]
                    index=[name,elem,elem1]
                else:
                    if time == None or time<self.id_times[name][elem][elem1]:
                        time=self.id_times[name][elem][elem1]
                        index=[name,elem,elem1]
            return time, index

        def set_max_index(self,old_array):
            time=None
            index=[]
            for name in old_array:
                for elem in old_array[name]:
                    for elem1 in old_array[name][elem]:
                        time, index=self.sub_smi(time,index)
            return index

        def delete_old(self,chat_type,lang_class,lang,num):
            old_array={}
            count=0
            max_index=[]
            for name in self.id_times:
                for elem in self.id_times[name]:
                    if type(self.id_times[name][elem]) is dict:
                        for elem1 in self.id_times[name][elem]:
                            if count<num:
                                old_array=self.add_elem_id(old_array,name,elem,elem1)
                                max_index=self.set_max_index(old_array)
                                count+=1
                            elif max_index[0]==max_index[1] and self.id_times[name][max_index[0]]>self.id_times[name][elem][elem1]:
                                old_array=self.delete_elem_id(old_array,name,max_index[0],max_index[0])
                                old_array=self.add_elem_id(old_array,name,elem,elem1)
                                max_index=self.set_max_index(old_array)
                            elif max_index[0]!=max_index[1] and self.id_times[name][max_index[0]][max_index[1]]>self.id_times[name][elem][elem1]:
                                old_array=self.delete_elem_id(old_array,name,max_index[0],max_index[1])
                                old_array=self.add_elem_id(old_array,name,elem,elem1)
                                max_index=self.set_max_index(old_array)
                    elif type(self.id_times[name][elem]) is datetime.datetime:
                        if count<num:
                            old_array=self.add_elem_id(old_array,name,elem,elem)
                            count+=1
                        elif max_index[0]==max_index[1] and self.id_times[name][max_index[0]]>self.id_times[name][elem]:
                            old_array=self.delete_elem_id(old_array,name,max_index[0],max_index[0])
                            old_array=self.add_elem_id(old_array,name,elem,elem)
                            max_index=self.set_max_index(old_array)
                        elif max_index[0]!=max_index[1] and self.id_times[name][max_index[0]][max_index[1]]>self.id_times[name][elem]:
                            old_array=self.delete_elem_id(old_array,name,max_index[0],max_index[1])
                            old_array=self.add_elem_id(old_array,name,elem,elem)
                            max_index=self.set_max_index(old_array)
            for name in old_array:
                for elem in old_array[name]:
                    for elem1 in old_array[name][elem]:
                        user=bot.getChat(elem1)
                        if elem==elem1:
                            del self.id_times[name][elem]
                            if name in self.id_commands and elem in self.id_commands[name]:
                                send_message(self.bot_array[name],elem,lang_class.get_string(lang,"timeout"))
                                del self.id_commands[name][elem]
                                if len(self.id_commands[name])==0:
                                    del self.id_commands[name]
                        elif elem!=elem1:
                            del self.id_times[name][elem][elem1]
                            if name in self.id_commands and elem in self.id_commands[name] and elem1 in self.id_commands[name][elem]:
                                send_message(self.bot_array[name],elem,tag_group(chat_type,user)+lang_class.get_string(lang,"timeout"))
                                del self.id_commands[name][elem][elem1]
                                if len(self.id_commands[name][elem])==0:
                                    del self.id_commands[name][elem]
                                    if len(self.id_commands[name])==0:
                                        del self.id_commands[name]
                            if len(self.id_times[name][elem])==0:
                                del self.id_times[name][elem]
                if len(self.id_times[name])==0:
                    del self.id_times[name]

        def add_elem(self,array,array1,elem,elem1,name):
            if elem1!=None:
                if elem not in array:
                    array[elem]={}
                    array1[elem]={}
                array[elem][elem1]=self.id_times[name][elem][elem1]
                if elem in self.id_commands[name] and elem1 in self.id_commands[name][elem]:
                    array1[elem][elem1]=self.id_commands[name][elem][elem1]
                return array, array1
            array[elem]=self.id_times[name][elem]
            if elem in self.id_commands[name]:
                array1[elem]=self.id_commands[name][elem]
            return array, array1

        def normalize_vect(self,chat_type,lang_class,lang,time,name):
            new_times={}
            new_ids={}
            count=0
            for elem in self.id_times[name]:
                if type(self.id_times[name][elem]) is dict:
                    for elem1 in self.id_times[name][elem]:
                        user=bot.getChat(elem1)
                        if self.id_times[name][elem][elem1]>time:
                            new_times,new_ids=self.add_elem(new_times,new_ids,elem,elem1,name)
                            count+=1
                        elif name in self.id_commands and elem in self.id_commands[name] and elem1 in self.id_commands[name][elem]:
                            send_message(self.bot_array[name],elem,tag_group(chat_type,user)+lang_class.get_string(lang,"timeout"))
                elif type(self.id_times[name][elem]) is datetime.datetime:
                    if self.id_times[name][elem]>time:
                        new_times,new_ids=self.add_elem(new_times,new_ids,elem,None,name)
                        count+=1
                    elif name in self.id_commands and elem in self.id_commands[name]:
                        send_message(self.bot_array[name],elem,lang_class.get_string(lang,"timeout"))
            self.id_times[name]=new_times
            self.id_commands[name]=new_ids
            return count

        def set_time(self,from_id,chat_id,name):
            if name not in self.id_times:
                self.id_times[name]={}
            if from_id==chat_id:
                self.id_times[name][chat_id]=datetime.datetime.today()
            else :
                if chat_id not in self.id_times[name]:
                    self.id_times[name][chat_id]={}
                self.id_times[name][chat_id][from_id]=datetime.datetime.today()

        def del_id(self,from_id,chat_id,name):
            if name in self.id_commands:
                if from_id==chat_id:
                    if chat_id in self.id_commands[name]:
                        del self.id_commands[name][chat_id]
                else :
                    if chat_id in self.id_commands[name]:
                        if from_id in self.id_commands[name][chat_id]:
                            del self.id_commands[name][chat_id][from_id]
                        if len(self.id_commands[name][chat_id])==0:
                            del self.id_commands[name][chat_id]
                if len(self.id_commands[name])==0:
                    del self.id_commands[name]

        def add_id(self,from_id,chat_id,val,name):
            if name not in self.id_commands:
                self.id_commands[name]={}
            if from_id==chat_id:
                self.id_commands[name][chat_id]=val
            else :
                if chat_id not in self.id_commands[name]:
                    self.id_commands[name][chat_id]={}
                self.id_commands[name][chat_id][from_id]=val

        def check_id(self,from_id,chat_id,name):
            ret_val=0
            if name in self.id_commands:
                if from_id==chat_id:
                    if chat_id in self.id_commands[name]:
                        ret_val=self.id_commands[name][chat_id]
                else :
                    if chat_id in self.id_commands[name] and from_id in self.id_commands[name][chat_id]:
                        ret_val=self.id_commands[name][chat_id][from_id]
            return ret_val

        def delete_old_ids(self,chat_type,lang_class,lang):
            count=0
            lim=1000
            for id_name in self.id_commands:
                count+=self.normalize_vect(chat_type,lang_class,lang,datetime.datetime.now()-datetime.timedelta(0, 300, 0),id_name)
            if count>lim:
                self.delete_old(chat_type,lang_class,lang,count-lim)

        def add_time_id(self,chat_type,lang_class,lang,from_id,chat_id,val,name):
            self.add_id(from_id,chat_id,val,name)
            self.set_time(from_id,chat_id,name)
            self.delete_old_ids(chat_type,lang_class,lang)

        def check_time_id(self,chat_type,lang_class,lang,from_id,chat_id,name):
            num=self.check_id(from_id,chat_id,name)
            self.set_time(from_id,chat_id,name)
            self.delete_old_ids(chat_type,lang_class,lang)
            return num

        def del_time_id(self,chat_type,lang_class,lang,from_id,chat_id,name):
            self.del_id(from_id,chat_id,name)
            self.set_time(from_id,chat_id,name)
            self.delete_old_ids(chat_type,lang_class,lang)
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotId.instance:
            BotId.instance = BotId.Singleton()
        return BotId.instance
