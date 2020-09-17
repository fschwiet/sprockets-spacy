import collections

import sprocketry.spanish_conjugations

VerbPhraseInnerConnection = collections.namedtuple("VerbPhraseInnerConnection", ["mark", "head", "tail"])


class VerbPhrase:
    # A verb and its helper verbs, object complements are not included.

    def __init__(self, verbs, sentence):
        if not any(verbs):
            raise Exception("VerbPhrase given no verbs")
        self.verbs = verbs
        self.sentence = sentence
        self.connections = []

        self.headOfCopula = None
        [*_, lastVerb] = verbs;
        if lastVerb.head > 0 and lastVerb.deprel == "cop":
            self.headOfCopula = sentence.words[lastVerb.head - 1]

    def has_finite(self):
        return None is not next((x for x in self.verbs if "VerbForm=Fin" in x.feats), None)

    def only_infinitives(self):
        return None is next((x for x in self.verbs if "VerbForm=Inf" not in x.feats), None)

    def add_connection(self, mark, head, tail):
        self.connections.append(VerbPhraseInnerConnection(mark, head, tail))

    @property
    def verb_string(self):
        def get_verb_string_parts(w):
            yield w.text
            for mark in (connection.mark for connection in self.connections if connection.head == w):
                yield "-" + mark.text
        return " ".join("".join(get_verb_string_parts(w)) for w in self.verbs)

    @property
    def verb_string_plus(self):
        first_verb = self.verbs[0]
        return self.verb_string + "(" + sprocketry.spanish_conjugations.get().get_conjugation_name(first_verb.text, first_verb.lemma) + ")"
