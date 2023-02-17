from library import match_command, tag_group, send_message, send_document, match_command

from bots.bot_class import Bot

class BotEventsMaker:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="em"
            super().__init__(token,match_command_handler=self.match_command_handler,permissions=self.permissions)

        def permissions(self,user):
            return super().get_database().get_postgres().run_function("telegram_id_event_maker_check",str(user["id"]))
        
        def match_command_handler(self,chat_id,from_id,chat_type,content_type,txt,user):
            if match_command('/start',txt,chat_type,user):
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco","Vorrei segnalare un bug"]))
                super().set_status(self.bot_name,chat_id,from_id,1,None)
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotEventsMaker.instance:
            BotEventsMaker.instance = BotEventsMaker.Singleton(token)
        return BotEventsMaker.instance 