import spacy
import deplacy

phrase = "Y para colmo ese proceso comienza en el 94, el año en que estalló el escándalo por Europa del AMI, que fue lo mismo a escala universal."

nlp = spacy.load("es_core_news_lg", style="ent")

doc = nlp(phrase)

for w in doc:
    print([(w.text, w.pos_, w.tag_)])

deplacy.serve(doc)