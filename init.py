import time
from tree_class import Tree
from database_class import Database
from bot_admin_class import BotAdmin
from bot_creation_class import BotCreation
from bot_getlink_class import BotGetlink
from bot_pwd_class import BotPwd
from bot_teacher_class import BotTeacher

database=Database()
bot_admin=BotAdmin()
bot_pwd=BotPwd()
database.set_bot_pwd(bot_pwd)
database.set_bot_admin(bot_admin)
tree=Tree()
bot_creation=BotCreation()
bot_getlink=BotGetlink()
teacher=database.get_teacher()
bot_teacher=BotTeacher()
database.set_bot_teacher(bot_teacher)

print("Init complete")

while True:
    time.sleep(10)