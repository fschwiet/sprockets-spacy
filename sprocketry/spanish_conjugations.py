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
    def all_subjunctive_keys():
        yield ConjugationKeys.subjunctive.value
        yield ConjugationKeys.subjunctive_ra.value
        yield ConjugationKeys.subjunctive_se.value
        yield ConjugationKeys.subjunctive_future.value


def _load_conjugations(file):
    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)

        header_row = next(reader)

        for row in reader:

            next_conjugation = {}

            for column in range(len(header_row)):
                if column < 3:
                    next_conjugation[header_row[column]] = row[column]
                else:
                    next_conjugation[header_row[column]] = row[column].split(";")

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
