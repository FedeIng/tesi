from bots.bot_class import Bot

class BotLogs:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="l"
            super().__init__(token)
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotLogs.instance:
            BotLogs.instance = BotLogs.Singleton(token)
        return BotLogs.instance