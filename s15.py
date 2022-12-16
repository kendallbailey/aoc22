import re, sys
from functools import reduce
from operator import sub

inp = sys.stdin.readlines()
quads = [list(map(int, m.groups())) for ln in inp if
         (m := re.search(r'x=(.*?), y=(.*?):.*x=(.*?), y=(.*)\s*$', ln))]
sn, bn = zip(*[map(tuple, (x[:2], x[2:])) for x in quads])
radii = list(map(lambda a, b: sum(map(abs, map(sub, a, b))), sn, bn))

def mrgl(l1, l2):
    'Merge two lists of sorted spans'
    ms = (a[0], max(a[1], b[1])) if (a:=l1[-1])[1]+1 >= (b:=l2[0])[0] else None
    return l1+l2 if not ms else (l1[:-1] + (ms,) + l2[1:])

# Range of sensor visibility of sensor s with radius r on line y
xviz = lambda s, r, y: None if (offs := r - abs(y - s[1])) < 0 else (s[0]-offs, s[0]+offs)
# reduce a list of spans to eliminate overlap between spans
sred = lambda spans: list(reduce(mrgl, map(lambda x:(x,), sorted(spans))))
# visible spans on a row
spans = lambda row: sred(filter(None,(xviz(s, r, row) for s, r in zip(sn, radii))))

# report sensor coverage on a given row
spl = spans(row := int(sys.argv[1]))
print(sum(x[1]-x[0] for x in spl) + 1 - sum(x[1] == row for x in set(bn)))

def freq(H):  # assume first gap is the unique one we are looking for
    #rws = ((k, spans(k)) for k in ((i//2, H-i//2-1)[i%2] for i in range(H)))
    rws = ((k, spans(k)) for k in range(H+1, -1, -1))
    rn, spl = next(filter(lambda x: len(x[1])>1, rws))
    print(rn)
    return rn + 4_000_000*(spl[0][1]+1)

print(freq(int(sys.argv[2])))
