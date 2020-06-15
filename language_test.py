import unittest
from language_class import *

class TestLanguage(unittest.TestCase):

    def test_check_lang(self):
        lang=Language()
        val={}
        val["Come si chiama Ginevra?"]="it"
        self.assertEqual(lang.check_lang("Come si chiama Ginevra?"),val)
        val["Where is the book?"]="en"
        self.assertEqual(lang.check_lang("Come si chiama Ginevra? Where is the book?"),val)

    def test_calculate_similarity(self):
        lang=Language()
        self.assertEqual(lang.calculate_similarity("Come si crea una classe?","Come viene creata una classe?","it")>0.8,True)
        self.assertEqual(lang.calculate_similarity("Where is the book?","Who is Lincoln?","en")>0.8,False)

    def test_translate(self):
        lang=Language()
        self.assertEqual(lang.translate("Ciao, come va?","it","de"),"Hallo, wie geht es dir?")
        