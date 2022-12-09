import telepot
from library import match_command, tag_group, send_message

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.bot_class import Bot
from databases.database_class import Database

class BotUser:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="u"
            super().__init__(token,message=self.message)

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            if content_type == 'text':
                txt=msg["text"].lower()
                user=super().get_bot().getChat(from_id)
                if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]) and super().get_database().get_postgres().run_function("user_set",str(user["id"]),"'"+user["first_name"].lower()+"'","'"+user["last_name"].lower()+"'","'"+user["username"]+"'"):
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
                else:
                    status=super().get_status(self.bot_name,chat_id,from_id)
                    if status!=None:
                        match status.id:
                            case 1:
                                match txt:
                                    case "vorrei vedere l'elenco dei giochi disponibili":
                                        games=super().get_database().get_postgres().run_function("free_games_get")
                                        if games==[]:
                                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
                                        else:
                                            divisore='\n'
                                            send_message(super().get_bot(),from_id,tag_group(chat_type,user)+f"Lista dei giochi disponibili:\n{divisore.join(sorted(games))}")
                                            if chat_id!=from_id:
                                                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Lista inviata in privato.")
                                    case "vorrei prendere un gioco":
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
                                    case _:
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando non trovato, si prega di rieseguire il comando \start.")
                            case 2:
                                if super().get_database().get_postgres().run_function("user_rental_set",str(from_id),"'"+txt+"'"):
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Prenotazione presa con successo.")
                                else:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo la tua prenotazione non è andata a buon fine. Riesegui il comando \start e riprova.")

    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUser.instance:
            BotUser.instance = BotUser.Singleton(token)
        return BotUser.instance 