from library import match_command, tag_group, send_message, send_document, match_command

from bots.user.bot_user_class import BotUser

class BotUserEvents:
    class Singleton(BotUser):

        def __init__(self,token):
            self.bot_name="ue"
            super().__init__(token,match_command_handler=self.match_command_handler,permissions=self.permissions)

        def permissions(self,user):
            return super().get_database().get_postgres().run_function("user_set",str(user["id"]),f"'{user['first_name'].lower()}'",f"'{user['last_name'].lower()}'",f"'{user['username'].lower()}'")
        
        def send_notifies(self,events):
            for event in events:
                send_message(super().get_bot(),event["user_telegram_id"],f"Ricordati di partecipare all'evento: {event['event_name']}.")
        
        def match_command_handler(self,chat_id,from_id,chat_type,content_type,txt,user):
            if match_command('/start',txt,chat_type,user):
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere la lista degli eventi","Vorrei iscrivermi ad un evento","Vorrei disiscrivermi ad un evento"]))
                super().set_status(self.bot_name,chat_id,from_id,1,None)
            elif match_command('/list',txt,chat_type,user):
                self.command_one(chat_id,from_id,chat_type,user)
            elif match_command('/subscribe',txt,chat_type,user):
                self.command_two(chat_id,from_id,chat_type,user)
            elif match_command('/unsubscribe',txt,chat_type,user):
                self.command_three(chat_id,from_id,chat_type,user)
            else:
                super().match_status(txt,chat_id,from_id,chat_type,user)
        
        def match_status(self,txt,chat_id,from_id,chat_type,user,status):
            match status.id:
                case 1:
                    self.case_one(txt,chat_id,from_id,chat_type,user)
                    
        def case_one(self,txt,chat_id,from_id,chat_type,user):
            match txt:
                case "vorrei vedere la lista degli eventi":
                    self.command_one(chat_id,from_id,chat_type,user)
                case "vorrei iscrivermi ad un evento":
                    self.command_two(chat_id,from_id,chat_type,user)
                case "vorrei disiscrivermi ad un evento":
                    self.command_three(chat_id,from_id,chat_type,user)
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())
                    
        def command_one(self,chat_id,from_id,chat_type,user):
            return
        
        def command_two(self,chat_id,from_id,chat_type,user):
            return
        
        def command_three(self,chat_id,from_id,chat_type,user):
            return
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUserEvents.instance:
            BotUserEvents.instance = BotUserEvents.Singleton(token)
        return BotUserEvents.instance 