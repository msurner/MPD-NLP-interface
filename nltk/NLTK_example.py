from nltk import CFG
from nltk.parse import RecursiveDescentParser

# Define grammar
grammar = CFG.fromstring("""
S -> Instruction Argument
S -> Instruction
Instruction -> 'play'
Instruction -> 'pause'
Instruction -> 'resume'
Argument -> Song | Artist | Gerne
Gerne -> 'rock'
Gerne -> 'jazz'
Gerne -> 'classic'
""")

rd = RecursiveDescentParser(grammar)

sentence1 = "Play song".lower().split()

for t in rd.parse(sentence1):
    print(t)
