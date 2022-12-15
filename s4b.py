import sys

nums = list(map(int,(n for line in sys.stdin.readlines()
                  for r in line.split(',')
                  for n in r.split('-'))))
pairs = [tuple(nums[i:i+2]) for i in range(0,len(nums),2)]

sets = [tuple(map(set,(range(t[0],t[1]+1) for t in pairs[i:i+2])))
        for i in range(0,len(pairs),2)] 

contained = [bool(s[0]<=s[1] or s[1]<=s[0]) for s in sets]

print(sum(contained))

overlapped = [bool(s[0]&s[1]) for s in sets]
print(sum(overlapped))
