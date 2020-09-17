import unittest
import stanza
import deplacy

from tests.context import *


stanza.download('es')
nlp = stanza.Pipeline('es')


class TestVerbPhraseExtraction(unittest.TestCase):

    def test_mixed_perfsubj_infinite(self):
        sprocket = self.run_stanza("Ese es el caballo por el cual hubiera vendido mi casa de tener yo una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "hubiera vendido", "tener"])
        self.assertEqual(sprocket.summarize_interconnections(), ['hubiera vendido -de- tener'])

    def test_mixed_perfimp_infinite(self):
        sprocket = self.run_stanza("Ese es el caballo por el cual habría vendido mi casa, de tener yo una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "habría vendido", "tener"])
        self.assertEqual(sprocket.summarize_interconnections(), ['habría vendido -de- tener'])

    def test_mixed_perfimp_subj(self):
        sprocket = self.run_stanza("Ese es el caballo por el que habría vendido mi casa si tuviera una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "habría vendido", "tuviera"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_mixed_perfimp_perfsubj(self):
        sprocket = self.run_stanza("Este es el caballo por el que habría vendido mi casa si hubiera tenido una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "habría vendido", "hubiera tenido"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_mixed_perfimp_perfinf(self):
        sprocket = self.run_stanza("Ese es el caballo por el que habría vendido mi casa de haber tenido una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "habría vendido", "haber tenido"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_mixed_perfsubj_subj(self):
        sprocket = self.run_stanza("Ese es el caballo por el cual hubiera vendido mi casa si tuviera una.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "hubiera vendido", "tuviera"])
        self.assertEqual(sprocket.summarize_interconnections(), ['hubiera vendido -si- tuviera'])





    def test_another_weird_conditional(self):
        sprocket = self.run_stanza("Una cláusua relativa restrictiva es parte integral de la referencia del caso, de modo que si se extrae cambia el referente.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "hubiera vendido", "tuviera"])
        self.assertEqual(sprocket.summarize_interconnections(), [])


    def test_en_caso_de(self):
        sprocket = self.run_stanza(
            "En caso de que el vuelo sea cancelado, pueden tomar el siguiente.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "hubiera vendido", "tuviera"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    @staticmethod
    def run_stanza(text):
        stanza_result = nlp(text)
        [sentence] = stanza_result.sentences
        #tabulate_sentence(sentence)
        sprocket = SprocketSentence(sentence)
        print(sprocket.summarize_interconnections())
        #deplacy.render(stanza_result)
        return sprocket


if __name__ == '__main__':
    unittest.main()

