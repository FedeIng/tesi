import telepot
from library import match_command, tag_group, selection, list_to_str, array_to_matrix, create_reply_keyboard, seg_bug, send_message, send_doc

from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from bots.bot_class import Bot
from databases.database_class import Database

class BotStaff:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="s"
            super().__init__(token,message=self.message)

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            if content_type == 'text' and from_id in super().get_database().get_postgres().run_function("telegram_id_staff_get"):
                txt=msg["text"].lower()
                user=super().get_bot().getChat(from_id)
                if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]):
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi prestati","Vorrei prestare un gioco","Vorrei restituire un gioco"]))
                    super().set_status(self.bot_name,chat_id,from_id,1,None)
                else:
                    status=super().get_status(self.bot_name,chat_id,from_id)
                    if status!=None:
                        match status.id:
                            case 1:
                                match txt:
                                    case "vorrei vedere l'elenco dei giochi prestati":
                                        rentals=super().get_database().get_postgres().run_function("rental_get")
                                        if games==[]:
                                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
                                        else:
                                            divisore='\n\n'
                                            send_message(super().get_bot(),from_id,f"Lista dei giochi prestati:\n\n{divisore.join(rentals)}")
                                            if chat_id!=from_id:
                                                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Lista inviata in privato.")
                                    case "vorrei prestare un gioco":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi prestare?")
                                        super().set_status(self.bot_name,chat_id,from_id,2,None)
                                    case "vorrei restituire un gioco":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi restituire?")
                                        super().set_status(self.bot_name,chat_id,from_id,3,None)
                                    case _:
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando non trovato, si prega di rieseguire il comando \start.")
                            case 2:
                                if txt in super().get_database().get_postgres().run_function("free_games_get"):
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che dati dell'utente vuoi salvare per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                                    super().set_status(self.bot_name,chat_id,from_id,4,Game({"name":txt}))
                                else:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo il gioco non è stato trovato. Riesegui il comando \start e riprova.")
                            case 3:
                                users=self.get_users_by_game(super().get_database().get_postgres().run_function("rental_get"),txt)
                                if users==[]:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando annullato, nessun utente ha preso in prestito questo gioco. Rilanciare il comando \start.")
                                elif len(users)==1:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"É stato restituito da\n{user_to_string(users[0])}?",reply_markup=super().set_keyboard(["Sì","No"]))
                                    super().set_status(self.bot_name,chat_id,from_id,5,Rental({"game_obj":status,"user_obj":User({"name":user[0]["user_name"],"surname":user[0]["user_surname"],"nickname":user[0]["user_nickname"],"telephone":user[0]["user_telephone"],"telegram_id":user[0]["user_telegram_id"]})}))
                                else:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"Da chi è stato restituito il gioco?",reply_markup=super().set_keyboard(self.get_users_array_strings(users)))
                                    super().set_status(self.bot_name,chat_id,from_id,6,status)
                            case 4:
                                match txt:
                                    case "nome":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il nome:")
                                    case "cognome":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il cognome:")
                                    case "nickname":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il nickname:")
                                    case "telefono":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il telefono:")
                                    case "ok":
                                        pass
                                    case "annulla":
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Registrazione annullata.")
                                    case _:
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando non trovato, si prega di rieseguire il comando \start.")
                            case 5:
                                match txt:
                                    case "sì":
                                        pass
                                    case "no":
                                        pass
                                    case _:
                                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando non trovato, si prega di rieseguire il comando \start.")
                            case 6:
                                pass

        def get_rentals_array_string(self,rentals):
            rental_array=[]
            for rental in rentals:
                rental_array.append(self.rental_to_string(rental))
            return rental_array

        def rental_to_string(self,rental):
            string=f"{rental['game_name']} ->"
            if rental['user_name']!=None:
                string+=f"\nNome:{rental['user_name']}"
            if rental['user_surname']!=None:
                string+=f"\nCognome:{rental['user_surname']}"
            if rental['user_nickname']!=None:
                string+=f"\nNickname:{rental['user_nickname']}"
            if rental['user_telegram_id']!=None:
                string+=f"\nTelegram:@{super().get_bot().getChat(rental['user_telegram_id'])['username']}"
            if rental['user_telephone']!=None:
                string+=f"\nTelefono:{rental['user_telephone']}"
            if rental['staff_name']!=None or rental['staff_surname']!=None or rental['staff_nickname']!=None or rental['staff_telegram_id']!=None or rental['staff_telephone']!=None:
                string+=f"\nPrestato da ->"
                if rental['staff_name']!=None:
                    string+=f"\nNome:{rental['staff_name']}"
                if rental['staff_surname']!=None:
                    string+=f"\nCognome:{rental['staff_surname']}"
                if rental['staff_nickname']!=None:
                    string+=f"\nNickname:{rental['staff_nickname']}"
                if rental['staff_telegram_id']!=None:
                    string+=f"\nTelegram:@{super().get_bot().getChat(rental['staff_telegram_id'])['username']}"
                if rental['staff_telephone']!=None:
                    string+=f"\nTelefono:{rental['staff_telephone']}"
            return string

        def get_users_array_strings(self,users):
            user_array=[]
            for user in users:
                user_array.append(self.user_to_string(user))
            return user_array

        def user_to_string(self,user):
            string=""
            if user.name!=None:
                string+=f"Nome:{user.name}"
            if user.surname!=None:
                if string!="":
                    string+="\n"
                string+=f"Cognome:{user.surname}"
            if user.nickname!=None:
                if string!="":
                    string+="\n"
                string+=f"Nickname:{user.nickname}"
            if user.telegram_id!=None:
                if string!="":
                    string+="\n"
                string+=f"Telegram:@{super().get_bot().getChat(user.telegram_id)['username']}"
            if user.telephone!=None:
                if string!="":
                    string+="\n"
                string+=f"Telefono:{user.telefono}"
            return string

        def get_users_by_game(self,rentals,game_name):
            users=[]
            for rental in rentals:
                if game_name==rental["game_name"]:
                    data={
                        "telegram_id":rental["user_telegram_id"],
                        "telephone":rental["user_telephone"],
                        "name":rental["user_name"],
                        "surname":rental["user_surname"],
                        "nickname":rental["nickname"]
                    }
                    users.append(User(data))
            return users

    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotStaff.instance:
            BotStaff.instance = BotStaff.Singleton(token)
        return BotStaff.instance