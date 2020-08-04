import spacy
import deplacy

phrase = "After the student moved the chair broke." # problematic as a garden path
# phrase = "The window slides open and -- you sitting down? -- smoke comes out of it." # problematic use of --

nlp = spacy.load("en_core_web_lg", style="ent")

doc = nlp(phrase)

for w in doc:
    print([(w.text, w.pos_, w.tag_)])

deplacy.serve(doc)
