from nltk import Nonterminal, nonterminals, Production, CFG

nt1 = Nonterminal('NP')
nt2 = Nonterminal('VP')

print(str(nt1.symbol()))
# 'NP'

print(str(nt1 == Nonterminal('NP')))
# True

print(str(nt1 == nt2))
# False

S, NP, VP, PP = nonterminals('S, NP, VP, PP')
N, V, P, DT = nonterminals('N, V, P, DT')

prod1 = Production(S, [NP, VP])
prod2 = Production(NP, [DT, NP])

print(str(prod1.lhs()))
# S

print(str(prod1.rhs()))
# (NP, VP)

print(str(prod1 == Production(S, [NP, VP])))
# True

print(str(prod1 == prod2))
# False

grammar = CFG.fromstring("""
 S -> NP VP
 PP -> P NP
 NP -> 'the' N | N PP | 'the' N PP
 VP -> V NP | V PP | V NP PP
 N -> 'cat'
 N -> 'dog'
 N -> 'rug'
 V -> 'chased'
 V -> 'sat'
 P -> 'in'
 P -> 'on'
 """)


