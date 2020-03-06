# requires a few packages
import pandas as pd
import matplotlib.pyplot as plt


# finds counts for dummy variables and either gives counts if all satisfy or
# prints the names of the dummies that don't satisfy the condition
def dummy_counts(df, cutoff = 10):
    # only get columns that are dummied
    dummy = [c for c in df.columns if df[c].dtype == 'uint8']

    # check if all counts are at least 10
    less = [var for var in dummy if df[var].value_counts()[0] < cutoff or df[var].value_counts()[1] < cutoff]

    #make cutoff a string so it can be used in the .format later
    cutoff = str(cutoff)

    #if there are none that don't satisfy condition print all the counts, else print the offenders
    if len(less) > 0:
        print("These dummy variables didn't have counts of at least {} for both when they are 1 or 0: \n".format(cutoff))
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

#Creating safe boxplot for one statistic
def safe_boxplot(df, stat, positions=None, widths=None, vert=True, patch_artist=False, shownotches=False, 
                 showmeans=False, showcaps=True, showbox=True, showfliers=False, boxprops=None, whiskerprops=None, 
                 flierprops = None, medianprops=None, capprops=None, meanprops=None, meanline=False, 
                 manage_ticks=True, zorder=None):
    
    # find fuzzy 25, 50, and 75 quartiles
    fuzzy_med = (df[stat].quantile(.45) + df[stat].quantile(.55))/2
    fuzzy_25 = (df[stat].quantile(.20) + df[stat].quantile(.30))/2
    fuzzy_75 = (df[stat].quantile(.70) + df[stat].quantile(.80))/2
    
    # find outlier cutoffs for mins and maxs
    outlier_min = fuzzy_25 - 1.5*(fuzzy_75-fuzzy_25)
    outlier_max = fuzzy_75 + 1.5*(fuzzy_75-fuzzy_25)
    
    # eliminate all outliers
    df_nonoutliers = df[(df[stat] > outlier_min) & (df[stat] < outlier_max)]
    
    # find min and max in non-outliers
    fuzzy_min = (sorted(df_nonoutliers[stat])[0] + sorted(df_nonoutliers[stat])[1])/2
    fuzzy_max = (sorted(df_nonoutliers[stat])[-1] + sorted(df_nonoutliers[stat])[-2])/2
    
    #combine stats into a boxplot
    stats = [
        {'med': fuzzy_med, 'q1': fuzzy_25, 'q3': fuzzy_75, 'whislo': fuzzy_min, 'whishi': fuzzy_max}
    ]
    
    _, ax = plt.subplots()
    
    #return plot
    return(ax.bxp(stats, positions, widths, vert, patch_artist, shownotches, showmeans, 
                  showcaps, showbox, showfliers, boxprops, whiskerprops, flierprops, medianprops, capprops, 
                  meanprops, meanline, manage_ticks, zorder))
