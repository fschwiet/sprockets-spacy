from stanza.models.common.doc import Word

_verb_phrase = "_verb_phrase"


def get_verb_phrase(self):
    return getattr(self, "_verb_phrase", None)


def set_verb_phrase(self, value):
    self._verb_phrase = value


setattr(Word, 'verb_phrase', property(get_verb_phrase, set_verb_phrase))