class UsersEvent:
    
    def __init__(self,obj):
        self.class_name="UsersEvent"
        self.event=None
        self.users=[]
        if "event_obj" in obj:
            self.event=obj["event_obj"]
        if "event" in obj:
            self.event=Event(obj["event"])
        if "users_obj" in obj:
            for user_obj in obj['users_obj']:
                self.users.append(user_obj)
        if "users" in obj:
            for user in obj['users']:
                self.users.append(user)
    
    def __dict__(self):
        obj={
            "class_name":self.class_name,
            "event":None,
            "users":[]
        }
        if self.event!=None:
            obj["event"]=self.event.__dict__()
        if len(self.users)==0:
            obj["users"]=[]
            for user in self.users:
                obj["users"].append(user.__dict__())
        return obj
            