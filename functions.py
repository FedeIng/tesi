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

def on_callback_query(msg):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if from_id not in id_command:
        id_command.append(from_id)
    bot.sendMessage(from_id, 'Bot in manutenzione, riprovare prossimamente')

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in id_command:
        id_command.append(chat_id)
    if content_type == 'text':
        txt=msg['text'].lower()
        for elem in array:
            if match(txt,elem,chat_type,bot_name):
                bot.sendMessage(chat_id, 'Bot in manutenzione, riprovare prossimamente')