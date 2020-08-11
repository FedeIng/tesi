import json
import spacy
import telepot
from gensim.models import Word2Vec
from spacy_langdetect import LanguageDetector
from googletrans import Translator
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply

class Language:

    def __init__(self,database):
        print("Lang")
        self.database=database
        print(1)
        self.admins={}
        print(2)
        self.setted_lang=None
        print(3)
        self.nlp=None
        print(4)
        #with open (fileName,"r") as jfile:
            #self.user_lang=json.load(jfile)
        self.lang_strings=database.get_trans()
        print(5)
        self.switcher={
            "it":"\U0001F1EE\U0001F1F9 IT \U0001F1EE\U0001F1F9",
            "de":"\U0001F1E9\U0001F1EA DE \U0001F1E9\U0001F1EA",
            "fr":"\U0001F1EB\U0001F1F7 FR \U0001F1EB\U0001F1F7",
            "en":"\U0001F1EC\U0001F1E7 EN \U0001F1EC\U0001F1E7",
            "es":"\U0001F1EA\U0001F1F8 ES \U0001F1EA\U0001F1F8"
        }
        self.switch_coll={
            "it":"collaboratore",
            "de":"mitarbeiter",
            "fr":"collaborateur",
            "en":"collaborator",
            "es":"colaborador"
        }
        self.switch_teach={
            "it":"professore",
            "de":"lehrer",
            "fr":"prof",
            "en":"teacher",
            "es":"profesor"
        }
        self.switch_nlp={
            "it":self.it_fun,
            "de":self.de_fun,
            "fr":self.fr_fun,
            "en":self.en_fun,
            "es":self.es_fun
        }
        print("lang setted")

    def it_fun(self):
        self.nlp = spacy.load('it_core_news_sm')
        model = Word2Vec.load('wiki_iter=5_algorithm=skipgram_window=10_size=300_neg-samples=10.m')
        keys = []
        for idx in range(733392):
            keys.append(model.wv.index2word[idx])
        self.nlp.vocab.vectors = spacy.vocab.Vectors(data=model.wv.vectors, keys=keys)

    def de_fun(self):
        self.nlp = spacy.load('de_core_news_md')

    def fr_fun(self):
        self.nlp = spacy.load('fr_core_news_md')

    def en_fun(self):
        self.nlp = spacy.load('en_core_web_lg')

    def es_fun(self):
        self.nlp = spacy.load('es_core_news_md')

    def get_lang_by_flag(self,flag):
        for elem in self.switcher:
            if flag == self.switcher.get(elem,""):
                return elem
        return None

    def get_flag_list(self):
        return ["\U0001F1EE\U0001F1F9 IT \U0001F1EE\U0001F1F9",
            "\U0001F1E9\U0001F1EA DE \U0001F1E9\U0001F1EA",
            "\U0001F1EB\U0001F1F7 FR \U0001F1EB\U0001F1F7",
            "\U0001F1EC\U0001F1E7 EN \U0001F1EC\U0001F1E7",
            "\U0001F1EA\U0001F1F8 ES \U0001F1EA\U0001F1F8"]

    def match_array(self,txt,lang,vett):
        print(vett)
        e=''
        val=0
        for elem in vett:
            num=self.calculate_similarity(txt,elem,lang)
            if num > val:
                val=num
                e=elem
                print(elem)
        if val>0.8:
            return vett[e]
        else:
            return None

    def set_nlp(self,lang):
        if self.setted_lang != lang:
            self.switch_nlp.get(lang,None)()
            self.setted_lang=lang

    def checkLangStr(self,txt,string):
        for lang in self.lang_strings:
            if self.lang_strings[lang][string] == txt:
                return True
        return False

    def question_sent(self,lang,text):
        data=[]
        print(lang)
        print("2")
        trans=Translator()
        for elem in self.nlp(text).sents:
            string=elem.text
            print("3 : "+string)
            if string.endswith("?") and lang==trans.translate(string).src:
                data.append(string)
        return data
        
    def checkTeach(self,lang,text):
        return text==self.switch_teach.get(lang)
    
    def checkColl(self,lang,text):
        return text==self.switch_coll.get(lang)

    def printx(self, string, xxx=None, yyy=None):
        array=[]
        array1=[]
        if xxx!=None:
            array=string.split("XXX")
            print(array)
        else:
            return string
        if yyy!=None:
            array1=array[1].split("YYY")
        else:
            return array[0]+xxx+array[1]
        return array[0]+xxx+array1[0]+yyy+array1[1]

    def addAdmins(self, lang, vett):
        self.admins[lang]=vett

    def getAdmins(self, lang):
        return self.admins[lang]

    def getString(self, lang, string, xxx=None, yyy=None):
        if string=="start":
            xxx=self.translate(xxx,"en",lang)
        if lang in self.lang_strings:
            if string in self.lang_strings[lang]:
                return self.printx(self.lang_strings[lang][string],xxx,yyy)
        return ""

    def createButton(self,lang):
        return InlineKeyboardButton(text=self.switcher.get(lang,""),callback_data=lang)

    def setKeyboard(self,lang_array,bool_var=True):
        i=0
        data=[]
        l=0
        for elem in lang_array:
            if i == 0:
                data.append([])
                l+=1
            data[l-1].append(KeyboardButton(text=self.switcher.get(elem,"")))
            i+=1
            i%=2
        return ReplyKeyboardMarkup(keyboard=data,resize_keyboard=True,one_time_keyboard=True,selective=bool_var)

    def getLangBoard(self,lang,array,num=1):
        data=[[KeyboardButton(text=self.switch_coll.get(lang))],[KeyboardButton(text=self.switch_teach.get(lang))]]
        return ReplyKeyboardMarkup(keyboard=data,resize_keyboard=True,one_time_keyboard=True,selective=False)

    def setLangResp(self,id,lang,bot):
        if bot["topic"] not in self.user_lang:
            self.user_lang[bot["topic"]]={}
        self.user_lang[bot["topic"]][id]=lang
        with open(self.file,"w") as jfile:
            json.dump(self.user_lang,jfile)

    def calculate_similarity(self,text1,text2,lang):
        base = self.nlp(self.process_text(text1,lang))
        compare = self.nlp(self.process_text(text2,lang))
        num=base.similarity(compare)
        return num

    def process_text(self,string,lang):
        doc = self.nlp(string.lower())
        result = []
        for token in doc:
            if token.text in self.nlp.Defaults.stop_words:
                continue
            if token.is_punct:
                continue
            if token.lemma_ == '-PRON-':
                continue
            result.append(token.lemma_)
        return " ".join(result)

    def translate(self,string,src,dest):
        trans=Translator()
        t=trans.translate(string,src=src,dest=dest)
        print(t)
        return t.text