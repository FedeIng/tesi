import time
from config_class import Config
from databases.database_class import Database
from databases.postgres_class import PostgresDb
from databases.redis_class import RedisDb
from bots.bot_staff_class import BotStaff
from bots.bot_user_class import BotUser

config=Config()

database=Database()

postgres=PostgresDb(config.postgres_host,config.postgres_database,config.postgres_username,config.postgres_password,config.postgres_port,config.postgres_schema)
database.set_postgres(postgres)
redis=RedisDb(config.redis_host,config.redis_port)
database.set_redis(redis)

#bot_staff=BotStaff()
#database.set_bot_staff(bot_staff)
#bot_user=BotTeacher()
#database.set_bot_staff(bot_user)

print("Init complete")

while True:
    time.sleep(10)