from bots.bot_class import Bot

class BotNews:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="lo"
            super().__init__(token)
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotNews.instance:
            BotNews.instance = BotNews.Singleton(token)
        return BotNews.instance