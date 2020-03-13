def match(msg,command,chat_type,bot_name):
    print(1)
    print(msg+" : "+command+" : "+chat_type+" : "+bot_name)
    if (chat_type=="group" or chat_type=="supergroup") and msg==command+"@"+bot_name:
        print(2)
        return True
    elif chat_type=="private" and msg==command:
        print(3)
        return True
    print(4)
    return False