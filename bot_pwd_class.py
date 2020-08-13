import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class BotPwd:

    def __init__(self,token):
        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':self.message,'callback_query':self.query})

    def message(self,msg):
        return None

    def query(self,msg):
        return None

    def get_bot(self):
        return self.bot