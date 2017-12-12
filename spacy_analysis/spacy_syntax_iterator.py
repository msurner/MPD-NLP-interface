import sys
import spacy
from spacy import displacy

if(len(sys.argv) == 1):
    print("Sentence missing.")
    exit()
elif(len(sys.argv) > 2):
    print("Make sure you use \"\" to delimit your sentence.")
    exit()

nlp = spacy.load("en_core_web_lg")

doc = nlp(sys.argv[1])#u'A phrase with another phrase occurs.')
chunks = list(doc.noun_chunks)

print(">> " + sys.argv[1])

for chunk in chunks:
    print(chunk)
