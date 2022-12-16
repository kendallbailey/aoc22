import sys, re, functools, operator, itertools, collections

ms = [m.groupdict() for ln in sys.stdin
      if (m := re.search(r'(?P<loc>..) h.*=(?P<flow>\d+).*v\w*?\s(?P<tunnels>.*)', ln))]
valves = {m['loc']: vp for m in ms if (vp := int(m['flow']))}
tunnels = {m['loc']: set(x.strip() for x in m['tunnels'].split(',')) for m in ms}


def run(n, ddt):
    wp = frm = ('AA',) * n
    # time, worker pos, worker from, ttl pressure, opened valves
    q = collections.deque([(1, wp, frm, 0, set())])
    opt = 0
    v = {}
    maxp, nvalves = sum(valves.values()), len(valves)

    while q:
        t, wp, frm, ttl, opened = q.popleft()
        if ttl <= v.get((t, wp), -1):
            continue  # already know as good a path to this state
        v[t, wp] = ttl

        if t == ddt or len(opened) == nvalves:
            # either all valves are open or time has run out
            opt = max(opt, ttl + maxp*(ddt-t))
            continue

        # compute choices for each worker
        choice = tuple([] for _ in wp)
        for cl, loc, ploc in zip(choice, wp, frm):
            if loc in valves and loc not in opened:
                cl.append((loc, loc, set((loc,))))  # stay and open a valve
            for d in (tunnels[loc] - set((ploc, ))):  # avoid backtracking
                cl.append((d, loc, set()))  # move without opening a valve

        # now that choices for each worker are described, queue all combinations
        # of those choices
        for cv in filter(None, itertools.product(*choice)):
            nwp, nfrm, to_open = zip(*cv)
            newo = functools.reduce(operator.or_, to_open, opened)
            nttl = ttl + sum(valves[x] for x in newo)
            q.append((t+1, nwp, nfrm, nttl, newo))  # type: ignore

    return opt

print(run(1, 30))
print(run(2, 26))
