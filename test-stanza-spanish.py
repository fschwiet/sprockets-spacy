import stanza
import deplacy

phrase = "Y para colmo ese proceso comienza en el 94, el año en que estalló el escándalo por Europa del AMI, que fue lo mismo a escala universal."


stanza.download('es')
nlp = stanza.Pipeline('es')
doc = nlp(phrase)

print(doc)
print(doc.entities)

deplacy.serve(doc)