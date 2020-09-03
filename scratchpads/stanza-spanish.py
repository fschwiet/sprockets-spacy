import stanza
import deplacy
from sprocketry import tabulate_sentence

phrase = "Y para colmo ese proceso comienza en el 94, el año en que estalló el escándalo por Europa del AMI, que fue lo mismo a escala universal."
phrase = "¿Qué pasaría si se me cayera?"
phrase = "Ese es el caballo por el cual hubiera vendido mi casa de tener yo una."
phrase = "Anuncio de inicio de un procedimiento antidumping relativo a las importaciones de carburo de silicio originario de Rumanía"

phrases = [
    "Los resultados escolares también están influidos por el hecho de que la mayoría de los alumnos no pueden pedir a sus padres.",
]

stanza.download('es')
nlp = stanza.Pipeline('es')

for doc in (nlp(phrase) for phrase in phrases):
    for sentence in doc.sentences:
        tabulate_sentence(sentence)
    deplacy.render(doc)

#deplacy.serve(doc)