import datetime

class Database:
    class Singleton:

        def __init__(self):
            self.postgres=None
            self.redis=None
            self.bot_staff=None
            self.bot_events_maker=None
            self.bot_user_games=None
            self.bot_user_events=None
            self.bot_logs=None
            self.bot_news=None

        def set_postgres(self,db):
            self.postgres=db

        def get_postgres(self):
            return self.postgres
        
        def set_redis(self,db):
            self.redis=db

        def get_redis(self):
            return self.redis    

        def set_bot_staff(self,bot):
            self.bot_staff=bot

        def get_bot_staff(self):
            return self.bot_staff
        
        def set_bot_events_maker(self,bot):
            self.bot_event_maker=bot

        def get_bot_events_maker(self):
            return self.bot_event_maker
        
        def set_bot_user_games(self,bot):
            self.bot_user_game=bot

        def get_bot_user_games(self):
            return self.bot_user_game

        def set_bot_user_events(self,bot):
            self.bot_user_event=bot

        def get_bot_user_events(self):
            return self.bot_user_event
        
        def set_bot_logs(self,bot):
            self.bot_logs=bot
        
        def get_bot_logs(self):
            return self.bot_logs
        
        def set_bot_news(self,bot):
            self.bot_news=bot
        
        def get_bot_news(self):
            return self.bot_news
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Database.instance:
            Database.instance = Database.Singleton()
        return Database.instance