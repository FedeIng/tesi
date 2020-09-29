import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from bot_class import Bot
from database_class import Database

class BotAdmin():
    class Singleton(Bot):

        def __init__(self):
            database = Database()
            admin=database.get_admin()
            super().__init__(admin["token"])
            self.admins=admin["admins"]

        def get_bot(self):
            return super().get_bot()
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotAdmin.instance:
            BotAdmin.instance = BotAdmin.Singleton()
        return BotAdmin.instance