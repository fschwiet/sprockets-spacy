import stanza
import deplacy
from sprocketry import tabulate_sentence

hacerTimeExpressions = [
    "Estuve en Londres hace dos años.",
    "Hace dos años que soy socio.",
    "Hace diez años que murió.",
    ]

hacerTimeExpressionsPartTwo = [
    "Hace diez años de su muerte.",
    "Ha llegado a casa hace diez minutos.",
    "Pronto hará cinco años, si no los ha hecho ya.",
    "Hace mucho que trabajo aquí.",
    "Trabajo aquí desde hace mucho.",
    "Trabajo aquí hace mucho.",
    "Trabajaba aquí hasta hace poco.",
    # "Las ciudades de hace 100 años.",  # noun clause
    "Sí hace diez años que murió.",
    "La había visto hacía un año.",
    "Abandonó la ciudad pronto hará tres meses.",
    "Se casó no hace ni un mes.",
    "Se divorciaron debe de hacer dos años o así."
]

## examples of adverbial clauses, some get marked as adjectival clauses
acl_advcl_ambiguity = [
    "Provoca aversión que estés conviviendo con tu prima.",
    "Induce simpatía que el ladrón haya repartido el botín entre los pobres.",
    "Engendra sospechas que ocultes cómo te sustentas.",
    "Establecieron por disposición arbitraria que se usaran turbantes.",
]

markless_subclause = "Ruego se excluya mi nombre de dicha demanda."

phrase = "Y para colmo ese proceso comienza en el 94, el año en que estalló el escándalo por Europa del AMI, que fue lo mismo a escala universal."
phrase = "¿Qué pasaría si se me cayera?"
phrase = "Ese es el caballo por el cual hubiera vendido mi casa de tener yo una."
phrase = "Anuncio de inicio de un procedimiento antidumping relativo a las importaciones de carburo de silicio originario de Rumanía"

phrases = [markless_subclause]

stanza.download('es')
nlp = stanza.Pipeline('es')

for doc in (nlp(phrase) for phrase in phrases):
    for sentence in doc.sentences:
        tabulate_sentence(sentence)
    deplacy.render(doc)

#deplacy.serve(doc)