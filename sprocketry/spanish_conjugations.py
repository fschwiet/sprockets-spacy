import os
import csv
from enum import Enum

#
# expected CSV file layout for conjugations data:
# infinitive,gerund,participle,indicative/present,indicative/preterite,indicative/imperfect,indicative/conditional,indicative/future,subjunctive/present,subjunctive/imperfect_ra,subjunctive/imperfect_se,subjunctive/future
# ir,yendo,ido,voy;vas;va;vamos;vais;van,fui;fuiste;fue;fuimos;fuisteis;fueron,iba;ibas;iba;íbamos;ibais;iban,iría;irías;iría;iríamos;iríais;irían,iré;irás;irá;iremos;iréis;irán,vaya;vayas;vaya;vayamos;vayáis;vayan,fuera;fueras;fuera;fuéramos;fuerais;fueran,fuese;fueses;fuese;fuésemos;fueseis;fuesen,fuere;fueres;fuere;fuéremos;fuereis;fueren
# dar,dando,dado,doy;das;da;damos;dais;dan,di;diste;dio;dimos;disteis;dieron,daba;dabas;daba;dábamos;dabais;daban,daría;darías;daría;daríamos;daríais;darían,daré;darás;dará;daremos;daréis;darán,dé;des;dé;demos;deis;den,diera;dieras;diera;diéramos;dierais;dieran,diese;dieses;diese;diésemos;dieseis;diesen,diere;dieres;diere;diéremos;diereis;dieren
#


class ConjugationKeys(Enum):
    infinitive = "infinitive"
    gerund = "gerund"
    participle = "participle"
    present: "indicative/present"
    preterite: "indicative/preterite"
    imperfect: "indicative/imperfect"
    conditional: "indicative/conditional"
    future: "indicative/future"
    subjunctive = "subjunctive/present"
    subjunctive_ra = "subjunctive/imperfect_ra"
    subjunctive_se = "subjunctive/imperfect_se"
    subjunctive_future = "subjunctive/future"

    @staticmethod
    def all():
        yield ConjugationKeys.infinitive
        yield ConjugationKeys.gerund
        yield ConjugationKeys.participle
        yield ConjugationKeys.present
        yield ConjugationKeys.preterite
        yield ConjugationKeys.imperfect
        yield ConjugationKeys.conditional
        yield ConjugationKeys.future
        yield ConjugationKeys.subjunctive
        yield ConjugationKeys.subjunctive_ra
        yield ConjugationKeys.subjunctive_se
        yield ConjugationKeys.subjunctive_future

    @staticmethod
    def all_subjunctive_keys():
        yield ConjugationKeys.subjunctive.value
        yield ConjugationKeys.subjunctive_ra.value
        yield ConjugationKeys.subjunctive_se.value
        yield ConjugationKeys.subjunctive_future.value


def _load_conjugations(file):
    with open(file, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)

        header_row = next(reader)

        for row in reader:

            next_conjugation = {"inverted": {}}
            inverted = next_conjugation["inverted"]

            def set_inverted(verb, label):
                if verb not in inverted:
                    inverted[verb] = label
                elif inverted[verb] == "indicative/present" and label == "indicative/preterite":
                    inverted[verb] = "indicative/present|preterite"
                elif inverted[verb] is not label:
                    raise Exception("Verb {0} was labelled as {1} and {2}".format(verb, inverted[verb], label))

            for column in range(len(header_row)):
                column_label = header_row[column]
                if column < 3:
                    next_conjugation[column_label] = row[column]
                    set_inverted(row[column], column_label)
                else:
                    next_conjugation[column_label] = row[column].split(";")
                    for variation in next_conjugation[column_label]:
                        set_inverted(variation, column_label)

            yield next_conjugation


class _ConjugationData:
    conjugationsByInfinitive = {}

    def __init__(self, file):
        for conjugation in _load_conjugations(file):
            self.conjugationsByInfinitive[conjugation["infinitive"]] = conjugation

    def has_subjunctivity(self, verb, lemma):
        conjugations = self.conjugationsByInfinitive[lemma]

        for key in ConjugationKeys.all_subjunctive_keys():
            if verb in conjugations[key]:
                return True

        return False

    def get_conjugation_name(self, verb, lemma):
        conjugations = self.conjugationsByInfinitive[lemma]

        return conjugations["inverted"][verb.lower()]



_singleton = None


def get():
    global _singleton
    if _singleton is None:
        _singleton = _ConjugationData(os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/verb-forms.csv')))
    return _singleton


if __name__ == '__main__':
    file_location = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data/verb-forms.csv'))
    print(file_location)
    results = _load_conjugations(file_location)
    print(next(results))
