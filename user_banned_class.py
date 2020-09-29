from database_class import Database

class UserBanned:
    class Singleton:

        def __init__(self):
            self.database=Database()
            self.banned_user=self.database.read_ban()

        def add_ban(self,chat_id):
            if chat_id in self.banned_user:
                self.banned_user[chat_id]+=1
            else:
                self.banned_user[chat_id]=1
            self.write_ban()

        def del_ban(self,chat_id):
            if chat_id in self.banned_user:
                del self.banned_user[chat_id]
                self.write_ban()

        def check_ban(self,chat_id):
            if chat_id in self.banned_user and self.banned_user[chat_id]>99:
                return True
            return False

        def write_ban(self):
            self.database.write_ban(self.banned_user)

    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not UserBanned.instance:
            UserBanned.instance = UserBanned.Singleton()
        return UserBanned.instance