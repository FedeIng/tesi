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

def q_and_a(array):
    array1={}
    for elem in array:
        array1[elem]={"answer":array[elem]}
    return array1

def read_doc():
    global db
    global topic
    global lang
    global name
    data={}
    with open(name,"r") as json_file:
        data = json.load(json_file)
    if lang !="":
        if topic !="":
            db.put("/bots/students/"+topic+"/"+lang,name="questions",data=q_and_a(data))
        else:
            for topic_str in data:
                db.put("/bots/students/"+topic_str+"/"+lang,name="questions",data=q_and_a(data[topic_str]))
    else:
        if topic !="":
            for lang_str in data:
                db.put("/bots/students/"+topic+"/"+lang_str,name="questions",data=q_and_a(data[lang_str]))
        else:
            for topic_str in data:
                for lang_str in data[topic_str]:
                    db.put("/bots/students/"+topic_str+"/"+lang_str,name="questions",data=q_and_a(data[topic_str][lang_str]))

def error():
    print("Questo è un programma per caricare il database delle domande del bot del politecnico")
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
    if (lang not in ["it","fr","de","en","es",""]) or not name.endswith(".txt"):
        raise CustomError
    read_doc()
except CustomError:
    error()
except IndexError:
    error()