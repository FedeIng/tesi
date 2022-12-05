import datetime
import yaml

class Config:
    class Singleton:

        def __init__(self):
            with open('../config.yaml') as f:
                data=yaml.load(f, Loader=yaml.FullLoader)
                self.user_token=data['bots']['token']['user']
                self.admin_token=data['bots']['token']['staff']
                self.postgres_host=data['databases']['postgres']['host']
                self.postgres_database=data['databases']['postgres']['database']
                self.postgres_username=data['databases']['postgres']['username']
                self.postgres_password=data['databases']['postgres']['password']
                self.postgres_port=data['databases']['postgres']['port']
                self.postgres_schema=data['databases']['postgres']['schema']
                self.redis_host=data['databases']['redis']['host']
                self.redis_port=data['databases']['redis']['port']

        def get_user_token(self):
            return self.user_token
        
        def get_admin_token(self):
            return self.admin_token

        def get_postgres_host(self):
            return self.postgres_host

        def get_postgres_database(self):
            return self.postgres_database

        def get_postgres_username(self):
            return self.postgres_username

        def get_postgres_password(self):
            return self.postgres_password

        def get_postgres_port(self):
            return self.postgres_port

        def get_redis_host(self):
            return self.redis_host
        
        def get_redis_port(self):
            return self.redis_port
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Config.instance:
            Config.instance = Config.Singleton()
        return Config.instance