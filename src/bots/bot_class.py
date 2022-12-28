import telepot

from data_structs.status import Status
from databases.database_class import Database
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from library import send_bug

class Bot:

    def __init__(self,token,message=lambda msg : None,query=lambda msg : None):
        self.token=token
        self.bot_instance=telepot.Bot(token)
        self.database=Database()
        self.bot_instance.message_loop({'chat':message,'callback_query':query})
        self.error_string = "Comando non trovato, si prega di rieseguire il comando \start."

    def get_bot(self):
        return self.bot_instance

    def get_token(self):
        return self.token
    
    def get_database(self):
        return self.database

    def set_status(self,bot_name,chat_id,from_id,status_id,data):
        self.database.get_redis().set_object(bot_name,chat_id,from_id,Status(status_id,obj=data))

    def get_status(self,bot_name,chat_id,from_id):
        return self.database.get_redis().get_and_delete_object(bot_name,chat_id,from_id)

    def get_error_string(self):
        return self.error_string
    
    def send_bug(self,txt,chat_id,chat_type,user,bot_name):
        send_message(self.bot_instance,chat_id,f"{tag_group(chat_type,user)} Bug segnalato.")
        send_bug(bot_name,chat_id,txt)

    def set_keyboard(self,string_array,bool_var=True):
        i=0
        data=[]
        l=0
        for elem in string_array:
            if i == 0:
                data.append([])
                l+=1
            data[l-1].append(KeyboardButton(text=elem))
            i+=1
            i%=2
        return ReplyKeyboardMarkup(keyboard=data,resize_keyboard=True,one_time_keyboard=True,selective=bool_var)