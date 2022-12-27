import sys
from math import log

lines = open(sys.argv[1]).readlines()
nums = [x.strip() for x in lines]

mult = lambda c: int({'-': -1, '=': -2}.get(c, c))
char = lambda n: str({-1: '-', -2: '='}.get(n, n)) 

def decode(n):
    t = 0
    for i, c in enumerate(reversed(n)):
        t += 5**i * mult(c)
    return t

def encode(n):
    digc = int(log(n)/log(5)) + 2  # might need an extra digit
    dm = [0]*(digc+1)
    for i in range(digc-1, -1, -1):
        fp = 5**i
        v = n//fp
        dm[i] = v
        n -= v*fp

    for pwr in range(digc):
        m = dm[pwr]
        if m > 2:
            dm[pwr+1] += 1
            dm[pwr] -= 5
    s = ''.join(str(char(dm[i])) for i in range(digc-1, -1, -1))
    return s.lstrip('0')


ttl = sum(decode(n) for n in nums)
print(encode(ttl))

