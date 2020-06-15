import unittest
from node_class import *

class TestLanguage(unittest.TestCase):

    def test_getArrays(self):
        array={}
        node1=Node("node1",array)
        self.assertEqual(node1.getArrays()[0],[])
        self.assertEqual(node1.getArrays()[1],[])
        node2=Node("node2",array)
        node1.addParent(node2)
        self.assertEqual(node1.getArrays()[0],[node2])
        node3=Node("node3",array)
        node1.addSon(node3)
        self.assertEqual(node1.getArrays()[1],[node3])
        node4=Node("node4",array)
        node1.addParent(node4)
        node1.addSon(node4)
        self.assertEqual(node1.getArrays()[0],sorted([node2,node4]))
        self.assertEqual(node1.getArrays()[1],sorted([node3,node4]))
        node5=Node("node5",array)
        node5.addSons([node1,node2])
        node5.addParents([node3,node4])
        self.assertEqual(node5.getArrays()[0],sorted([node3,node4]))
        self.assertEqual(node5.getArrays()[1],sorted([node1,node2]))

    def test_getJSONArray(self):
        array1={}
        array1["it"]={}
        array1["it"]["Ciao"]={}
        array1["it"]["Ciao"]["a"]="Hey"
        array1["it"]["Ciao"]["id"]=[]
        array1["en"]={}
        array1["en"]["Hello"]={}
        array1["en"]["Hello"]["a"]="Hi"
        array1["en"]["Hello"]["id"]=[]
        node1=Node("node1",array1)
        lang=Language()
        self.assertEqual(node1.getJSONArray(lang,"it"),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=True),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=False),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"en"),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=True),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=False),array1["en"])
        array2={}
        array2["it"]={}
        array2["en"]={}
        node2=Node("node2",array2)
        self.assertEqual(node2.getJSONArray(lang,"it"),array2["it"])
        self.assertEqual(node2.getJSONArray(lang,"it",recursive=True),array2["it"])
        self.assertEqual(node2.getJSONArray(lang,"it",recursive=False),array2["it"])
        self.assertEqual(node2.getJSONArray(lang,"en"),array2["en"])
        self.assertEqual(node2.getJSONArray(lang,"en",recursive=True),array2["en"])
        self.assertEqual(node2.getJSONArray(lang,"en",recursive=False),array2["en"])
        node1.addParent(node2)
        self.assertEqual(node1.getJSONArray(lang,"it"),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=True),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=False),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"en"),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=True),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=False),array1["en"])
        array3={}
        array3["it"]={}
        array3["it"]["Mi chiamo Fede"]={}
        array3["it"]["Mi chiamo Fede"]["a"]="Siiiii"
        array3["it"]["Mi chiamo Fede"]["id"]=[]
        array3["en"]={}
        array3["en"]["Hello"]={}
        array3["en"]["Hello"]["a"]="Hi"
        array3["en"]["Hello"]["id"]=[]
        node3=Node("node3",array3)
        node1.addParent(node3)
        array3["it"]["Ciao"]={}
        array3["it"]["Ciao"]["a"]="Hey"
        array3["it"]["Ciao"]["id"]=[]
        self.assertEqual(node1.getJSONArray(lang,"it"),array3["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=True),array3["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=False),array1["it"])
        self.assertEqual(node1.getJSONArray(lang,"en"),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=True),array1["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=False),array1["en"])
        array4={}
        array4["it"]={}
        array4["it"]["Bene"]={}
        array4["it"]["Bene"]["a"]="Male"
        array4["it"]["Bene"]["id"]=[]
        array4["en"]={}
        array4["en"]["Good"]={}
        array4["en"]["Good"]["a"]="Evil"
        array4["en"]["Good"]["id"]=[]
        node4=Node("node4",array4)
        node3.addParent(node4)
        array3["it"]["Bene"]={}
        array3["it"]["Bene"]["a"]="Male"
        array3["it"]["Bene"]["id"]=[]
        array3["en"]["Good"]={}
        array3["en"]["Good"]["a"]="Evil"
        array3["en"]["Good"]["id"]=[]
        self.assertEqual(node1.getJSONArray(lang,"it"),array3["it"])
        self.assertEqual(node1.getJSONArray(lang,"it",recursive=True),array3["it"])
        self.assertEqual(node1.getJSONArray(lang,"en"),array3["en"])
        self.assertEqual(node1.getJSONArray(lang,"en",recursive=True),array3["en"])
        array5={}
        node5=Node("node5",array5)
        self.assertEqual(node5.getJSONArray(lang,"it"),array5)
        self.assertEqual(node5.getJSONArray(lang,"it",recursive=True),array5)
        self.assertEqual(node5.getJSONArray(lang,"en"),array5)
        self.assertEqual(node5.getJSONArray(lang,"en",recursive=True),array5)
        node5.addParent(node1)
        self.assertEqual(node5.getJSONArray(lang,"it"),array3["it"])
        self.assertEqual(node5.getJSONArray(lang,"it",recursive=True),array3["it"])
        self.assertEqual(node5.getJSONArray(lang,"en"),array3["en"])
        self.assertEqual(node5.getJSONArray(lang,"en",recursive=True),array3["en"])
    
    def test_crossLang(self):
        array={}
        array["it"]={}
        array["it"]["Mi chiamo Fede"]={}
        array["it"]["Mi chiamo Fede"]["a"]="Siiiii"
        array["it"]["Mi chiamo Fede"]["id"]=[]
        array["en"]={}
        array["en"]["Hello"]={}
        array["en"]["Hello"]["a"]="Hi"
        array["en"]["Hello"]["id"]=[]
        array["it"]["Bene"]={}
        array["it"]["Bene"]["a"]="Male"
        array["it"]["Bene"]["id"]=[]
        array["en"]["Good"]={}
        array["en"]["Good"]["a"]="Evil"
        array["en"]["Good"]["id"]=[]
        array["it"]["Ciao"]={}
        array["it"]["Ciao"]["a"]="Hey"
        array["it"]["Ciao"]["id"]=[]
        node1=Node("node1",array)
        lang=Language()
        vett=["it","en"]
        self.assertEqual(node1.crossLang(node1,lang,vett),True)
        empty_array={}
        node2=Node("node2",empty_array)
        self.assertEqual(node2.crossLang(node2,lang,vett),True)
        self.assertEqual(node2.crossLang(node1,lang,vett),True)
        self.assertEqual(node1.crossLang(node2,lang,vett),False)
        array1={}
        array1["it"]={}
        array1["en"]={}
        array1["it"]["Bene"]={}
        array1["it"]["Bene"]["a"]="Male"
        array1["it"]["Bene"]["id"]=[]
        array1["en"]["Good"]={}
        array1["en"]["Good"]["a"]="Evil"
        array1["en"]["Good"]["id"]=[]
        node3=Node("node3",array1)
        self.assertEqual(node3.crossLang(node1,lang,vett),True)
        self.assertEqual(node1.crossLang(node3,lang,vett),False)


    def test_getLang(self):
        array1={}
        array1["it"]={}
        array1["it"]["Ciao"]={}
        array1["it"]["Ciao"]["a"]="Hey"
        array1["it"]["Ciao"]["id"]=[]
        array1["en"]={}
        array1["en"]["Hello"]={}
        array1["en"]["Hello"]["a"]="Hi"
        array1["en"]["Hello"]["id"]=[]
        node1=Node("node1",array1)
        vett=["en","it"]
        self.assertEqual(node1.getLang(),vett)
        array2={}
        array2["it"]={}
        array2["it"]["Ciao"]={}
        array2["it"]["Ciao"]["a"]="Hey"
        array2["it"]["Ciao"]["id"]=[]
        node2=Node("node2",array2)
        vett=["it"]
        self.assertEqual(node2.getLang(),vett)
        array3={}
        array3["en"]={}
        array3["en"]["Hello"]={}
        array3["en"]["Hello"]["a"]="Hi"
        array3["en"]["Hello"]["id"]=[]
        node3=Node("node3",array3)
        vett=["en"]
        self.assertEqual(node3.getLang(),vett)

    def test_equal(self):
        array={}
        node1=Node("node1",array)
        self.assertEqual(node1==node1,True)
        self.assertEqual(node1!=node1,False)
        node2=Node("node2",array)
        self.assertEqual(node1==node2,True)
        self.assertEqual(node1!=node2,False)
        self.assertEqual(node2==node1,True)
        self.assertEqual(node2!=node1,False)
        node2.addSon(node1)
        self.assertEqual(node1==node2,False)
        self.assertEqual(node1!=node2,True)
        self.assertEqual(node2==node1,False)
        self.assertEqual(node2!=node1,True)
        node3=Node("node3",array)
        node3.addParent(node1)
        self.assertEqual(node1==node3,False)
        self.assertEqual(node1!=node3,True)
        self.assertEqual(node3==node1,False)
        self.assertEqual(node3!=node1,True)
        self.assertEqual(node3==node2,False)
        self.assertEqual(node3!=node2,True)
        self.assertEqual(node2==node3,False)
        self.assertEqual(node2!=node3,True)
        node4=Node("node4",array)
        node4.addParent(node2)
        self.assertEqual(node4==node3,False)
        self.assertEqual(node4!=node3,True)
        self.assertEqual(node3==node4,False)
        self.assertEqual(node3!=node4,True)
        node5=Node("node5",array)
        node5.addSon(node3)
        self.assertEqual(node5==node2,False)
        self.assertEqual(node5!=node2,True)
        self.assertEqual(node2==node5,False)
        self.assertEqual(node2!=node5,True)
        node4.addSon(node1)
        node5.addParent(node1)
        self.assertEqual(node5==node4,False)
        self.assertEqual(node5!=node4,True)
        self.assertEqual(node4==node5,False)
        self.assertEqual(node4!=node5,True)


    def test_getName(self):
        array={}
        node1=Node("node1",array)
        self.assertEqual(node1.getName(),"node1")

    def test_Relation(self):
        array={}
        node1=Node("node1",array)
        node2=Node("node2",array)
        self.assertEqual(node1.isSon(node2),False)
        self.assertEqual(node1.isParent(node2),False)
        node1.addSon(node2)
        self.assertEqual(node1.isSon(node2),True)
        node1.addParent(node2)
        self.assertEqual(node1.isParent(node2),True)