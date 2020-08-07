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
from tree_class import *
from urllib.request import urlopen
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from firebase import firebase
from database_class import *
from bot_admin_class import * 
from bot_creation_class import * 
from bot_getlink_class import * 
from bot_pwd_class import * 
from bot_teacher_class import * 

database = Database()
print("Database created")
admin=database.get_admin()
bot_admin=BotAdmin(admin['token'],admin['admins'])
print("Admin created")
pwd=database.get_pwd()
bot_pwd=BotPwd(pwd)
print("Pwd created")
database.set_bot_pwd(bot_pwd)
database.set_bot_admin(bot_admin)
tree=Tree(database)
print("Tree created")
creation=database.get_creation()
bot_creation=BotCreation(creation,tree)
print("Creation created")
getlink=database.get_getlink()
bot_getlink=BotGetlink(getlink,tree)
print("Getlink created")
teacher=database.get_teacher()
bot_teacher=BotTeacher(teacher,tree)
print("Teacher created")
database.set_bot_teacher(bot_teacher)

while True:
    time.sleep(10)