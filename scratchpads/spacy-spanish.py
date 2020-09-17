import spacy
import deplacy

phrase = "Y para colmo ese proceso comienza en el 94, el año en que estalló el escándalo por Europa del AMI, que fue lo mismo a escala universal."
phrase = "Causa gran incomodidad que se corta el agua todos los días."
phrase = "Causa gran incomodidad que se corte el agua todos los días."
phrase = "Que se corta el agua todos los días me causa gran incomodidad."
phrase = "Me causa gran incomodidad que se corte el agua todos los días."
phrase = "Causa de gran incomodidad es que se corte el agua todos los días."

nlp = spacy.load("es_core_news_lg", style="ent")


acl_advcl_ambiguity = [
    "Provoca aversión que estés conviviendo con tu prima.",
    "Induce simpatía que el ladrón haya repartido el botín entre los pobres.",
    "Engendra sospechas que ocultes cómo te sustentas.",
    "Establecieron por disposición arbitraria que se usaran turbantes."
]

markless_subclause = "Ruego se excluya mi nombre de dicha demanda."

phrases = [markless_subclause]

for phrase in phrases:
    doc = nlp(phrase)
    deplacy.render(doc)

deplacy.serve(doc)
