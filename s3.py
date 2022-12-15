import sys, operator, functools;(

(sacks := [x.strip() for x in sys.stdin.readlines()]),

prio := lambda it: 
    ord(it) - (ord('A')-27 if it.isupper() else ord('a')-1),

print(sum(prio(next(iter(set(s[:len(s)//2])&set(s[len(s)//2:]))))
    for s in sacks)),

print(sum(prio(next(iter(
    functools.reduce(operator.and_,map(set,grp)))))
    for grp in (sacks[i:i+3] for i in range(0,len(sacks),3))))
)
