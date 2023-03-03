import time
import schedule
from config_class import Config
from databases.database_class import Database
from databases.postgres_class import PostgresDb
from databases.redis_class import RedisDb
from bots.staff.bot_staff_games_class import BotStaffGames
from bots.staff.bot_staff_events_class import BotStaffEvents
from bots.user.bot_user_games_class import BotUserGames
from bots.user.bot_user_events_class import BotUserEvents
from bots.bot_logs_class import BotLogs
from bots.bot_news_class import BotNews

def work(bot_staff_games, bot_user_games, bot_events_maker, bot_user_events, database):
    rentals = database.get_postgres().run_function("rental_get_two_weeks")
    if len(rentals) > 0:
        bot_staff_games.send_notifies(rentals)
        bot_user_games.send_notifies(rentals)
    events = database.get_postgres().run_function("event_get_today")
    if len(events) > 0:
        bot_events_maker.send_notifies(events)
        bot_user_events.send_notifies(events)

if __name__ == "__main__":
    config=Config()

    database=Database()

    postgres=PostgresDb(config.get_postgres_host(),config.get_postgres_database(),config.get_postgres_username(),config.get_postgres_password(),config.get_postgres_port(),config.get_postgres_schema())
    database.set_postgres(postgres)
    redis=RedisDb(config.get_redis_host(),config.get_redis_port())
    database.set_redis(redis)

    bot_staff_games=BotStaffGames(config.get_staff_games_token())
    database.set_bot_staff_games(bot_staff_games)
    bot_staff_events=BotStaffEvents(config.get_staff_events_token())
    database.set_bot_staff_events(bot_staff_events)
    bot_events_maker=BotUserGames(config.get_events_maker_token())
    database.set_bot_events_maker(bot_events_maker)
    bot_user_games=BotUserGames(config.get_user_games_token())
    database.set_bot_user_games(bot_user_games)
    bot_user_events=BotUserEvents(config.get_user_events_token())
    database.set_bot_user_events(bot_user_events)
    bot_logs=BotLogs(config.get_logs_token())
    database.set_bot_logs(bot_logs)
    bot_news=BotNews(config.get_news_token())
    database.set_bot_news(bot_news)

    schedule.every().day.at("12:00").do(lambda: work(bot_staff_games, bot_user_games, bot_events_maker, bot_user_events, database))

    print("Init complete")

    while True:
        schedule.run_pending()
        time.sleep(10)
