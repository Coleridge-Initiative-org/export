# requires pandas
import pandas


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

#Creating a crosstab that returns a table, but with values less than 10 returned to NaN
def fuzzy_crosstab(col1,col2):

    #Create the initial crosstab
    xtab = pd.crosstab(col1, col2)

    #Reset the index so you may loop over the columns
    xtab_fixed = xtab.reset_index()

    #Loop over the columns, finding which columns are a int64 dtype
    #If column type is numeric, replace values < 10 with NaN
    for i in xtab_fixed.columns:
        if xtab_fixed[i].dtype == 'int64':
            xtab_fixed.loc[xtab_fixed[i] < 10, i] = 'NaN'
    return xtab_fixed
