import sys, itertools, functools, math
from collections import defaultdict, namedtuple, deque

lines = open(sys.argv[1]).readlines()
NR = len(lines) - 2
NC = len(lines[0].strip()) - 2
S = lines[0].index('.') + 0j
E = lines[-1].index('.') + (NR+1)*1j
bbr = defaultdict(list) 
bbc = defaultdict(list)
 
BM = {'v': 1j, '>': 1, '^': -1j, '<': -1, '.': 0j}

for i, ln in enumerate(lines):
    for j, c in enumerate(ln):
        b = BM.get(c, 0j)
        if b.real:
            bbr[i].append((j, b))
        if b.imag:
            bbc[j].append((i*1j, b))

rpos = lambda r: (int(r.imag)-1) % NR + 1
cpos = lambda c: (int(c.real)-1) % NC + 1
legal = lambda p: (p in (S, E)) or (1<=p.real<=NC and (1<=p.imag<=NR))

@functools.lru_cache(None)
def b_at(t):
   bs = {} 
   for r, std in bbr.items():
       for st, d in std:
           bs[st, r] = cpos(st+d*t) + r*1j
   for c, std in bbc.items():
       for st, d in std:
           bs[c, st] = c + rpos(st+d*t)*1j
   return set(bs.values())

State = namedtuple('State', 'pos, t')

def search(st, en, tm):
    nbs = (NR*NC)/math.gcd(NR, NC)
    best = 1e99 
    q = deque([State(st, tm)])
    visited = set()
    while q:
        st = q.popleft()
        bsn = st.t % nbs
        if st.pos == en:
            best = min(best, st.t)
            continue
        vs = (st.pos, bsn)
        if vs in visited: continue
        visited.add(vs) 
        if st.t >= best:
            continue
        nogo = b_at(bsn)
        choices = [x for act in BM.values()
                   if (x:=State(st.pos+act, st.t+1))
                   if legal(x.pos) and x.pos not in nogo]
        q.extend(choices)
    return best-1

t1 = search(S, E, 0)
t2 = search(E, S, t1)
t3 = search(S, E, t2)
print(t1, t3)

