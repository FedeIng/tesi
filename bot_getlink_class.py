import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class BotGetlink:

    def __init__(self,token,tree):

        def message(msg):
            content_type, chat_type, chat_id = telepot.glance(msg)
            if content_type == 'text' and chat_type=="private":
                if msg["text"]=='/start':
                    self.bot.sendMessage(chat_id,"Select a bot:",reply_markup=self.create_url_inline_query())

        def query(msg):
            return None

        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':message,'callback_query':query})
        self.tree=tree

    def create_url_button(self,topic):
        return InlineKeyboardButton(text=topic,url="https://t.me/"+self.tree.get_username_by_topic(topic)+"?start=foo")

    def create_url_inline_query(self):
        data=[]
        for elem in self.tree.get_topic_list():
            data.append([self.create_url_button(elem)])
        return  InlineKeyboardMarkup(inline_keyboard=data)