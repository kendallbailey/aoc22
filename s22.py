import sys, pdb, copy, time
import numpy as np

inp = open(sys.argv[1]).read()
maplines, pathlines = inp.split('\n\n') 
map = {}
for row, ml in enumerate(maplines.split('\n')):
    for col, c in enumerate(ml):
        if c == ' ': continue 
        map[col, row] = c

sz = (max(x for x, y in map), max(y for x, y in map))
path = pathlines.split('\n')[0].strip()

tup = tuple
a = lambda *c: np.array(c)

dr = {(1, 0): {'L': a(0, -1), 'R': a(0, 1)},   # R
      (-1, 0): {'L': a(0, 1), 'R': a(0, -1)},  # L
      (0, 1): {'L': a(1, 0), 'R': a(-1, 0)},   # D
      (0, -1): {'L': a(-1, 0), 'R': a(1, 0)}}  # U
drn = {(1, 0): 0, # R
      (-1, 0): 2,  # L
      (0, 1): 1,   # D
      (0, -1): 3}  # U
drc = {(1, 0): '>', # R
      (-1, 0): '<',  # L
      (0, 1): 'v',   # D
      (0, -1): '^'}  # U
K=50

def draw(m, k, inst = ''):
    space = [[' ' for _ in range(sz[0]+1)] for _ in range(sz[1]+1)]
    for (x, y), c in m.items():
        space[y][x] = c
    sl = 58
    print(f'\n\n\n{inst}\n')
    print('\n'.join(''.join(y) for y in space[max(k-sl,0):min(k+sl, len(space)-1)]))



fac = a(1, 0)
start = a(min(x for x, y in map if y == 0), 0)  # upper left corner

def ssf(pos, fac):
    other = max(y for y in range(max(sz)) if tup(pos - y*fac) in map)
    return tup(pos - other*fac), fac

def csf(pos, fac):
    # 14 cases
    f = drn[tup(fac)]
    # E1
    if f==2 and pos[0]==K and pos[1]>=K: return (pos[1]-K, 2*K), a(0, 1)
    if f==3 and pos[1]==2*K and pos[0]<K: return (K, K+pos[0]), a(1, 0)
    # E2
    if f==2 and pos[0]==0 and pos[1]<3*K: return (K, 3*K-pos[1]-1), a(1, 0)
    if f==2 and pos[0]==K and pos[1]<K: return (0, 3*K-pos[1]-1), a(1, 0)
    # E3
    if f==3 and pos[1]==0 and pos[0]<2*K: return (0, 2*K+pos[0]), a(1, 0)
    if f==2 and pos[0]==0 and pos[1]>=3*K: return (pos[1]-2*K,0), a(0, 1)
    # E4
    if f==0 and pos[0]==2*K-1 and pos[1]<2*K: return (pos[1]+K, K-1), a(0, -1)
    if f==1 and pos[1]==K-1 and pos[0]>=2*K: return (2*K-1, pos[0]-K), a(-1, 0)
    # E5
    if f==0 and pos[0]==3*K-1: return (2*K-1, 3*K-pos[1]-1), a(-1, 0)
    if f==0 and pos[0]==2*K-1 and pos[1]>=2*K: return (3*K-1, 3*K-pos[1]-1), a(-1, 0)
    # E6
    if f==0 and pos[0]==K-1 and pos[1]>=3*K: return (pos[1]-2*K, 3*K-1), a(0, -1)
    if f==1 and pos[1]==3*K-1 and pos[0]>=K: return (K-1, pos[0]+2*K), a(-1, 0)
    # E7
    if f==3 and pos[1]==0 and pos[0]>=2*K: return (pos[0]-2*K, 4*K-1), a(0, -1)
    if f==1 and pos[1]==4*K-1: return (pos[0]+2*K, 0), a(0, 1)

def nxt(pos, fac, sf):
    step = tup(pos+fac)
    on = map.get(step, None)
    if on == '#': return pos, fac
    if on == '.': return a(*step), fac
    # stepped off the edge, use step function
    step, nfac = sf(pos, fac)
    on = map[step]
    if on == '.': return a(*step), nfac
    return pos, fac


def walk(pos, path, fac, sf=ssf):
    i = 0
    inst = path[:10]
    while i < len(path):
        if path[i] in ('L', 'R'):
            inst = path[:10]
            fac = dr[tup(fac)][path[i]]
            i += 1
            continue
        nc = path[i:i+10].split('L')[0].split('R')[0]
        n = int(nc)
        i += len(nc)
        for _ in range(n):
            npos, nfac = nxt(pos, fac, sf)
            if tup(npos) == tup(pos):
                break
            pos, fac = npos, nfac
            map2[tup(pos)] = drc[tup(fac)]
            #draw(map2, pos[1], inst)
            #time.sleep(0.5)
    return pos, fac

#map2 = copy.deepcopy(map)
#end, ef = walk(start, path, fac)
#print((end[1]+1)*1000 + (end[0]+1)*4 + drn[tup(ef)])
#draw(map2)
#
map2 = copy.deepcopy(map)
end, ef = walk(start, path, fac, csf)
print((end[1]+1)*1000 + (end[0]+1)*4 + drn[tup(ef)])
