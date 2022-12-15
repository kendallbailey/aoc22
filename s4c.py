import sys
from functools import reduce
from operator import add

from itertools import islice, count, tee, takewhile, cycle, chain, repeat, groupby

# infinite generator expressions
N = 0 if len(sys.argv)<2 else float(sys.argv[1])
if N:
    raw = sys.stdin.readlines()
    data = chain(islice(cycle(raw), len(raw)*int(N)), repeat(''))
else:
    data = (sys.stdin.readline() for _ in count())

# make it finite
lines = takewhile(lambda x:x, data)

no_seps = (x.replace(',',' ').replace('-',' ') for x in lines)

txtnums = (n for x in no_seps for n in x.split())

nums = map(int,txtnums)

rangebounds = map(lambda x:x[1]+x[0]%2, enumerate(nums))

numpairs = zip(*[rangebounds]*2)

ranges = (range(*x) for x in numpairs)

sets = map(set,ranges)

setpairs = zip(*[sets]*2)

# We have two puzzles to solve from the sequence of set pairs
p1, p2 = tee(setpairs)
p1v = (bool(a<=b or b<=a) for a,b in p1)
p2v = (bool(a&b) for a,b in p2)
sol = reduce(lambda a,b:tuple(map(add,a,b)), zip(p1v,p2v))
print(sol)
