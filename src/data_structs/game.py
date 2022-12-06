class Game:

    def __init__(self,obj):
        self.class_name="Game"
        self.id=None
        self.name=None
        self.number=None
        if "id" in obj:
            self.id=obj["id"]
        if "name" in obj:
            self.name=obj["name"]
        if "number" in obj:
            self.surname=obj["number"]