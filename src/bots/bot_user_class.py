import telepot
from library import match_command, tag_group, send_message, send_document

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.bot_class import Bot
from databases.database_class import Database

class BotUser:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="u"
            self.retry_string="Purtroppo la tua prenotazione non è andata a buon fine. Riesegui il comando /start e riprova."
            super().__init__(token,message=self.message)

        def send_notifies(self,rentals):
            for rental in rentals:
                send_message(super().get_bot(),rental["user_telegram_id"],"Ricordati di restituire il gioco: "+rental["game_name"]+".")

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            if content_type == 'text':
                txt=msg["text"].lower()
                user=super().get_bot().getChat(from_id)
                if self.match_command('/start',txt,chat_type,user):
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco","Vorrei segnalare un bug"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
                elif self.match_command('/list',txt,chat_type,user):
                    self.command_one(chat_id,from_id,chat_type,user)
                elif self.match_command('/rental',txt,chat_type,user):
                    self.command_two(chat_id,from_id,chat_type,user)
                elif self.match_command('/bug',txt,chat_type,user):
                    self.command_three(chat_id,from_id,chat_type,user)
                else:
                    self.match_status(txt,chat_id,from_id,chat_type,user)

        def match_command(self,command,txt,chat_type,user):
            return match_command(command,txt,chat_type,super().get_bot().getMe()["username"]) and super().get_database().get_postgres().run_function("user_set",str(user["id"]),"'"+user["first_name"].lower()+"'","'"+user["last_name"].lower()+"'","'"+user["username"].lower()+"'")
        
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
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
            else:
                divisore='\n'
                send_document(super().get_bot(),from_id,divisore.join(sorted(games)),"Lista dei giochi disponibili.")
                if chat_id!=from_id:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Lista inviata in privato.")
        
        def command_two(self,chat_id,from_id,chat_type,user):
            games=super().get_database().get_postgres().run_function("rental_get_by_telegram_id",str(from_id))
            if games==[]:
                free_games=super().get_database().get_postgres().run_function("free_games_get")
                if free_games==[]:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco disponibile.")
                else:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi prendere?",reply_markup=super().set_keyboard(sorted(free_games)))
                    super().set_status(self.bot_name,chat_id,from_id,2,None)
            else:
                divisore='\n'
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"Non puoi prendere un gico perchè hai già preso:\n{divisore.join(sorted(games))}")
        
        def command_three(self,chat_id,from_id,chat_type,user):
            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che bug vuoi segnalare?")
            super().set_status(self.bot_name,chat_id,from_id,4,None)
                        
        def case_two(self,txt,chat_id,from_id,chat_type,user):
            if super().get_database().get_postgres().run_function("free_games_check_by_name","'"+txt+"'") > 0:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"Vuoi prendere il gioco {txt}?",reply_markup=super().set_keyboard(["Sì","No"]))
                super().set_status(self.bot_name,chat_id,from_id,3,Game({"name":txt}))
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)

        def case_three(self,txt,chat_id,from_id,chat_type,user,status):
            match txt:
                case 'sì':
                    if super().get_database().get_postgres().run_function("user_rental_set",str(from_id),"'"+status.obj.name+"'"):
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Prenotazione presa con successo.")
                    else:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)
                case 'no':
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+self.retry_string)
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())

    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUser.instance:
            BotUser.instance = BotUser.Singleton(token)
        return BotUser.instance 