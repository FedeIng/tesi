import datetime
import yaml

class Config:
    class Singleton:

        def __init__(self):
            with open('./config.yaml') as f:
                data=yaml.load(f, Loader=yaml.FullLoader)
                self.user_games_token=data['bots']['token']['user']['games']
                self.user_events_token=data['bots']['token']['user']['events']
                self.staff_token=data['bots']['token']['staff']
                self.logs_token=data['bots']['token']['logs']
                self.news_token=data['bots']['token']['news']
                self.links_token=data['bots']['token']['links']
                self.postgres_host=data['databases']['postgres']['host']
                self.postgres_database=data['databases']['postgres']['database']
                self.postgres_username=data['databases']['postgres']['username']
                self.postgres_password=data['databases']['postgres']['password']
                self.postgres_port=data['databases']['postgres']['port']
                self.postgres_schema=data['databases']['postgres']['schema']
                self.redis_host=data['databases']['redis']['host']
                self.redis_port=data['databases']['redis']['port']

        def get_user_games_token(self):
            return self.user_games_token
        
        def get_user_events_token(self):
            return self.user_events_token
        
        def get_staff_token(self):
            return self.staff_token

        def get_logs_token(self):
            return self.logs_token

        def get_news_token(self):
            return self.news_token

        def get_links_token(self):
            return self.links_token

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
        
        def get_postgres_schema(self):
            return self.postgres_schema

        def get_redis_host(self):
            return self.redis_host
        
        def get_redis_port(self):
            return self.redis_port
    
    instance = None
    def __new__(cls): # __new__ always a classmethod
        if not Config.instance:
            Config.instance = Config.Singleton()
        return Config.instance