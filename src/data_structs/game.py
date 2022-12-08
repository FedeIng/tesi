class Game:

    def __init__(self,obj):
        self.class_name="Game"
        self.name=None
        self.number=None
        if "name" in obj:
            self.name=obj["name"]
        if "number" in obj:
            self.surname=obj["number"]
    
    def __dict__(self):
        return {
            "class_name":self.class_name,
            "name":self.name,
            "number":self.number
        }