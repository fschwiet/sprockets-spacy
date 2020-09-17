import unittest
import stanza

from tests.context import *

stanza.download('es')
nlp = stanza.Pipeline('es')

subclauseSpecs = [

    ## verbs of influence take a complement in the subjunctive voice / nominalización.

    ("Te prohíbo que vayas a esa fiesta",
     ["prohíbo", "vayas"],
     [("complement","prohíbo(indicative/present)", "vayas(subjunctive/present)")]),
    # more verbs of influence taking a clause as direct object “aceptar”, “permitir”, “admitir”, “sugerir”, “pedir”, “ordenar”, “proponer”, “convenir”, “preferir”, “exigir”, “querer”, “pretender”, “ordenar”, “mandar”, “acceder a”, “someterse a”, “instigar a”, “incitar a”, “estimular a”, “influir en”, “complacerse”, “satisfacer”, “molestar/se”,
    # verbs of influence taking a subjunctive clause as object: “provocar aversión”, “causar incomodidad”, “inducir simpatía”, “despertar interés”, “concertar oposición”, “promover aceptación”, “suscitar curiosidad”, “engendrar sospecha”
    # verbs of influecne taking a subjunctive clause as indirect object: “juzgar inconveniente”, “decidir por unanimidad”, “decretar por mera voluntad dictatorial”, “establecer por disposición arbitraria”, “presentar a consideración”
    #

    ("Aceptamos que nuestros representantes vengan de otra provincia, pero que estén en contra de los intereses de esta provincia, eso no lo aceptamos.",
     ["Aceptamos", "vengan", "estén", "aceptamos"],
     [("complement", "Aceptamos(indicative/present|preterite)", "vengan(subjunctive/present)"), ("complement", "vengan(subjunctive/present)", "estén(subjunctive/present)")]),

    ("Propongo que sea la propia presidenta que nos proponga tres candidatos.",
     ["Propongo", "sea", "proponga"],
     [("complement", "Propongo(indicative/present)", "sea(subjunctive/present)")]),

    ## Stanza gives incorrect POS tagging for Causa in this case.  Changing it to "Me causa" fixed
    ## the POS tagging, but "que se corte" is still marked as relative to noun "incomodidad" and not
    ## the verb phrase.
    #("Causa gran incomodidad que se corte el agua todos los días.",
    # ["Causa", "corte"],
    # [("complement", "Causa(indicative)", "corte(subjunctive)")]),

    #("Me causa gran incomodidad que se corte el agua todos los días.",
    # ["causa", "corte"],
    # [("complement", "causa(indicative)", "corte(subjunctive)")]),

    ## Stanza again misclassifies the relative clause "que ocultes..." as applying to the preceding noun,
    ## not noun phrase.
    #("Engendra sospechas que ocultes cómo te sustentas.",
    # ["Engendra", "ocultes"],
    # [('complement', 'Engendra(indicative)', 'ocultes(subjunctive)')]),

    ("Induce simpatía que el ladrón haya repartido el botín entre los pobres.",
     ["Induce", "haya repartido"],
     [("complement", "Induce(indicative/present)", "haya repartido(subjunctive/present)")]),

    # que isn't necessary in some cases, in particular verbs of petition
    ("Ruego se excluya mi nombre de dicha demanda.",
     ["Ruego", "excluya"],
     [("complement", "Ruego(indicative)", "excluya(subjunctive)")]),
    # other verbs of petition: solicitar, pedir

    # recursitivity
    ("Critico que soliciten que les suministremos más agua, si la derrochan.",
     ["Critico", "soliciten", "suministremos", "derrochan"],
     [("complement", "Critico(indicative)", "soliciten(subjunctive)"), ("complement", "soliciten(subjunctive)", "suministremos(subjunctive)")]),

    ("Les incomoda que sepa que les incomoda tu presencia.",
     ["incomoda", "sepa", "incomoda"],
     [("complement", "incomoda(indicative)", "sepa(subjunctive)"), ("complement", "sepa(subjunctive)", "incomoda(indicative)")]),

    # examples of verbs that take an indicative subclause, like verbs of thought and perception: saber, reconocer, averiguar

    # 1.4. Concordancias temporales describes how the aspect of time is coordinated across the primary and sub clause.
    ("Quiero que hayas estudiado.", ["Quiero", "hayas estudiado"], [("complement", "Quiero(indicative)", "hayas estudiado(subjunctive)")]),
    ("Querré que estudies.", ["Querré", "estudies"], [("complement", "Querré(future)", "estudies(subjunctive)")]),
    ("Querré que comiences a estudiar.", ["Querré", "comiences-a estudiar"], [("complement", "Querré(future)", "comiences estudiar(subjunctive)")]),
    ("Quería que entraras a estudiar.", ["Quería", "entraras-a estudiar"], [("complement", "Quería(imperfect)", "entraras estudiar(subjunctive imp)")]),
    ("Quise que entraras a estudiar.", ["Quise", "entraras-a estudiar"], [("complement", "Quise(preterite)", "entraras estudiar(subjunctive imp)")]),

    # continue at 2.  Verbs of emocion
]


class TestSubclauseDetection(unittest.TestCase):
    def pretest_spec_format(self):
        for (testInput, phrases, relationships) in subclauseSpecs:
            try:
                self.assertIsInstance(testInput, str)
                for phrase in phrases:
                    self.assertIsInstance(phrase, str)
                for relationship in relationships:
                    self.assertIsInstance(relationship, tuple)
                    (a, b, c) = relationship
                    self.assertIsInstance(a, str)
                    self.assertIsInstance(b, str)
                    self.assertIsInstance(c, str)
            except Exception as ex:
                raise Exception('Error checking \"{0}\".'.format(testInput))

    def pretest_verbphrase_partitioning(self):
        for (testInput, phrases, _) in subclauseSpecs:
            stanza_result = nlp(testInput)
            [sentence] = stanza_result.sentences
            try:
                sprocket = SprocketSentence(sentence)
                self.assertEqual(sprocket.summarize_verb_phrases(), phrases)
            except Exception as ex:
                tabulate_sentence(sentence)
                raise Exception('Error checking \"{0}\".'.format(testInput))

    def test_complement_detection(self):
        for (testInput, _, relationships) in subclauseSpecs:
            stanza_result = nlp(testInput)
            [sentence] = stanza_result.sentences
            try:
                sprocket = SprocketSentence(sentence)
                self.assertEqual(sprocket.summarize_complements(), relationships)
            except Exception as ex:
                tabulate_sentence(sentence)
                raise Exception('Error checking \"{0}\".'.format(testInput))


if __name__ == '__main__':
    unittest.main()