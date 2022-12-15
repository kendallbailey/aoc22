import sys
import numpy as np
import functools
from itertools import takewhile, product
import operator

lines = [l.strip() for l in sys.stdin.readlines()]
nums = [int(n) for l in lines for n in l]
I, J = len(lines),len(lines[0])
mat = np.array(nums, int).reshape(I,J)

# look 4 directions from i,j
slices = lambda i,j: (mat[:i,j],mat[i+1:,j],mat[i,:j],mat[i,j+1:])

# iterator over interior of coordinate space
ijs = lambda: product(range(1,I-1), range(1,J-1))

# count how many elements are in an iterator by consuming it
isz = lambda iter: functools.reduce(max,enumerate(iter,1),(0,))[0]

# is a tree of a given height visible from i,j
viz = lambda i,j: functools.partial(operator.gt,mat[i,j])

# visible trees
print(I*2 + J*2 - 4
   + sum(any((mat[i,j]>sl).all() for sl in slices(i,j)) for i,j in ijs()))

def scenic(ij):
    s = [isz(takewhile(viz(*ij),xf(sl)))
         for xf,sl in zip([reversed,lambda _:_]*2,slices(*ij))]

    # add 1 when the view fails to hit the boundary, then multiply
    i,j = ij
    dists = (i,I-i-1,j,J-j-1)
    return np.product([x+(x<d) for x,d in zip(s,dists)])

# max scenic score
print(max(map(lambda ij:scenic(ij),ijs())))
