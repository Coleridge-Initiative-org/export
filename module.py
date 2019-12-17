# finds counts for dummy variables and either gives counts if all satisfy or
# prints the names of the dummies that don't satisfy the condition
def dummy_counts(df, cutoff = 10):
    # only get columns that are dummied
    dummy = [c for c in df.columns if df[c].dtype == 'uint8']

    # check if all counts are at least 10
    less = [var for var in dummy if df[var].value_counts()[0] < cutoff or df[var].value_counts()[1] < cutoff]

    #if there are none that don't satisfy condition print all the counts, else print the offenders
    if len(less) > 0:
        print("These dummy variables didn't have counts of at least 10 for both when they are 1 or 0: \n")
        return([print(var) for var in less])
    else:
    # get the value counts for each dummy
        return([print(df[var].value_counts()) for var in dummy])
