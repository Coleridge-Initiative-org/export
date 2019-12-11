# Define function

def world():
    print("Hello, world!!!")


def add_8(x):
    print(x + 8)


def dummy_counts(df):
    # only get columns that are dummied
    dummy = [c for c in df.columns if df[c].dtype == 'uint8']

    # check if all counts are at least 10
    less_10 = [var for var in dummy if df[var].value_counts()[0] < 10 or df[var].value_counts()[1] < 10]

    #if there are none that don't satisfy condition print all the counts, else print the offenders
    if len(less_10) > 0:
        print("These dummy variables didn't have counts of at least 10 for both when they are 1 or 0: \n")
        return([print(var) for var in less_10])
    else:
    # get the value counts for each dummy
        return([print(df[var].value_counts()) for var in dummy])
