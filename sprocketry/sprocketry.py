import collections

from .helpers import *
from .verb_phrase import VerbPhrase

VerbPhraseConnection = collections.namedtuple("VerbPhraseConnection", ["mark", "head", "tail", "headPhrase", "tailPhrase"])


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
                head_verb_phrase.add_connection(mark, head, tail)
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


def _get_verb_phrases(sentence):
    accumulator = []
    for word in sentence.words:
        should_publish_existing = False
        should_accumulate_word = False

        # any finite verb indicates we're in a new verb phrase
        if word_is_finite_verb(word):
            should_publish_existing = True
            should_accumulate_word = True

        # adverbial clauses like "haciendo tanto ruido" can start with a non-finite verb
        elif word.deprel == "advcl":
            should_publish_existing = True
            should_accumulate_word = word_is_verb(word)

        # once we're in a verb phrase, keep anything verbal
        if any(accumulator) and word_is_verb(word):
            should_accumulate_word = True

        if should_publish_existing and any(accumulator):
            yield VerbPhrase(accumulator, sentence)
            accumulator = []

        if should_accumulate_word:
            accumulator.append(word)

    if any(accumulator):
        yield VerbPhrase(accumulator, sentence)