class User:

    def __init__(self,obj):
        self.id=None
        self.telegram_id=None
        self.telephone=None
        self.name=None
        self.surname=None
        self.nickname=None
        self.is_staff=None
        if "id" in obj:
            self.id=obj["id"]
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
        if "is_staff" in obj:
            self.nickname=obj["is_staff"]