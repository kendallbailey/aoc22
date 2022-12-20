import sys, numpy as np
from itertools import repeat, chain
from collections import deque


def mix(nbrs, fact=1, times=1):
    orig = list(enumerate(nbrs*fact))
    circ = deque(orig)
    for itm in chain.from_iterable(repeat(orig, times)):
        # put the i_th element in the correct relative position
        pos = circ.index(itm)
        circ.rotate(-pos)
        circ.popleft()
        circ.rotate(-itm[1])
        circ.appendleft(itm)

    # find the zero position
    zoff = next(i for i, (_, z) in enumerate(circ) if not z)
    # compute the puzzle answer
    return sum(circ[k % len(nbrs)][1]
               for k in np.array([1, 2, 3])*1000 + zoff)

inp = np.array([int(x.strip()) for x in open(sys.argv[1]).readlines()])
print(mix(inp))
print(mix(inp, 811_589_153, 10))
