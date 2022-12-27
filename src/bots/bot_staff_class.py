import telepot
import re
from library import match_command, tag_group, send_message, send_document

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

        def send_notifies(self,rentals):
            staff_array = super().get_database().get_postgres().run_function("telegram_id_staff_get")
            for staff in staff_array:
                divisore='\n\n'
                send_message(super().get_bot(),staff,f"Lista dei giochi prestati in ritardo di restituzione:\n\n{divisore.join(self.get_rentals_array_string(rentals))}")

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            from_id=msg["from"]["id"]
            if content_type == 'text':
                if super().get_database().get_postgres().run_function("telegram_id_staff_check",str(from_id)):
                    txt=msg["text"].lower()
                    user=super().get_bot().getChat(from_id)
                    if match_command('/start',txt,chat_type,super().get_bot().getMe()["username"]):
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Benvenuto nel bot telegram della Gilda del Grifone, cosa vuoi fare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi prestati","Vorrei prestare un gioco","Vorrei restituire un gioco","Vorrei segnalare un bug"]))
                        super().set_status(self.bot_name,chat_id,from_id,1,None)
                    else:
                        status=super().get_status(self.bot_name,chat_id,from_id)
                        if status!=None:
                            match status.id:
                                case 1:
                                    self.case_one(txt,chat_id,from_id,chat_type,user)
                                case 2:
                                    self.case_two(txt,chat_id,from_id,chat_type,user)
                                case 3:
                                    self.case_three(txt,chat_id,from_id,chat_type,user)
                                case 4:
                                    self.case_four(txt,chat_id,from_id,chat_type,user,status)
                                case 5:
                                    self.case_five(txt,chat_id,from_id,chat_type,user,status)
                                case 6:
                                    self.case_six(txt,chat_id,from_id,chat_type,user,status)
                                case 7:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nome salvato. Vuoi salvare altri dati per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                                    status.obj.user.set_name(txt)
                                    super().set_status(self.bot_name,chat_id,from_id,4,status.obj)
                                case 8:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Cognome salvato. Vuoi salvare altri dati per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                                    status.obj.user.set_surname(txt)
                                    super().set_status(self.bot_name,chat_id,from_id,4,status.obj)
                                case 9:
                                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nickname salvato. Vuoi salvare altri dati per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                                    status.obj.user.set_nickname(txt)
                                    super().set_status(self.bot_name,chat_id,from_id,4,status.obj)
                                case 10:
                                    self.case_ten(txt,chat_id,from_id,chat_type,user,status)
                elif chat_type=="private":
                    send_message(super().get_bot(),chat_id,"Non hai i permessi per usare questo bot.")

        def case_one(self,txt,chat_id,from_id,chat_type,user):
            match txt:
                case "vorrei vedere l'elenco dei giochi prestati":
                    rentals=super().get_database().get_postgres().run_function("rental_get")
                    if rentals==[]:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
                    else:
                        divisore='\n\n'
                        send_document(super().get_bot(),from_id,divisore.join(self.get_rentals_array_string(rentals)),"Lista dei giochi prestati.")
                        if chat_id!=from_id:
                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Lista inviata in privato.")
                case "vorrei prestare un gioco":
                    games=super().get_database().get_postgres().run_function("free_games_get")
                    if games==[]:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco disponibile.")
                    else:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi prestare?",reply_markup=super().set_keyboard(sorted(games)))
                        super().set_status(self.bot_name,chat_id,from_id,2,None)
                case "vorrei restituire un gioco":
                    games=super().get_database().get_postgres().run_function("game_name_rental_get")
                    if games==[]:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun gioco prestato.")
                    else:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che gioco vuoi restituire?",reply_markup=super().set_keyboard(games))
                        super().set_status(self.bot_name,chat_id,from_id,3,None)
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())
        
        def case_two(self,txt,chat_id,from_id,chat_type,user):
            if txt in super().get_database().get_postgres().run_function("free_games_get"):
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Che dati dell'utente vuoi salvare per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                super().set_status(self.bot_name,chat_id,from_id,4,Rental({"game":{"name":txt},"user":{}}))
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo il gioco non è stato trovato. Riesegui il comando /start e riprova.")

        def case_three(self,txt,chat_id,from_id,chat_type,user):
            users=super().get_database().get_postgres().run_function("user_rental_get_by_game_name","'"+txt+"'")
            if users==[]:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Comando annullato, nessun utente ha preso in prestito questo gioco. Rilanciare il comando /start.")
            elif len(users)==1:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"É stato prestato a {self.user_to_string(users[0])}?",reply_markup=super().set_keyboard(["Sì","No"]))
                super().set_status(self.bot_name,chat_id,from_id,5,Rental({"game_obj":Game({"name":txt}),"user_obj":User({"name":users[0]["name"],"surname":users[0]["surname"],"nickname":users[0]["nickname"],"telephone":users[0]["telephone"],"telegram_id":users[0]["telegram_id"]})}))
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+f"A chi è stato prestato il gioco?",reply_markup=super().set_keyboard(self.get_users_array_strings(users)))
                super().set_status(self.bot_name,chat_id,from_id,6,Game({"name":txt}))

        def case_four(self,txt,chat_id,from_id,chat_type,user,status):
            match txt:
                case "nome":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il nome:")
                    super().set_status(self.bot_name,chat_id,from_id,7,status.obj)
                case "cognome":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il cognome:")
                    super().set_status(self.bot_name,chat_id,from_id,8,status.obj)
                case "nickname":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il nickname:")
                    super().set_status(self.bot_name,chat_id,from_id,9,status.obj)
                case "telefono":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Digitare il telefono:")
                    super().set_status(self.bot_name,chat_id,from_id,10,status.obj)
                case "ok":
                    if status.obj.user.get_name() == "NULL" or status.obj.user.get_surname() == "NULL" or status.obj.user.get_telephone() == "NULL":
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nome, cognome e telefono necessari per la prenotazione.\nChe altri dati per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                        super().set_status(self.bot_name,chat_id,from_id,4,status.obj)
                    else:
                        if super().get_database().get_postgres().run_function("staff_rental_set",str(from_id),status.obj.game.get_name(),status.obj.user.get_name(),status.obj.user.get_surname(),status.obj.user.get_nickname(),status.obj.user.get_telephone()):
                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Prenotazione presa con successo.")
                        else:
                            send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo la prenotazione non è andata a buon fine. Riesegui il comando /start e riprova.")
                case "annulla":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Registrazione annullata.")
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())

        def case_five(self,txt,chat_id,from_id,chat_type,user,status):
            match txt:
                case "sì":
                    if super().get_database().get_postgres().run_function("restitution_set",status.obj.user.get_telephone(),status.obj.user.get_telegram_id()):
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Restituzione avvenuta con successo.")
                    else:
                        send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo la restituzione è fallita, si prega di rieseguire il comando /start.")
                case "no":
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Nessun altro utente trovato con questo prestito, comando annullato.")
                case _:
                    send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+super().get_error_string())

        def case_six(self,txt,chat_id,from_id,chat_type,user,status):
            if super().get_database().get_postgres().run_function("rental_set_by_full_name",status.obj.get_name(),"'"+txt+"'"):
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Restituzione avvenuta con successo.")
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Purtroppo la restituzione è fallita, si prega di rieseguire il comando /start.")

        def case_ten(self,txt,chat_id,from_id,chat_type,user,status):
            if re.search("^(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$", txt):
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Telefono salvato. Vuoi salvare altri dati per questa prenotazione?",reply_markup=super().set_keyboard(["Nome","Cognome","Nickname","Telefono","Ok","Annulla"]))
                status.obj.user.set_telephone(txt)
                super().set_status(self.bot_name,chat_id,from_id,4,status.obj)
            else:
                send_message(super().get_bot(),chat_id,tag_group(chat_type,user)+"Il numero non è valido. Riprova.")
                super().set_status(self.bot_name,chat_id,from_id,10,status.obj)

        def get_rentals_array_string(self,rentals):
            rental_array=[]
            for rental in rentals:
                rental_array.append(self.rental_to_string(rental))
            return sorted(rental_array)

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
                string+=self.staff_rental_to_string(rental)
            return string

        def staff_rental_to_string(self,rental):
            string=f"\nPrestato da ->"
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
            if user["name"]!=None:
                string+=user["name"]
            if user["surname"]!=None:
                if string!="":
                    string+=" "
                string+=user["surname"]
            if user["nickname"]!=None:
                if string!="":
                    string+=" "
                string+='('+user["nickname"]+')'
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