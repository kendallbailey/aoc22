import sys
from collections import deque, defaultdict
from itertools import count

gr = {}
inp = open(sys.argv[1]).readlines()
for i, ln in enumerate(inp):
    for j, c in enumerate(ln.strip()):
        gr[j + i*1j] = c

look = deque([(-1j, -1-1j, 1-1j), # N
              (1j, 1+1j, -1+1j), #S
              (-1, -1-1j, -1+1j), # W
              (1, 1-1j, 1+1j), #E
               ])
adj = set(x for d in look for x in d)  # all 8 adj cells

def round():
    frmto = {}
    mv = 0
    for p, c in gr.items():
        if c == '.': continue
        if all(gr.get(x, '.')=='.' for x in (p+a for a in adj)):
            continue # elf is isolated

        for ld in look:
            if all(gr.get(x, '.')=='.' for x in (p+a for a in ld)):
                frmto[p] = p+ld[0]
                break

    confl = defaultdict(int)
    for to in frmto.values():
        confl[to] += 1
    for frm, to in frmto.items():
        if confl[to] == 1:
            gr[frm] = '.'
            gr[to] = '#'
            mv += 1
    look.rotate(-1)
    return mv

def calcspace(p=False):
    esp = {x:y for x, y in gr.items() if y=='#'}
    rb = min(x.real for x in esp), max(x.real for x in esp)
    ib = min(x.imag for x in esp), max(x.imag for x in esp)
    if p:
        for ln in range(int(ib[0]), int(ib[1]+1)):
            for c in range(int(rb[0]), int(rb[1]+1)):
                sys.stdout.write(gr.get(c+ln*1j, '.'))
            sys.stdout.write('\n')
        print('')
    return (rb[1]-rb[0]+1)*(ib[1]-ib[0]+1) - len(esp)

space = {}
for i in count(1):
    if round() == 0:
        end = i
        space[i] = calcspace()
        break
    if i == 10: space[i] = calcspace()

print(next(iter(space.values())))
print(end)

 