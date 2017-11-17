import sys
import spacy
from spacy import displacy

if(len(sys.argv) == 1):
    print("Sentence missing.")
    exit()
elif(len(sys.argv) > 2):
    print("Make sure you use \"\" to delimit your sentence.")
    exit()

nlp = spacy.load('en_core_web_lg')

doc = nlp(sys.argv[1])#u'Apple is looking at buying U.K. startup for $1 billion')

for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
