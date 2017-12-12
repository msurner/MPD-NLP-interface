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
doc = nlp(sys.argv[1])#u'This is a sentence.')
displacy.serve(doc, style='dep')
