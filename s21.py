import sys
from operator import add, sub, mul, truediv as div

opmap = {'+': add, '-': sub, '*': mul, '/': div}

# original monkey list
mk = {nv[0]: (int(nv[1]) if not any(x in nv[1] for x in opmap) else nv[1].split())
      for ln in sys.stdin.readlines() if (nv := ln.strip().split(': '))}

def yell(mk, n, humn=None):
    if n == 'humn' and humn is not None:
        return humn
    if isinstance(mk[n], int):
        return mk[n]

    x, op, y = mk[n]
    return opmap[op](*(yell(mk, n, humn) for n in (x, y)))

print(int(yell(mk, 'root')))

# Change root to a subtraction function between left and right operands
left, _, right = mk['root']
mk['root'] = (left, '-', right)

# Find a root of the guess() function
guess = lambda k: yell(mk, 'root', k)

def search(x, dx):
    fx = guess(x)
    while abs(fx) > 0:
        fpx = (guess(x+dx) - fx) / dx
        x = x - fx/fpx
        fx = guess(x)

    return x

print(int(search(0, 1)))
