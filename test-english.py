import spacy
from spacy import displacy

phrase = "After the student moved the chair broke."

nlp = spacy.load("en_core_web_lg", style="ent")

doc = nlp(phrase)

for w in doc:
    print([(w.text, w.pos_, w.tag_)])

# options={ "fine_grained":"True", "add_lemma": "True", "compact" : "True"}
options={ "compact":"True"}

displacy.serve(doc, style="dep", options=options)
