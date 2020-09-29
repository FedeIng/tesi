import telepot

class Bot:

    def __init__(self,token,message=lambda msg : None,query=lambda msg : None):
        self.token=token
        self.bot=telepot.Bot(token)
        self.bot.message_loop({'chat':message,'callback_query':query})

    def get_bot(self):
        return self.bot

    def get_token(self):
        return self.token