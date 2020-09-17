I am just playing with spaCy and Stanza a bit in this repo.  Observations:

- lots of incorrect dependency relationships for subclauses (distinguishing adjectival vs adverbial clauses, for example)
- despacy draws better graphs than displacy
- Stanza handles english garden path sentence "After the student moved the chair broke." better than SpaCy

Stanza: https://stanfordnlp.github.io/stanza/
- required pytorch, installed with: pip install torch===1.6.0 torchvision===0.7.0 -f https://download.pytorch.org/whl/torch_stable.html
- model interpretation:
  - https://universaldependencies.org/u/pos/all.html
  - https://universaldependencies.org/u/feat/all.html
  - https://universaldependencies.org/u/dep/all.html
  
spaCy: https://spacy.io/
- downloaded modules: es_core_news_lg, en_core_web_lg

To switch to the python virtual envrionment, run:
- ./env/Scripts/activate
- documentation on python virtual environments:  https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/#creating-a-virtual-environment
