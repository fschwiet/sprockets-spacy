from tabulate import tabulate

def tabulate_sentence(sentence):
    # Summarizes the contents of a Stanza run in a dense way.

    print(sentence.text)
    print(tabulate(([w.id, w.head, w.deprel, w.upos, w.xpos, w.text, w.lemma if w.lemma != w.text else "", w.feats] for w in sentence.words),
          headers=["id", "", "deprel", "upos", "vpos", "text", "lemma", "feats"]))
    print("")

