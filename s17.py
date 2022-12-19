import sys, time
from itertools import count, islice

inp = sys.stdin.read().strip()

ROCKS=[ [(x, 0) for x in range(2, 6)],
        [(3, 0), (2, 1), (3, 1), (4, 1), (3, 2)],
        [(x, 0) for x in range(2,5)] + [(4,1), (4, 2)],
        [(2, i) for i in range(0, 4)],
        [(2, 0), (3, 0), (2, 1), (3, 1)] ]

def shapes():  # forever repeating sequence of rocks
    while True:
        for r in ROCKS: yield r

pause = 0
ch = 6 # chamber bounds 0 - 6

def mv(g, rock, dx=0, dy=0):
    rock = [(x+dx, y+dy) for x, y in rock]
    if dy>0: return rock  # places rock above all others
    if dy and not dx:
        return all(p[1]>=0 and p not in g for p in rock) and rock 
    if dx and not dy:
        return all(0<=p[0]<=ch and p not in g for p in rock) and rock
    raise ValueError()

def draw(i, g, r, h):
    H = max((c[1] for c in g), default=0)
    rm = max((c[1] for c in r), default=H)
    st = h + max(0, rm-H)
    sc = [['.']*7 for h in range(max(rm, H)+1)]
    for c in (g | set(r)):
        sc[c[1]][c[0]] = '#'
    print(h+1, i+1)
    print('\n'.join( f'{i:15}|' + ''.join(y) + '|'
          for i, y in
          islice(zip(count(st+1, -1), reversed(sc)),50)))
    print(' '*10,'^'*20)
    if pause: time.sleep(pause)

def bottom_shape(g):
    shape = tuple(max((c[1] for c in g if c[0] == i), default=0) for i in range(7)) 
    bottom = tuple(x-min(shape) for x in shape)
    return bottom

def run(N, dN=lambda n: False):
    g = set()
    H = -1
    jx = {'<': -1, '>': 1}
    jp = 0
    rjf = {(tuple(ROCKS[0]), jp, (0,)*7): (0, 0)} # initial 
    i = -1
    shape_iter = shapes()
    offset = 0
    while i+1 < N:
        i += 1
        rock = next(shape_iter)
        if i and not offset:
           key = (tuple(rock), jp, bottom_shape(g))
           if key in rjf: # found a cycle 
               pH, pi = rjf[key]
               rN, cs = (N-i), (i-pi)  # remaining rocks, cycle size
               fit, togo = divmod(N-i, i-pi) 
               offset, i = ((H-pH)*fit), (N-togo)
           else:
               rjf[key] = (H, i)  # remember this in case it repeats
        rock = mv(g, rock, 0, H+4)  # position 3 above highest
        while True:
            j, jp = inp[jp], (jp+1) % len(inp)
            rock = mv(g, rock, jx[j], 0) or rock
            #if dN(i): draw(i, g, rock, H+offset)
            fallen = mv(g, rock, 0, -1)
            #if dN(i): draw(i, g, fallen or rock, H+offset)
            if not fallen:
                g = g | set(rock)
                H = max(H, max(c[1] for c in rock))
                #if dN(i): draw(i, g, (), H+offset)
                break
            rock = fallen
    return H+1+offset

part1 = run(2022)
part2 = run(1_000_000_000_000)

print(part1, part2)

