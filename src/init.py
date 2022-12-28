import time
import schedule
from config_class import Config
from databases.database_class import Database
from databases.postgres_class import PostgresDb
from databases.redis_class import RedisDb
from bots.bot_staff_class import BotStaff
from bots.bot_user_class import BotUser
from bots.bot_logs_class import BotLogs

def work(bot_staff, bot_user, database):
    rentals = database.get_postgres().run_function("rental_get_two_weeks")
    if len(rentals) > 0:
        bot_staff.send_notifies(rentals)
        bot_user.send_notifies(rentals)

if __name__ == "__main__":
    config=Config()

    database=Database()

    postgres=PostgresDb(config.get_postgres_host(),config.get_postgres_database(),config.get_postgres_username(),config.get_postgres_password(),config.get_postgres_port(),config.get_postgres_schema())
    database.set_postgres(postgres)
    redis=RedisDb(config.get_redis_host(),config.get_redis_port())
    database.set_redis(redis)

    bot_staff=BotStaff(config.get_staff_token())
    database.set_bot_staff(bot_staff)
    bot_user=BotUser(config.get_user_token())
    database.set_bot_staff(bot_user)
    bot_logs=BotLogs(config.get_logs_token())
    database.set_bot_logs(bot_logs)

    schedule.every().day.at("12:00").do(lambda: work(bot_staff, bot_user, database))

    print("Init complete")

    while True:
        schedule.run_pending()
        time.sleep(10)
