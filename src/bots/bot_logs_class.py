from bots.bot_class import Bot

class BotLogs:
    class Singleton(Bot):

        def __init__(self,token):
            self.bot_name="lo"
            super().__init__(token,permissions=self.permissions)
            
        def permissions(self,user):
            return super().get_database().get_postgres().run_function("telegram_id_log_check",str(user["id"]))
    
    instance = None
    def __new__(cls,token): # __new__ always a classmethod
        if not BotLogs.instance:
            BotLogs.instance = BotLogs.Singleton(token)
        return BotLogs.instance