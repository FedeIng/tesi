class Game:

    def __init__(self,obj):
        self.class_name="Game"
        self.name=None
        if "name" in obj:
            self.name=obj["name"]
    
    def get_name():
        return self.name

    def __dict__(self):
        return {
            "class_name":self.class_name,
            "name":self.name
        }