# Import classes from your brand new package
import module
import pandas as pd

#call function
module.world()

#call add_8 function
module.add_8(2)

# test dummy_counts function
# get a series
s = pd.Series(list('abcaaaaaaaaaaaaaaaaabbbbbbbbbbbbbb'))
# make dummies of the series
d = pd.get_dummies(s)

#call function when it should give list of columns that don't pass test
module.dummy_counts(d)

#columns that should pass test
module.dummy_counts(d[['a','b']])
