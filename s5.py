import sys, re, copy

data = sys.stdin.read()
pic, moves = [txt.split('\n') for txt in data.split('\n\n')]

stacks = [[crate
         for line in pic
             if line[:2] != ' 1'
             if i < len(line)
             if (crate:=line[i])!=' '][::-1]
         for i in range(1,34,4)]

def move(stacks, retain):
    stacks = copy.deepcopy(stacks) 
    for move in moves:
        m = re.match(r'(?i)move (\d+) from (\d) to (\d)', move)
        if m:
            n,frm,to = [int(m.group(i)) for i in range(1,4)]
            pick = stacks[frm-1][-n:]
            del stacks[frm-1][-n:]
            stacks[to-1].extend(pick[::retain])
    return stacks

print(''.join(s[-1] for s in move(stacks,-1)))

print(''.join(s[-1] for s in move(stacks,1)))


