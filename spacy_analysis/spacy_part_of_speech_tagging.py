import sys
import spacy

if(len(sys.argv) == 1):
    print("Sentence missing.")
    exit()
elif(len(sys.argv) > 2):
    print("Make sure you use \"\" to delimit your sentence.")
    exit()

nlp = spacy.load('en_core_web_lg')

doc = nlp(sys.argv[1])#u'Apple is looking at buying U.K. startup for $1 billion')

for token in doc:
    print(token.text, token.lemma_, token.pos_, token.tag_, token.dep_,
          token.shape_, token.is_alpha, token.is_stop)

