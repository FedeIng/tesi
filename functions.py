def match(msg,command,chat_type,bot_name,chat_id,lista,boolean):
    if (boolean and chat_id not in lista) or ((not boolean) and chat_id in lista):
        if (chat_type=="group" or chat_type=="supergroup") and msg=="/start@"+bot_name:
            bot.sendMessage(chat_id,"Permesso negato")
        elif chat_type=="private" and msg=="/start":
            bot.sendMessage(chat_id,"Permesso negato")
        return False
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

def MsgMan(msg,array,id_command):
    content_type, chat_type, chat_id = telepot.glance(msg)
    if chat_id not in id_command:
        id_command.append(chat_id)
    if content_type == 'text':
        txt=msg['text'].lower()
        for elem in array:
            if match(txt,elem,chat_type,bot_name):
                bot.sendMessage(chat_id, 'Bot in manutenzione, riprovare prossimamente')
    return id_command

def CallBackMan(msg,id_command):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if from_id not in id_command:
        id_command.append(from_id)
    bot.sendMessage(from_id, 'Bot in manutenzione, riprovare prossimamente')
    return id_command

def add_id(array,from_id,chat_id,val):
    if from_id==chat_id:
        if chat_id not in array:
            array[chat_id]=val
    else :
        if chat_id not in array:
            array[chat_id]={}
            array[chat_id][from_id]=val
        else :
            if from_id not in array[chat_id]:
                array[chat_id][from_id]=val
    return array

def check_id(array,from_id,chat_id):
    ret_val=0
    if from_id==chat_id:
        if chat_id in array:
            ret_val=array[chat_id]
    else :
        if chat_id in array:
            if from_id in array[chat_id]:
                ret_val=array[chat_id][from_id]
    return ret_val

def del_id(array,from_id,chat_id):
    if from_id==chat_id:
        if chat_id in array:
            del array[chat_id]
    else :
        if chat_id in array:
            if from_id in array[chat_id]:
                del array[chat_id][from_id]
            if len(array[chat_id])==0:
                del array[chat_id]
    return array