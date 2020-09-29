import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from bot_class import Bot
from database_class import Database

class BotPwd:
    class Singleton(Bot):

        def __init__(self):
            super().__init__(Database().get_pwd())

        def get_bot(self):
            return super().get_bot()
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotPwd.instance:
            BotPwd.instance = BotPwd.Singleton()
        return BotPwd.instance