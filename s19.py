import sys, re
from functools import reduce
from collections import namedtuple
from operator import add, sub, mul

inp = open(sys.argv[1]).readlines()

bps = [{x: int(y) for x, y in m.groupdict().items()}
       for line in inp
       if (m := re.search(r"""(?x)
          print\s(?P<id>\d+).*?
                 (?P<ore>\d+).*?
                 (?P<orecly>\d+).*?
                 (?P<obsore>\d+).*?
                 (?P<obscly>\d+).*?
                 (?P<geoore>\d+).*?
                 (?P<geoobs>\d+).*?""", line))]

def va(a, b, op=add):
    return tuple(map(op, a, b))
def inc(a, i):
    return (x+(c==i) for c, x in enumerate(a))

def sim(bp, N):
    cst = {'ore': (bp['ore'], 0, 0, 0),
           'cly': (bp['orecly'], 0, 0, 0),
           'obs': (bp['obsore'], bp['obscly'], 0, 0),
           'geo': (bp['geoore'], 0, bp['geoobs'], 0)}
    S = namedtuple('S', 'ore,cly,obs,geo,rore,rcly,robs,rgeo')
    maxs = tuple(max(c[i] for c in cst.values()) for i in range(4))
    q = [(0, S(0, 0, 0, 0, 1, 0, 0, 0))]

    best = 0
    while q:
        q = sorted(q, key=lambda x: (x[1][7:2:-1]))
        t, s = q.pop()
        tremain = N-t
        if t == N:
            best = max(best, s[3])
            continue
        max_potential = s.geo + sum(s.rgeo+i for i in range(tremain+1))
        if max_potential < best:
            continue  # prune infeasible branch

        choices = {}
        outp, rbts = s[:4], s[4:]
        for prd, need in enumerate(cst.values()):
            #if all(a for a, b in zip(rbts, need) if b):
                # I have all robot types to create inputs to this new robot.
                # how long will it take to get the product I need if I wait?
            #    nt = max(max(0, (nd-op)//rb) for nd, op, rb in zip(need, outp, rbts) if nd)
            #    nrinv = inc(rbts, prd)
            #    noinv = va(va(outp, need, sub), (x*(nt+1) for x in rbts))
            #    choices[prd] = (t+nt+1, S(*noinv, *nrinv))
            if all(a>=b for a, b in zip(s[:4], need)):
                nrinv = inc(rbts, prd)
                noinv = va(va(outp, need, sub), rbts)
                choices[prd] = (t+1, S(*noinv, *nrinv))
        if 3 in choices:
            q.append(choices[3])
        else:
            for prd, st in choices.items():
                if 0 < prd < 3 and rbts[prd] >= maxs[prd]:
                    continue  # we produce enough output to create a robot each minute, no more needed
                if maxs[prd] and outp[prd] > maxs[prd] + 1:
                    continue  # don't make a robot if we have a glut of the product
                q.append(st)
            q.append((t+1, S(*va(outp, rbts), *s[4:])))  # collect resources only

    return best


scores = {}
if len(sys.argv) < 2 or int(sys.argv[2]) == 1:
    for i, bp in enumerate(bps):
        scores[i] = sim(bp, 24)
        print(i, scores[i])
    print(scores, sum((i+1)*s for i, s in scores.items()))

if len(sys.argv) < 2 or int(sys.argv[2]) == 2:
    scores = {}
    for i, bp in enumerate(bps[:3]):
        scores[i] = sim(bp, 32)
        print(i, scores[i])
    print(scores, reduce(mul, scores.values()))
