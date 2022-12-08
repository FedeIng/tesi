from data_structs.game import Game
from data_structs.user import User

class Rental:

    def __init__(self,obj):
        self.class_name="Rental"
        self.game=None
        self.user=None
        self.staff=None
        if "game_obj" in obj:
            self.game=obj["game_obj"]
        if "game" in obj:
            self.game=Game(obj["game"])
        if "user_obj" in obj:
            self.user=obj["user_obj"]
        if "user" in obj:
            self.user=User(obj["user"])
    
    def __dict__(self):
        obj={
            "class_name": self.class_name,
            "game": None,
            "user": None
        }
        if self.game != None:
            obj["game"]=self.game.__dict__()
        if self.user != None:
            obj["user"]=self.user.__dict__()
        return obj