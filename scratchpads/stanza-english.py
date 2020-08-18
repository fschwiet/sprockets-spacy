import stanza
import deplacy

phrase = "After the student moved the chair broke." # problematic as a garden path
# phrase = "The window slides open and -- you sitting down? -- smoke comes out of it." # problematic use of --

stanza.download('en')
nlp = stanza.Pipeline('en')
doc = nlp(phrase)

print(doc)
print(doc.entities)

deplacy.render(doc)
deplacy.serve(doc)