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