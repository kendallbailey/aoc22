import sys

lines = [x.strip() for x in sys.stdin.readlines()]
ranges = [x.split(',') for x in lines]
pairs = [[list(map(int,y.split('-'))) for y in x] for x in ranges]
sets = [tuple(map(set,(range(r[0],r[1]+1) for r in p)))
        for p in pairs]

contained = [bool(s[0]<=s[1] or s[1]<=s[0]) for s in sets]

print(sum(contained))

overlapped = [bool(s[0]&s[1]) for s in sets]
print(sum(overlapped))
