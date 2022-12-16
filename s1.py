import sys

inp = sys.stdin.read()

elf_cals = [sum(int(x) for x in lines)
            for elf in inp.split('\n\n')
            if (block := elf.strip())
            if (lines := block.split())]

max_elf = max(elf_cals)
print(f"The elf with the most has {max_elf} calories")

top_three = sorted(elf_cals, reverse=True)[:3]
print(f"Top three elves have total of {sum(top_three)} calories")

import pandas as pd
import io
elves = (pd.read_csv(
    io.StringIO(('"'
       + inp.strip()
         .replace("\n\n",'","')
       + '"')
       .replace("\n", ",")),
    header=None)
    .stack()
    .astype(str)
    .apply(lambda s: sum(int(x) for x in s.split(",")))
    .sort_values(ascending=False)
    .iloc[:3]).to_frame().apply(lambda col: print(col.max(), col.sum()))

