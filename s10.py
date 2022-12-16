import sys, numpy as np

def cpu():
    yield (cyc:=1),(x:=1)
    cyc+=1
    for c in sys.stdin.readlines():
        cmd, *args = c.split()
        if cmd == 'addx':
            yield cyc, x
            yield cyc+1, (x:=x+int(args[0]))
            cyc += 2
        else:
            yield cyc, x
            cyc += 1 

v = set(range(20,221,40))
acc = 0
screen = [['.']*40 for _ in range(7)]
for cyc, x in cpu():
    acc += (cyc*x) if cyc in v else 0
    r,c = divmod(cyc-1,40)
    screen[r][c] = ' #'[abs(x-c)<=1]

print(acc)
print('\n'.join(''.join(l[:40]) for l in screen[:6])) 
