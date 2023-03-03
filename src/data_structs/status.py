from data_structs.game import Game
from data_structs.user import User
from data_structs.rental import Rental
from data_structs.event import Event

class Status:

    def __init__(self,id,dictionary=None,obj=None):
        self.id=id
        self.obj=None
        if obj!=None:
            self.obj=obj
        elif dictionary!=None:
            match dictionary["class_name"]:
                case "Game":
                    self.obj=User(dictionary)
                case "User":
                    self.obj=User(dictionary)
                case "Rental":
                    self.obj=Rental(dictionary)
                case "Event":
                    self.obj=Event(dictionary)

    def __dict__(self):
        obj={
                "id": self.id,
                "obj": None
            }
        if self.obj != None:
            obj["obj"]=self.obj.__dict__()
        return obj