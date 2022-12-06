from data_structs.game import Game
from data_structs.user import User

class Rental:

    def __init__(self,obj):
        self.id=None
        self.game=None
        self.user=None
        self.staff=None
        if "id" in obj:
            self.id=obj["id"]
        if "game" in obj:
            self.game=Game(obj["game"])
        if "user" in obj:
            self.user=User(obj["user"])
        if "staff" in obj:
            self.user=User(obj["staff"])