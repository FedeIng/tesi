from telegram.ext import Updater, MessageHandler, Filters, CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton, Bot

from data_structs.status import Status
from databases.database_class import Database
from library import send_bug, send_message, tag_group

class Bot:

    def __init__(self,token,match_command_handler=lambda chat_id,from_id,chat_type,content_type,txt,user : None,permissions=lambda user : True):
        self.token=token
        self.permissions=permissions
        self.match_command_handler=match_command_handler
        self.bot_instance=Bot(token)
        self.database=Database()
        self.updater=Updater(token,use_context=True)
        self.updater.dispatcher.add_handler(MessageHandler(Filters.text,self.message_handler))
        self.updater.start_polling()
        self.updater.idle()
        self.error_string="Comando non trovato, si prega di rieseguire il comando \start."
        
    def message_handler(self,update,context):
        chat_id,from_id,chat_type,content_type=self.glance(update.message)
        if content_type == 'text':
            txt=update.message.text.lower()
            user=self.get_bot().getChat(from_id)
            if self.permissions(user):
                self.match_command_handler(chat_id,from_id,chat_type,content_type,txt,user)
            else:
                send_message(self.get_bot(),chat_id,"Non hai i permessi per usare questo bot.")
    
    def glance(self,message):
        return message.chat_id, message.from_id, message.chat_type, message.content_type

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