import sys, operator, functools, time

inp = [(dn[0], int(dn[1])) for line in sys.stdin.readlines() if (dn:=line.split())]

def follow(h,t):
    d = tuple(map(operator.sub,h,t))
    ad = tuple(map(abs,d)) 
 
    if max(ad) <= 1: return t
    r = tuple(0 if not r else r//abs(r) for r in d)
    return tuple(map(operator.add,t,r))

def mv(h,d):
    if d=='U': return (h[0], h[1]+1)
    if d=='R': return (h[0]+1, h[1])
    if d=='L': return (h[0]-1, h[1])
    if d=='D': return (h[0], h[1]-1)

def pth(h,d,n):
    for _ in range(n):
        h = mv(h,d)
        yield h 

pvz = lambda v: print('\n'.join(reversed([''.join(l) for l in v])))
def draw(h,s,ts):
    if len(ts)<2: return
    bs = [f(x) for x in ([y[i] for y in [h,s]+ts] for i in (0,1))
              for f in (min,max)]
    patch = [['.' for _ in range(bs[1]-bs[0] + 4)] for _ in range(bs[3]-bs[2]+4)]
    tr = lambda p: (p[0]-bs[0]+2, p[1]-bs[1]+2)  
    def put(p, c):
        p = tr(p)
        patch[p[1]][p[0]] = c
    for i,t in reversed(list(enumerate(ts,1))):
        put(t, str(i) if len(ts) > 1 else 'T')
    put(s, 's')
    put(h, 'H')
    pvz(patch)
    time.sleep(0.003)
    print('\n'*100)

for N in (1,9):
    s = h = (0,0) 
    ts = [s]*N
    visited = set((s,))
    for m in inp:
        for h in pth(h,*m):
            draw(h,s,ts)
            ts[0] = follow(h,ts[0])
            for i in range(1,N):
                ts[i] = follow(ts[i-1],ts[i])
                draw(h,s,ts)
            visited.add(ts[-1])
    print(len(visited))

