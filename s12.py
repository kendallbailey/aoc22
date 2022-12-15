import sys
from collections import deque
from operator import le, ge

class Map:
    def __init__(self, txt):
        self.grid = {}
        for i, line in enumerate(txt.split('\n')):
            for j, c in enumerate(line):
                if c == 'S':
                    self.begin = i, j
                elif c == 'E':
                    self.end = i, j
                self.grid[i, j] = ord({'S': 'a', 'E': 'z'}.get(c, c))
        self.up = True  # are we driving up or down?

    def nbr(self, ij):
        # 4 directions
        n = zip((ij[0]+d for d in (-1,0,0,1)), (ij[1]+d for d in (0,-1,1,0)))
        # (to - frm <= 1) if self.up else (to - frm >= -1)
        tst = lambda to, frm: [ge, le][self.up](to-frm, self.up*2-1)
        return [x for x in n if x in self.grid if tst(self.grid[x], self.grid[ij])]

    def bfs(self, st, goal):
        q = deque(d := {st: 0})
        while q:
            for n in self.nbr(ij := q.popleft()):
                if n not in d:
                    d[n] = d[ij] + 1
                    # new value in d, might have achieved the goal
                    if goal(d, n):
                        return d
                    q.append(n)
        return d


m = Map(sys.stdin.read())
# drive up towared the end point
dists = m.bfs(m.begin, lambda dists, _: m.end in dists)
print(dists[m.end])

# now drive down from the end towards a different goal... any 'a'
m.up = False
dists = m.bfs(m.end, lambda _, p: m.grid[p] == ord('a'))
# once we hit the goal, the max dist is the dist to an 'a'
print(max(dists.values()))
