import time
import schedule
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

bot_staff=BotStaff(config.staff_token)
database.set_bot_staff(bot_staff)
bot_user=BotUser(config.user_token)
database.set_bot_staff(bot_user)

def work():
    global bot_staff
    global bot_user
    global database

    rentals = database.get_postgres().run_function("rental_get_two_weeks")
    if len(rentals) > 0:
        bot_staff.send_notifies(rentals)
        bot_user.send_notifies(rentals)

schedule.every().day.at("12:00").do(work)

print("Init complete")

while True:
    schedule.run_pending()
    time.sleep(10)