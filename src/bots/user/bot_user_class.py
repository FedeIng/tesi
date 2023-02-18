from bots.bot_class import Bot

class BotUser(Bot):
    
    def __init__(self,token,match_command_handler=lambda chat_id,from_id,chat_type,content_type,txt,user : None,status_switcher=lambda txt,chat_id,from_id,chat_type,user,status : None):
        super().__init__(token,match_command_handler=match_command_handler,status_switcher=status_switcher,permissions=self.permissions)
    
    def permissions(self,user):
        return super().get_database().get_postgres().run_function("telegram_id_staff_check",str(user["id"]))
    
    def get_database(self):
        return super().get_database()
    
    def get_bot(self):
        return super().get_bot()
    
    def send_bug(self,txt,chat_id,chat_type,user,bot_name):
        super().send_bug(txt,chat_id,chat_type,user,bot_name)
    
    def set_status(self,bot_name,chat_id,from_id,status_id,data):
        super().set_status(bot_name,chat_id,from_id,status_id,data)
        
    def get_status(self,bot_name,chat_id,from_id):
        return super().get_status(bot_name,chat_id,from_id)
    
    def set_keyboard(self,array):
        return super().set_keyboard(array)
    
    def match_status(self,txt,chat_id,from_id,chat_type,user,bot_name):
        super().match_status(txt,chat_id,from_id,chat_type,user,bot_name)
        
    def get_error_string(self):
        return super().get_error_string()