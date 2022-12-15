import sys
from ast import literal_eval as li
from functools import reduce as rd
from operator import sub, mul

pp = [[li(y) for y in x.strip().split('\n')] for x in sys.stdin.read().split('\n\n')]
tl = lambda x, xi: [x] if xi else x

def cmp(*ab):
    if all(ab):
        f = next(zip(*ab))
        i = tuple(isinstance(x, int) for x in f)
        return (rd(sub,f) if all(i) else cmp(*map(tl,f,i))) or cmp(*(x[1:] for x in ab))
    return (0, len(ab[0]) or -1)[any(ab)]

print(sum(i for i, c in enumerate((cmp(a,b) for a,b in pp),1) if c<0)) 

divs, pkts = [[[2]], [[6]]], [p for x in pp for p in x]

# find the position of the dividers by counting how many
# packets and dividers precede each divider.  This way we don't have
# sort the whole list.
poss = [sum(cmp(x,y)>0 for y in pkts)+i for i,x in enumerate(divs,1)]
print(rd(mul, poss))

