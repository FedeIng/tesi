from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import emoji

from library import tag_group, send_message
from bots.bot_class import Bot
from databases.database_class import Database

class BotLinks:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="li"
            super().__init__(token,message=self.message)

        def message(self,update,context):
            chat_id=update.message.chat_id
            from_id=update.message.from_id
            chat_type=update.message.chat_type
            content_type=update.message.content_type
            if content_type == 'text':
                txt=update.message.text.lower()
                user=super().get_bot().getChat(from_id)
                if self.match_command('/start',txt,chat_type,user):
                    bot_array=[]
                    send_message(super().get_bot(),chat_id,f"{tag_group(chat_type,user)} Benvenuto nel bot telegram della Gilda del Grifone, cosa bot vuoi usare?",reply_markup=super().set_keyboard(["Vorrei vedere l'elenco dei giochi disponibili","Vorrei prendere un gioco","Vorrei segnalare un bug"]))

        def make_button_bot_dict(self):
            button_bot_dict = {}
            button_bot_dict["user_games"] = InlineKeyboardButton(text=topic,url="https://t.me/"+self.tree.get_username_by_topic(topic)+"?start=foo")