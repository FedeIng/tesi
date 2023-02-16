from library import match_command, tag_group, send_message, send_document

from bots.bot_class import Bot
from databases.database_class import Database

class BotUserEvents:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="ue"
            super().__init__(token,message=self.message)

        def message(self,update,context):
            chat_id=update.message.chat_id
            from_id=update.message.from_id
            chat_type=update.message.chat_type
            content_type=update.message.content_type
            if content_type == 'text':
                txt=update.message.text.lower()
                user=super().get_bot().getChat(from_id)
                if super().exec_match_command('/start',txt,chat_type,user):
                    send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco","Vorrei segnalare un bug"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUserEvents.instance:
            BotUserEvents.instance = BotUserEvents.Singleton(token)
        return BotUserEvents.instance 