import datetime
import json

from data_structs.status import Status
from redis import Redis

class RedisDb:
    class Singleton:

        def __init__(self,host,port):
            self.host=host
            self.port=port
            self.redis=Redis(host=host,port=port)

        def set_object(self,id,obj):
            self.redis.set(str(id),json.dumps(obj.__dict__))
        
        def get_object(self,id):
            try:
                return Status(json.loads(self.redis.get(str(id))))
            except TypeError:
                return None

        def delete_object(self,id):
            self.redis.delete(str(id))

        def get_and_delete_object(self,id):
            obj=self.get_object(id)
            self.delete_object(id)
            return obj
    
    instance = None
    def __new__(cls,host,port): # __new__ always a classmethod
        if not RedisDb.instance:
            RedisDb.instance = RedisDb.Singleton(host,port)
        return RedisDb.instance