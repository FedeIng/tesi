import datetime

class Database:
    class Singleton:

        def __init__(self):
            self.postgres=None
            self.redis=None
            self.bot_staff=None   
            self.bot_user=None

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
        
        def set_bot_user(self,bot):
            self.bot_user=bot

        def get_bot_user(self):
            return self.bot_user
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Database.instance:
            Database.instance = Database.Singleton()
        return Database.instance