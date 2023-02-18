import re
from library import tag_group, send_message, send_document, match_command

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.staff.bot_staff_class import BotStaff

class BotStaffEvents:
    class Singleton(BotStaff):

        def __init__(self,token):
            self.bot_name="se"
            super().__init__(token,match_command_handler=self.match_command_handler,match_status=self.match_status)

        def send_notifies(self,rentals):
            staff_array = super().get_database().get_postgres().run_function("telegram_id_staff_get")
            for staff in staff_array:
                divisore='\n\n'
                send_message(super().get_bot(),staff,f"Lista dei giochi prestati in ritardo di restituzione:\n\n{divisore.join(self.get_rentals_array_string(rentals))}")

        def match_command_handler(self,chat_id,from_id,chat_type,content_type,txt,user):
            if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]):
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco di tutti i creatori di eventi","Vorrei promuovere un utente a creatore di eventi","Vorrei rimuovere il ruolo creatore di eventi a un utente"]))
                super().set_status(self.bot_name,chat_id,from_id,1,None)
            elif match_command('/list',txt,chat_type,super().get_bot().getMe()["username"]):
                return
            elif match_command('/promote',txt,chat_type,super().get_bot().getMe()["username"]):
                return
            elif match_command('/remove',txt,chat_type,super().get_bot().getMe()["username"]):
                return
            else:
                self.match_status(txt,chat_id,from_id,chat_type,user)
                
        def match_status(self,txt,chat_id,from_id,chat_type,user,status):
            match status.id:
                case 1:
                    return
        
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotStaffEvents.instance:
            BotStaffEvents.instance = BotStaffEvents.Singleton(token)
        return BotStaffEvents.instance