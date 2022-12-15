
import sys,pandas as pd;((_1:=3, _2:=pd.Series(range(_1))) and
print(list(pd.DataFrame(
    # Step 4: create a dataframe of scores
    list(
        # Step 3: map the two score functions to the data...
        map(lambda _:[
                  # first score function has winner determined by
                  # difference mod N formula
                  (_2*_1)[(_.M-_.O+1)%_1]+
                  # points for selection
                  _.M+1,
                  # second score function has winner specified in data 
                  _.M*_1+
                  # points for selection, need to map the two
                  # values to a selection using a NxN matrix
                  list(map(lambda _:(_2+_1+_-1)%_1, _2))
                  [_.O][_.M]+1],
          # Step 1: read into a df
         (pd.read_csv(sys.stdin,sep=' ',header=None,names=list('OM'))
          # Step 2: convert to numeric 0,1,2 values
         .apply(lambda _:_.apply(ord))-list(map(ord,'AX')))
          # data points for step 3
         .itertuples(index=False))))
          # Step 5: sum the scores for the two puzzles 
         .sum())))
