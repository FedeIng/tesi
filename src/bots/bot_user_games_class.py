from library import tag_group, send_message, send_document

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.bot_class import Bot
from databases.database_class import Database

class BotUserGames:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="ug"
            permissions=lambda user: super().get_database().get_postgres().run_function("user_set",str(user["id"]),f"'{user['first_name'].lower()}'",f"'{user['last_name'].lower()}'",f"'{user['username'].lower()}'")
            self.retry_string="Purtroppo la tua prenotazione non è andata a buon fine. Riesegui il comando /start e riprova."
            super().__init__(token,message=self.message,permissions=permissions)

        def send_notifies(self,rentals):
            for rental in rentals:
                send_message(super().get_bot(),rental["user_telegram_id"],f"Ricordati di restituire il gioco: {rental['game_name']}.")

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
                elif super().exec_match_command('/list',txt,chat_type,user):
                    self.command_one(chat_id,from_id,chat_type,user)
                elif super().exec_match_command('/rental',txt,chat_type,user):
                    self.command_two(chat_id,from_id,chat_type,user)
                elif super().exec_match_command('/bug',txt,chat_type,user):
                    self.command_three(chat_id,from_id,chat_type,user)
                else:
                    self.match_status(txt,chat_id,from_id,chat_type,user)
        
        def match_status(self,txt,chat_id,from_id,chat_type,user):
            status=super().get_status(self.bot_name,chat_id,from_id)
            if status!=None:
                match status.id:
                    case 1:
                        self.case_one(txt,chat_id,from_id,chat_type,user)
                    case 2:
                        self.case_two(txt,chat_id,from_id,chat_type,user)
                    case 3:
                        self.case_three(txt,chat_id,from_id,chat_type,user,status)
                    case 4:
                        super().send_bug(txt,chat_id,chat_type,user,self.bot_name)
                                
        def case_one(self,txt,chat_id,from_id,chat_type,user):
            match txt:
                case "vorrei vedere l'elenco dei giochi disponibili":
                    self.command_one(chat_id,from_id,chat_type,user)
                case "vorrei prendere un gioco":
                    self.command_two(chat_id,from_id,chat_type,user)
                case "vorrei segnalare un bug":
                    self.command_three(chat_id,from_id,chat_type,user)
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())

        def command_one(self,chat_id,from_id,chat_type,user):
            games=super().get_database().get_postgres().run_function("free_games_get")
            if games==[]:
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Nessun gioco prestato.")
            else:
                divisore='\n'
                send_document(super().get_bot(),from_id,divisore.join(sorted(games)),"Lista dei giochi disponibili.")
                if chat_id!=from_id:
                    send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Lista inviata in privato.")
        
        def command_two(self,chat_id,from_id,chat_type,user):
            games=super().get_database().get_postgres().run_function("rental_get_by_telegram_id",str(from_id))
            if games==[]:
                free_games=super().get_database().get_postgres().run_function("free_games_get")
                if free_games==[]:
                    send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Nessun gioco disponibile.")
                else:
                    send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Che gioco vuoi prendere?",reply_markup=super().set_keyboard(sorted(free_games)))
                    super().set_status(self.bot_name,chat_id,from_id,2,None)
            else:
                divisore='\n'
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Non puoi prendere un gico perchè hai già preso:\n{divisore.join(sorted(games))}")
        
        def command_three(self,chat_id,from_id,chat_type,user):
            send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Che bug vuoi segnalare?")
            super().set_status(self.bot_name,chat_id,from_id,4,None)
                        
        def case_two(self,txt,chat_id,from_id,chat_type,user):
            if super().get_database().get_postgres().run_function("free_games_check_by_name","'"+txt+"'") > 0:
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Vuoi prendere il gioco {txt}?",reply_markup=super().set_keyboard(["Sì","No"]))
                super().set_status(self.bot_name,chat_id,from_id,3,Game({"name":txt}))
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)

        def case_three(self,txt,chat_id,from_id,chat_type,user,status):
            match txt:
                case 'sì':
                    if super().get_database().get_postgres().run_function("user_rental_set",str(from_id),f"'{status.obj.name}'"):
                        send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Prenotazione presa con successo.")
                    else:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)
                case 'no':
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())

    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUserGames.instance:
            BotUserGames.instance = BotUserGames.Singleton(token)
        return BotUserGames.instance 