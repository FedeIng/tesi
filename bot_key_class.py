import telepot
from database_class import Database

class BotKey:
    class Singleton:

        def __init__(self):
            self.database=Database()
            self.key_id=self.database.get_key_id()