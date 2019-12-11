# Import classes from your brand new package
import module
import pandas as pd


## NOTE: Included print("\n") under each function call so it's easy to designate
## between outputs

#call function
module.world()
print("\n")

#call add_8 function
module.add_8(2)
print("\n")

# test dummy_counts function
# get a series
s = pd.Series(list('abcaaaaaaaaaaaaaaaaabbbbbbbbbbbbbb'))
# make dummies of the series
d = pd.get_dummies(s)

#call function when it should give list of columns that don't pass test
module.dummy_counts(d)
print("\n")

#columns that should pass test
module.dummy_counts(d[['a','b']])
print("\n")
