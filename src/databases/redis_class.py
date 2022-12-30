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

        def set_object(self,bot_name,chat_id,from_id,obj):
            if chat_id==from_id:
                self.redis.set(f"{bot_name}-{str(chat_id)}",json.dumps(obj.__dict__()))
            else:
                self.redis.set(f"{bot_name}-{str(chat_id)}-{str(from_id)}",json.dumps(obj.__dict__()))
        
        def get_object(self,bot_name,chat_id,from_id):
            try:
                data=None
                if chat_id==from_id:
                    data=json.loads(self.redis.get(f"{bot_name}-{str(chat_id)}"))
                else:
                    data=json.loads(self.redis.get(f"{bot_name}-{str(chat_id)}-{str(from_id)}"))
                return Status(data["id"],dictionary=data["obj"])
            except TypeError as error:
                db.get_postgres().run_function("insert_exception",str(0),f"'TypeError'",f"'{error}'",str(6))
                send_logs("ERROR",error,0,recursive=True)
                return None

        def delete_object(self,bot_name,chat_id,from_id):
            if chat_id==from_id:
                self.redis.delete(f"{bot_name}-{str(chat_id)}")
            else:
                self.redis.delete(f"{bot_name}-{str(chat_id)}-{str(from_id)}")

        def get_and_delete_object(self,bot_name,chat_id,from_id):
            obj=self.get_object(bot_name,chat_id,from_id)
            self.delete_object(bot_name,chat_id,from_id)
            return obj
    
    instance = None
    def __new__(cls,host,port): # __new__ always a classmethod
        if not RedisDb.instance:
            RedisDb.instance = RedisDb.Singleton(host,port)
        return RedisDb.instance