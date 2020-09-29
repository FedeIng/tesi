import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from bot_class import Bot
from database_class import Database
from tree_class import Tree
from bot_id_class import BotId
from library import send_message

class BotGetlink:
    class Singleton(Bot):

        def __init__(self):
            super().__init__(Database().get_getlink(),message=self.message)
            self.tree=Tree()
            self.Singleton=BotId()
            self.Singleton.set_bot("getlink",super().get_bot())
            self.Singleton.reset_key_id("getlink")

        def message(self,msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == 'text' and chat_type=="private" and msg["text"]=='/start':
                try:
                    self.Singleton.set_key_id(telepot.message_identifier(send_message(super().get_bot(),chat_id,"Select a bot:",reply_markup=self.create_url_inline_query())),"getlink")
                except TypeError:
                    pass

        def create_url_button(self,topic):
            return InlineKeyboardButton(text=topic,url="https://t.me/"+self.tree.get_username_by_topic(topic)+"?start=foo")

        def create_url_inline_query(self):
            data=[]
            for elem in self.tree.get_topic_list():
                data.append([self.create_url_button(elem)])
            return  InlineKeyboardMarkup(inline_keyboard=data)
        
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not BotGetlink.instance:
            BotGetlink.instance = BotGetlink.Singleton()
        return BotGetlink.instance