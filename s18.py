import sys
from operator import add

inp = sys.stdin.readlines()
g = set(tuple(map(int, (i.strip() for i in x.split(",")))) for x in inp)

def pt(p, dp):
    return tuple(map(add, p, dp))

nbr = [(-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)]

cnt = lambda chk: sum((a not in g and not chk(a)) for p in g for dp in nbr if (a:=pt(p, dp)))

def mk_encl():
    bnds = [[fn(p[i] for p in g) for fn in (min, max)] for i in (0, 1, 2)]
    ir, er = set(), set() 

    def encl(a):
        nonlocal ir, er
        if a in ir: return True
        if a in er: return False
        stk = [a]
        seen = set(stk)
        while stk:
            a = stk.pop()
            if any(not b[0] < d < b[1] for d, b in zip(a, bnds)):
                # search reached open air
                er |= seen
                return False
            for n in (pt(a, dp) for dp in nbr):
                if all(n not in s for s in (g, seen)):
                    seen.add(a)
                    stk.append(n)
        ir |= seen
        return True 
    return encl

print(cnt(lambda x: False))  # don't check for interior air bubbles
print(cnt(mk_encl()))  # identify bubbles

