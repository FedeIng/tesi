class Game:

    def __init__(self,obj):
        self.class_name="Game"
        self.name=None
        self.number=None
        if "name" in obj:
            self.name=obj["name"]
        if "number" in obj:
            self.surname=obj["number"]