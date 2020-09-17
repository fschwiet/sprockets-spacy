import unittest
import stanza

from tests.context import *


stanza.download('es')
nlp = stanza.Pipeline('es')

specs = [
    ("Había estado corriendo durante treinta minutos.", ["Había estado corriendo"], []),
    # verbs marked as a copula aren't always at the top of the clause hierarchy
    ("Me es desagradable que comas haciendo tanto ruido.", ["es", "comas", "haciendo"], ["es -que- comas"]),
    # created from previous to have a longer copula verb phrase
    ("Me ha sido desagradable que comas haciendo tanto ruido.", ["ha sido", "comas", "haciendo"], ["ha sido -que- comas"]),
    ("Si éste solía funcionar, piense que es lo que ha cambiado en su sistema desde el momento que ha dejado de funcionar.",
     ["solía funcionar", "piense", "es", "ha cambiado", "ha dejado-de funcionar"],
     ["piense -Si- solía funcionar", "piense -que- es"]),
    ("Los resultados escolares también están influidos por el hecho de que la mayoría de los alumnos no pueden pedir a sus padres.",
     ["están", "pueden pedir"], []),
    ("Ese es el caballo por el cual hubiera vendido mi casa de tener yo una.", ["es", "hubiera vendido", "tener"], []),
    # Stanza misclassifies causa as a noun if the "Me" is omited.  Regardless it misclassifies the "que se corta..." clause as modifying "incomodidad" not "causa"
    ("Me causa gran incomodidad que se corte el agua todos los días.", ["causa", "corte"], []),
    ("Querré que comiences a estudiar.", ["Querré", "comiences-a estudiar"], ["Querré -que- comiences-a estudiar"]),
]

class TestVerbPhraseExtraction(unittest.TestCase):

    def test_from_specs(self):
        for (testInput, phrases, relationships) in specs:
            stanza_result = nlp(testInput)
            [sentence] = stanza_result.sentences
            try:
                sprocket = SprocketSentence(sentence)
                self.assertEqual(sprocket.summarize_verb_phrases(), phrases)
                self.assertEqual(sprocket.summarize_interconnections(), relationships)
            except Exception as ex:
                tabulate_sentence(sentence)
                raise Exception('Error checking \"{0}\".'.format(testInput))


if __name__ == '__main__':
    unittest.main()

