#%%
import spacy

nlp = spacy.load("en_core_web_sm")

#%%
doc = nlp("I prefer cats over dogs")
for token in doc.noun_chunks:
    print(token.text, token.lemma_, token.root.text, spacy.explain(token.root.dep_),
            token.root.head.text)