import sys
from itertools import islice


def rg(a, b):
    return range(a, b + (st := a < b and 1 or -1), st)


def grid(inplines):
    g = {}
    for ln in inplines:
        pts = [tuple(map(int, x.strip().split(','))) for x in ln.split('->')]
        for f, s in zip(pts, islice(pts, 1, None)):
            if f[0] == s[0]:
                for v in rg(f[1], s[1]):
                    g[f[0], v] = '#'
            else:
                for h in rg(f[0], s[0]):
                    g[h, f[1]] = '#'
    return g


def drop(orig, g, lowest, floor):
    snd = orig

    def stop(s):  # is it below the matrix or hit floor?
        return s[1] >= (lowest+(floor and floor-1 or 0))

    while not stop(snd):
        if (n := (snd[0], snd[1]+1)) not in g:
            snd = n
        elif (n := (snd[0]-1, snd[1]+1)) not in g:
            snd = n
        elif (n := (snd[0]+1, snd[1]+1)) not in g:
            snd = n
        else:
            g[snd] = 'o'  # stopped inside the matrix
            break

    if floor:
        if stop(snd):
            g[snd] = 'o'  # hit the floor
        return None if (snd == orig) else snd
    return None if stop(snd) else snd


def pour(orig, g, floor=0):
    lowest = max(x[1] for x in g if g[x] == '#')
    while drop(orig, g, lowest, floor):
        pass
    return sum(c=='o' for c in g.values())


inp = sys.stdin.readlines()
print(pour((500, 0), grid(inp)))
print(pour((500, 0), grid(inp), 2))
