from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import emoji

from library import tag_group, send_message
from bots.bot_class import Bot

class BotLinks:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="li"
            self.button_bot_dict={
                "USER_GAMES":InlineKeyboardButton(text=emoji.emojize(f":video_game: Bot per prendere in prestito i giochi :video_game:"),url=self.create_link(super().get_database().get_bot_user_games())),
                "USER_EVENTS":InlineKeyboardButton(text=emoji.emojize(f":tada: Bot per partecipare agli eventi :tada:"),url=self.create_link(super().get_database().get_bot_user_events())),
                "STAFF":InlineKeyboardButton(text=emoji.emojize(f":man: Bot per lo staff :man:"),url=self.create_link(super().get_database().get_bot_staff())),
                "EVENT_MAKER":InlineKeyboardButton(text=emoji.emojize(f":construction_worker: Bot per la creazione di eventi :construction_worker:"),url=self.create_link(super().get_database().get_bot_staff())),
                "LOG":InlineKeyboardButton(text=emoji.emojize(f":writing_hand: Bot per la gestione dei log :writing_hand:"),url=self.create_link(super().get_database().get_bot_logs())),
                "NEWS":InlineKeyboardButton(text=emoji.emojize(f":newspaper: Bot per la gestione dei log :newspaper:"),url=self.create_link(super().get_database().get_bot_news()))
            }
            super().__init__(token,match_command_handler=self.match_command_handler)
            
        def create_link(self,bot):
            return f"https://t.me/{bot.get_bot().username}?start=foo"

        def match_command_handler(self,chat_id,from_id,chat_type,content_type,txt,user):
            if self.match_command('/start',txt,chat_type,user):
                user_powers=super().get_database().get_postgres().run_function("user_powers_get",str(user["id"]))
                bot_array=self.create_buttons_array(['USER_GAMES','USER_EVENTS','NEWS']+user_powers)
                send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa bot vuoi usare?",reply_markup=InlineKeyboardMarkup(bot_array))

        def create_buttons_array(self,button_list):
            btn_array=[]
            for elem in button_list:
                btn_array.append([self.button_bot_dict[elem]])
            return btn_array
        
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotLinks.instance:
            BotLinks.instance = BotLinks.Singleton(token)
        return BotLinks.instance