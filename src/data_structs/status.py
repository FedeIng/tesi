class Status:

    def __init__(self,obj):
        self.id=None
        self.obj=None
        if "id" in obj:
            self.id=obj["id"]
        if "data" in obj:
            match obj["data"]["class_name"]:
                case "Game":
                     self.obj=User(obj["data"])
                case "User":
                     self.obj=User(obj["data"])
                case "Rental":
                     self.obj=Rental(obj["data"])
                case _:
                    pass