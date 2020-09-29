import sys
from firebase import firebase
import json

class CustomError(Exception):
    pass

lang=""
name="questions.txt"
topic=""

def set_lang(string):
    global lang
    lang=string
    return True

def set_name(string):
    global name
    name=string
    return True

def set_topic(string):
    global topic
    topic=string
    return True

switcher={
    "-lang": set_lang,
    "-name": set_name,
    "-topic": set_topic
}

db = firebase.FirebaseApplication('https://tesi-database.firebaseio.com/',None)
data=db.get("/bots/students/",'')
topic_array=[]
lang_array=[]

for topic_str in data:
    if topic_str not in topic_array:
        topic_array.append(topic_str)
    for lang_str in data[topic_str]:
        if lang_str not in lang_array:
            lang_array.append(lang_str)

def q_and_a(array):
    array1={}
    for elem in array:
        if "answer" not in array[elem]:
            array1[elem]=""
        else:
            array1[elem]=array[elem]["answer"]
    return array1

def write_doc():
    global data
    global topic
    global name
    global lang
    with open(name,"w") as jfile:
        array={}
        for topic_str in data:
            if topic=="":
                array[topic_str]={}
                for lang_str in data[topic_str]:
                    if "questions" not in data[topic_str][lang_str]:
                        continue
                    if lang =="":
                        array[topic_str][lang_str]=q_and_a(data[topic_str][lang_str]["questions"])
                    elif lang_str==lang:
                        array[topic_str]=q_and_a(data[topic_str][lang_str]["questions"])
            elif topic_str==topic:
                for lang_str in data[topic_str]:
                    if lang =="":
                        array[lang_str]=q_and_a(data[topic_str][lang_str]["questions"])
                    elif lang_str==lang:
                        array=q_and_a(data[topic_str][lang_str]["questions"])
        json.dump(array,jfile)

def Error():
    print("Questo è un programma per scaricare il database delle domande del bot del politecnico")
    print("Accetta i seguenti parametri")
    print("-lang <string>: si sceglie la lingua da scaricare, se non specificato si scaricano tutte")
    print("-topic <string>: si sceglie la materia da scaricare, se non specificato si scaricano tutti")
    print("-name <string>: si sceglie la materia il nome del file di output, se non specificato il tutto viene salvato nel file questions.txt (il nome deve finire con txt)")

try:
    i=1
    while i<len(sys.argv):
        func=switcher.get(sys.argv[i],lambda a : False)
        if func(sys.argv[i+1]):
            i+=2
        else:
            raise CustomError
    print("lang: "+lang)
    print("name: "+name)
    print("topic: "+topic)
    if (lang not in lang_array and lang!="") or (topic not in topic_array and topic!="") or not name.endswith(".txt"):
        raise CustomError
    write_doc()
except CustomError:
    Error()
except IndexError:
    Error()