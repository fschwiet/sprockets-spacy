import unittest
import collections
import stanza
from tabulate_stanza import tabulate_sentence


stanza.download('es')
nlp = stanza.Pipeline('es')


VerbPhraseInnerConnection = collections.namedtuple("VerbPhraseInnerConnection", ["mark", "head", "tail"])
VerbPhraseConnection = collections.namedtuple("VerbPhraseConnection", ["mark", "head", "tail", "headPhrase", "tailPhrase"])


class VerbPhrase:
    # A verb and its helper verbs, object complements are not included.

    def __init__(self, verbs, sentence):
        if not any(verbs):
            raise Exception("VerbPhrase given no verbs")
        self.verbs = verbs
        self.connections = []

        self.headOfCopula = None
        [*_, lastVerb] = verbs;
        if lastVerb.head > 0 and lastVerb.deprel == "cop":
            self.headOfCopula = sentence.words[lastVerb.head - 1]

    @property
    def verb_string(self):
        def get_verb_string_parts(w):
            yield w.text
            for mark in (connection.mark for connection in self.connections if connection.head == w):
                yield "-" + mark.text
        return " ".join("".join(get_verb_string_parts(w)) for w in self.verbs)


class SprocketSentence:
    # contains additional information about a stanza sentence

    def __init__(self, sentence):
        self.sentence = sentence
        self.verbPhrases = list(_get_verb_phrases(sentence))
        self.connections = []

        for mark in (w for w in sentence.words if w.deprel == "mark"):
            if mark.head == 0:
                continue
            tail = sentence.words[mark.head - 1]

            if tail.head == 0:
                continue
            head = sentence.words[tail.head - 1]

            head_verb_phrases = list(vp for vp in self.verbPhrases if (head in vp.verbs) or head is vp.headOfCopula)
            if not any(head_verb_phrases):
                continue

            tail_verb_phrases = list(vp for vp in self.verbPhrases if (tail in vp.verbs) or tail is vp.headOfCopula)
            if not any(tail_verb_phrases):
                continue

            [head_verb_phrase] = head_verb_phrases  # can only be 1 unless VerbPhrases are erroneously overlapping
            [tail_verb_phrase] = tail_verb_phrases

            if head_verb_phrase == tail_verb_phrase:
                head_verb_phrase.connections.append(VerbPhraseInnerConnection(mark, head, tail))
            else:
                self.connections.append(VerbPhraseConnection(mark, head, tail, head_verb_phrase, tail_verb_phrase))

    def summarize_verb_phrases(self):
        return list(vp.verb_string for vp in self.verbPhrases)

    def summarize_interconnections(self):
        return list(self._summarize_interconnections())

    def _summarize_interconnections(self):
        for [mark, head, tail, head_verb_phrase, tail_verb_phrase] in self.connections:
            yield "{0} -{1}- {2}".format(head_verb_phrase.verb_string, mark.text, tail_verb_phrase.verb_string)

    def __repr__(self):
        return "<SprocketSentence({0},{1})>".format(self.summarize_verb_phrases(), self.summarize_interconnections())

def get_word_feature(w, feature):
    if not hasattr(w, "features"):
        w.features = dict(pair.split("=") for pair in w.feats.split("|")) if w.feats is not None else dict()
    return w.features[feature] if feature in w.features else None


def is_finite_verb(w):
    return get_word_feature(w, "VerbForm") == "Fin"


def is_verb(w):
    verb_form = get_word_feature(w, "VerbForm")
    return verb_form is not None


def _get_verb_phrases(sentence):
    accumulator = []
    for word in sentence.words:
        should_publish_existing = False
        should_accumulate_word = False

        # any finite verb indicates we're in a new verb phrase
        if is_finite_verb(word):
            should_publish_existing = True
            should_accumulate_word = True

        # adverbial clauses like "haciendo tanto ruido" can start with a non-finite verb
        elif word.deprel == "advcl":
            should_publish_existing = True
            should_accumulate_word = is_verb(word)

        # once we're in a verb phrase, keep anything verbal
        if any(accumulator) and is_verb(word):
            should_accumulate_word = True

        if should_publish_existing and any(accumulator):
            yield VerbPhrase(accumulator, sentence)
            accumulator = []

        if should_accumulate_word:
            accumulator.append(word)

    if any(accumulator):
        yield VerbPhrase(accumulator, sentence)


class TestVerbPhraseExtraction(unittest.TestCase):
    def test_can_find_single_clause(self):
        sprocket = self.run_stanza("Había estado corriendo durante treinta minutos.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["Había estado corriendo"])
        self.assertEqual(sprocket.summarize_interconnections(), []);

    def test_can_find_multiple_clauses(self):
        sprocket = self.run_stanza("Me es desagradable que comas haciendo tanto ruido.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["es", "comas", "haciendo"])
        self.assertEqual(sprocket.summarize_interconnections(), ["es -que- comas"]);

    def test_can_find_multiple_clauses_2(self):
        # Unsourced sentence - created from previous to have a longer copula verb phrase
        sprocket = self.run_stanza("Me ha sido desagradable que comas haciendo tanto ruido.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["ha sido", "comas", "haciendo"])
        self.assertEqual(sprocket.summarize_interconnections(), ["ha sido -que- comas"]);

    def test_can_recognize_soler_auxillary_usage(self):
        sprocket = self.run_stanza("Si éste solía funcionar, piense que es lo que ha cambiado en su sistema desde el momento que ha dejado de funcionar.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["solía funcionar", "piense", "es", "ha cambiado", "ha dejado-de funcionar"])
        self.assertEqual(sprocket.summarize_interconnections(), ["piense -Si- solía funcionar", "piense -que- es"]);

    def test_el_hecho_is_excluded(self):
        sprocket = self.run_stanza("Los resultados escolares también están influidos por el hecho de que la mayoría de los alumnos no pueden pedir a sus padres.")
        self.assertEqual(sprocket.summarize_verb_phrases(), ["están influidos", "pueden pedir"]);
        self.assertEqual(sprocket.summarize_interconnections(), []);

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

