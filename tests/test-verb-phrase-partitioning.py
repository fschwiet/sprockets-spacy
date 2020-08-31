import unittest
import stanza

from tests.context import *


stanza.download('es')
nlp = stanza.Pipeline('es')


class TestVerbPhraseExtraction(unittest.TestCase):
    def test_can_find_single_clause(self):
        sprocket = self.run_stanza("Había estado corriendo durante treinta minutos.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Había estado corriendo"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    def test_can_link_copula_verb_phrase(self):
        # the copula verb isn't always at the top of the clause hierarchy

        sprocket = self.run_stanza("Me es desagradable que comas haciendo tanto ruido.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "comas", "haciendo"])
        self.assertEqual(sprocket.summarize_interconnections(), ["es -que- comas"])

    def test_can_link_copula_long_verb_phrase(self):
        # Unsourced sentence - created from previous to have a longer copula verb phrase

        sprocket = self.run_stanza("Me ha sido desagradable que comas haciendo tanto ruido.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["ha sido", "comas", "haciendo"])
        self.assertEqual(sprocket.summarize_interconnections(), ["ha sido -que- comas"])

    def test_can_recognize_soler_auxillary_usage(self):
        sprocket = self.run_stanza("Si éste solía funcionar, piense que es lo que ha cambiado en su sistema desde el momento que ha dejado de funcionar.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["solía funcionar", "piense", "es", "ha cambiado", "ha dejado-de funcionar"])
        self.assertEqual(sprocket.summarize_interconnections(), ["piense -Si- solía funcionar", "piense -que- es"])

    def test_el_hecho_is_excluded(self):
        sprocket = self.run_stanza("Los resultados escolares también están influidos por el hecho de que la mayoría de los alumnos no pueden pedir a sus padres.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["están influidos", "pueden pedir"])
        self.assertEqual(sprocket.summarize_interconnections(), [])

    @staticmethod
    def run_stanza(text):
        stanza_result = nlp(text)
        [sentence] = stanza_result.sentences
        tabulate_sentence(sentence)
        sprocket = SprocketSentence(sentence)
        print(sprocket.summarize_interconnections())
        return sprocket


if __name__ == '__main__':
    unittest.main()

