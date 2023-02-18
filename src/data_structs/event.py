class Event:
    
    def __init__(self,obj):
        self.class_name="Event"
        self.name=None
        self.category=None
        self.date=None
        self.description=None
        self.maker=None
        if "name" in obj:
            self.name=obj["name"]
        if "category" in obj:
            self.category=obj["category"]
        if "date" in obj:
            self.name=obj["date"]
        if "description" in obj:
            self.description=obj["description"]
        if "maker_obj" in obj:
            self.maker=obj["maker_obj"]
        if "maker" in obj:
            self.maker=User(obj["maker"])
    
    def set_name(self,name):
        self.name=name 

    def get_name(self):
        if self.name == None:
            return "NULL"
        return f"'{self.name}'"
    
    def set_category(self,category):
        self.category=category

    def get_category(self):
        if self.category == None:
            return "NULL"
        return f"'{self.category}'"
    
    def set_date(self,date):
        self.date=date

    def get_date(self):
        if self.date == None:
            return "NULL"
        return f"'{self.date}'"
    
    def set_description(self,description):
        self.description=description

    def get_description(self):
        if self.description == None:
            return "NULL"
        return f"'{self.description}'"
            
    def __dict__(self):
        obj={
            "class_name":self.class_name,
            "name":self.name,
            "category":self.categpry,
            "date":self.date,
            "description":self.description,
            "maker":None
        }
        if self.maker!=None:
            obj["maker"]=self.maker.__dict__()
        return obj
            
        