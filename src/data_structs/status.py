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
                case _:
                    pass