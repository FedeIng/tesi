class User:

    def __init__(self,obj):
        self.class_name="User"
        self.telegram_id=None
        self.telephone=None
        self.name=None
        self.surname=None
        self.nickname=None
        if "telegram_id" in obj:
            self.telegram_id=obj["telegram_id"]
        if "telephone" in obj:
            self.telephone=obj["telephone"]
        if "name" in obj:
            self.name=obj["name"]
        if "surname" in obj:
            self.surname=obj["surname"]
        if "nickname" in obj:
            self.nickname=obj["nickname"]

    def set_telegram_id(self,telegram_id):
        self.telegram_id=telegram_id
    
    def get_telegram_id(self):
        if self.telegram_id == None:
            return "NULL"
        return f"'{str(self.telegram_id)}'"

    def set_telephone(self,telephone):
        self.telephone=telephone
    
    def get_telephone(self):
        if self.telephone == None:
            return "NULL"
        return f"'{self.telephone}'"

    def set_name(self,name):
        self.name=name
    
    def get_name(self):
        if self.name == None:
            return "NULL"
        return f"'{self.name}'"

    def set_surname(self,surname):
        self.surname=surname  
    
    def get_surname(self):
        if self.surname == None:
            return "NULL"
        return f"'{self.surname}'"

    def set_nickname(self,nickname):
        self.nickname=nickname 

    def get_nickname(self):
        if self.nickname == None:
            return "NULL"
        return f"'{self.nickname}'"

    def __dict__(self):
        return {
            "class_name":self.class_name,
            "telegram_id":self.telegram_id,
            "telephone":self.telephone,
            "name":self.name,
            "surname":self.surname,
            "nickname":self.nickname
        }