import sys, re
from functools import reduce as rd
from operator import mul
from itertools import product as cp 
from types import SimpleNamespace as sn
from collections import defaultdict, deque as dq

inp = sys.stdin.read()

def monkeys():
    mk = [sn(**m.groupdict())
          for m in
          re.finditer(r"""(?ixs)
             Monkey.(?P<monkey>\d+):
             .*?items:.(?P<items>.*?)\n
             .*?Operation:.*?=\s*(?P<op>.*?)\n
             .*?Test:.*?(?P<tst>\d+)\s*\n
             .*?If.true:.throw.to.monkey.(?P<tn>\d+)
             .*?If.false:.throw.to.monkey.(?P<fn>\d+)
             """, inp)]

    itms = {}
    for m in mk:
        # give each item a unique item index and track worry by that index
        w = dict(enumerate(map(int,m.items.split(',')),len(itms)))
        itms.update(w)
        m.monkey = int(m.monkey)
        m.items = list(w)
        m.tst, m.fn, m.tn = map(int, (m.tst, m.fn, m.tn))
        m.lop = lambda old, m=m: eval(m.op.replace('old', str(old)))
    # each item's current worry
    itms = [[v]*len(mk) for i,v in itms.items()]
    return mk, itms

def turn(mk, itms, m, wlm, inspect):
    for i in mk[m].items:
        itms[i] = [wlm(mk[m].lop(wv),mo.tst) for mo,wv in zip(mk,itms[i])]
        mk[[mk[m].fn, mk[m].tn][itms[i][m]%mk[m].tst==0]].items.append(i)
    inspect[m] += len(mk[m].items)
    mk[m].items.clear()

def game(wlm, rnds, topn=2):
    mk, itms = monkeys()
    inspect = [0]*len(mk) # inspections per monkey
    dq((turn(mk, itms, m.monkey, wlm, inspect) for i,m in cp(range(rnds),mk)),1)

    return rd(mul,sorted(inspect)[-topn:])

print(game(lambda x,_: x//3, 20))
print(game(lambda x,d: x%d, 10_000))

