import deplacy
import stanza
import unittest

from tests.context import *


stanza.download('es')
nlp = stanza.Pipeline('es')


hacerTimeExpressions = [
    "Estuve en Londres hace dos años.",
    "Hace dos años que soy socio.",
    "Hace diez años que murió.",
    ]


class TestHacerTimeDetection(unittest.TestCase):

    def test_mixed_perfsubj_infinite(self):
        sprocket = self.run_stanza("Estuve en Londres hace dos años.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Estuve", "hace"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_mixed_perfimp_infinite(self):
        sprocket = self.run_stanza("Hace dos años que soy socio.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Hace", "soy"])
        self.assertEqual(sprocket.summarize_interconnections(), ["Hace -que- soy"])

    def test_mixed_perfimp_subj(self):
        sprocket = self.run_stanza("Hace diez años que murió.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Hace", "murió"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_mixed_perfimp_subj(self):
        sprocket = self.run_stanza("Trabajo aquí desde hace mucho.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Trabajo", "hace"])
        self.assertEqual(sprocket.summarize_interconnections(), ['Trabajo -desde- hace'])

    @staticmethod
    def run_stanza(text):
        stanza_result = nlp(text)
        [sentence] = stanza_result.sentences
        tabulate_sentence(sentence)
        sprocket = SprocketSentence(sentence)
        print(sprocket.summarize_interconnections())
        deplacy.render(stanza_result)
        return sprocket


if __name__ == '__main__':
    unittest.main()

