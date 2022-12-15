import re,pprint,io,operator,pathlib,pandas
N=3
S=('max','sum')
print(re.sub(r"(?m)(^ )|([\{\}\',])",'',
      pprint.pformat(
          dict(
              zip(S,
                  pandas.read_csv(
                  io.StringIO((pathlib.Path('./1.txt')
                      .read_text().strip().replace("\n\n",','))
                      .replace("\n"," ")),header=None)
                  .stack()
                  .astype(str)
                  .apply(lambda s:sum(map(int,s.split())))
                  .sort_values()
                  .iloc[-N:]
                  .to_frame(S[0][0])
                  .apply(lambda c:[operator.methodcaller(m)(c) for m in S])
                  .m.to_list())),
          width=1)))
