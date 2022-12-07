import telepot
from library import match_command, tag_group, selection, list_to_str, array_to_matrix, create_reply_keyboard, seg_bug, send_message, send_doc

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.bot_class import Bot
from databases.database_class import Database

class BotUser:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="user"
            super().__init__(token,message=self.message)

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"].lower()
            if content_type == 'text':
                txt=msg["text"]
                user=super().get_bot().getChat(from_id)
                if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]):
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
                else:
                    status=super().get_status(self.bot_name,chat_id,from_id)
                    if status!=None:
                        match status.id:
                            case 1:
                                match txt:
                                    case "Vorrei vedere l'elenco dei giochi disponibili":
                                        games=super().get_database().get_postgres().run_function("free_games_get")
                                        if games==[]:
                                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
                                        else:
                                            divisore='\n'
                                            send_message(super().get_bot(),from_id,tag_group(chat_type,user)+f"Lista dei giochi disponibili:\n{divisore.join(games)}")
                                            if chat_id!=from_id:
                                                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Lista inviata in privato.")
                                    case "Vorrei prendere un gioco":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi prendere?",reply_markup=super().set_keyboard(super().get_database().get_postgres().run_function("free_games_get")))
                                        super().set_status(self.bot_name,chat_id,from_id,2,None)
                                    case _:
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando non trovato, si prega di rieseguire il comando \start.")
                            case 2:
                                if super().get_database().get_postgres().run_function("rental_set"):
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Prenotazione presa con successo.")
                                else:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo la tua prenotazione non è andata a buon fine. Riesegui il comando \start e riprova.")

    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotUser.instance:
            BotUser.instance = BotUser.Singleton(token)
        return BotUser.instance 