import telepot
import time
from filelock import Timeout, FileLock

lockM = FileLock("mode.txt.lock")

def post_0(Name,LockName,val):
    print("Set val "+val+" to "+Name)
    with LockName:
        with open(Name,'w') as f:
            f.write(val)

def post_1(Name,LockName,Vett,bot,socket=None):
    mode_type=""
    mode_change="CHANGE MODE"
    with lockM:
        with open('mode.txt','r') as f:
            mode=f.read()
            if len(Name)==11:
                mode_type="man"
            elif len(Name)==10:
                mode_type="std"
            if mode==mode_type:
                if socket!=None:
                    socket.send(mode_change.encode())
                for id in Vett:
                    if len(Name)==11:
                        bot.sendMessage(id, 'Il bot sta entrando in modalitá manutenzione, alcune funzioni potrebbero non essere abilitate')
                    elif len(Name)==10:
                        bot.sendMessage(id, 'Il bot é di nuovo operativo')
                    else :
                        print("Error in post_1")
                post_0(Name,LockName,"1")
                return False
            return True

def wait(Name,LockName):
    num_closed="0"
    while num_closed!="1":
        time.sleep(10)
        with LockName:
            with open(Name,'r') as f:
                num_closed=f.read()

def match(msg,command,chat_type,chat_id,lista,boolean,bot):
    if (boolean and chat_id not in lista) or ((not boolean) and chat_id in lista):
        if command=="/start":
            bot["bot"].sendMessage(chat_id,"Permesso negato")
        return False
    print(1)
    print(msg+" : "+command+" : "+chat_type+" : "+bot["name"])
    if (chat_type=="group" or chat_type=="supergroup") and msg==command+"@"+bot["name"]:
        print(2)
        return True
    elif chat_type=="private" and msg==command:
        print(3)
        return True
    print(4)
    return False

def msg_man(msg,array,id_command,bot,bot_name):
    content_type, chat_type, chat_id = telepot.glance(msg)
    bot_array={}
    bot_array["bot"]=bot
    bot_array["name"]=bot_name
    if chat_id not in id_command:
        id_command.append(chat_id)
    if content_type == 'text':
        txt=msg['text'].lower()
        for elem in array:
            if match(txt,elem,chat_type,chat_id,[],False,bot_array):
                bot.sendMessage(chat_id, 'Bot in manutenzione, riprovare prossimamente')
    return id_command

def callback_man(msg,id_command,bot):
    query_id, from_id, query_data = telepot.glance(msg, flavor="callback_query")
    if from_id not in id_command:
        id_command.append(from_id)
    bot.sendMessage(from_id, 'Bot in manutenzione, riprovare prossimamente')
    return id_command

def add_id(array,from_id,chat_id,val):
    if from_id==chat_id:
        array[chat_id]=val
    else :
        if chat_id not in array:
            array[chat_id]={}
            array[chat_id][from_id]=val
        else :
            array[chat_id][from_id]=val
    return array

def check_id(array,from_id,chat_id):
    ret_val=0
    if from_id==chat_id:
        if chat_id in array:
            ret_val=array[chat_id]
    else :
        if chat_id in array and from_id in array[chat_id]:
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