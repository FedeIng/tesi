import telepot
from library import *
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Bot_admin:

    def __init__(self,token,admins):

        def message(msg):
            return None

        def query(msg):
            return None

        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':message,'callback_query':query})
        self.admins=admins

    def get_bot(self):
        return self.bot