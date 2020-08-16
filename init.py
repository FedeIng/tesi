import telepot
import json
import sys
import re
import time
import hashlib, binascii, os
import random
import string
import datetime
from telepot.loop import MessageLoop
from tree_class import Tree
from urllib.request import urlopen
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from firebase import firebase
from database_class import Database
from bot_admin_class import BotAdmin
from bot_creation_class import BotCreation
from bot_getlink_class import BotGetlink
from bot_pwd_class import BotPwd
from bot_teacher_class import BotTeacher

database = Database()
admin=database.get_admin()
bot_admin=BotAdmin(admin['token'],admin['admins'])
pwd=database.get_pwd()
bot_pwd=BotPwd(pwd)
database.set_bot_pwd(bot_pwd)
database.set_bot_admin(bot_admin)
tree=Tree(database)
creation=database.get_creation()
bot_creation=BotCreation(creation,tree)
getlink=database.get_getlink()
bot_getlink=BotGetlink(getlink,tree)
teacher=database.get_teacher()
bot_teacher=BotTeacher(teacher,tree)
database.set_bot_teacher(bot_teacher)

print("Init complete")

while True:
    time.sleep(10)