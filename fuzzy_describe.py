#Adjusts the describe fiunction by aggregating 5 above and below the desired percentile
def fuzzy_describe(self, percentiles=None, include=None, exclude=None):
        if self.ndim >= 3:
            msg = "describe is not implemented on Panel objects."
            raise NotImplementedError(msg)
        elif self.ndim == 2 and self.columns.size == 0:
            raise ValueError("Cannot describe a DataFrame without columns")

        if percentiles is not None:
            # explicit conversion of `percentiles` to list
            percentiles = list(percentiles)

            # get them all to be in [0, 1]
            self._check_percentile(percentiles)

            # median should always be included
            if 0.5 not in percentiles:
                percentiles.append(0.5)
            percentiles = np.asarray(percentiles)
        else:
            #Stating which percentiles to retreive
            percentiles = np.array([0.2, 0.25, 0.3, 0.45, 0.5, 0.55, 0.7, 0.75, 0.8])

        # sort and check for duplicates
        unique_pcts = np.unique(percentiles)
        if len(unique_pcts) < len(percentiles):
            raise ValueError("percentiles cannot contain duplicates")
        percentiles = unique_pcts

        formatted_percentiles = format_percentiles(percentiles)

        #Getting the count, mean, and standard deviation for numeric data
        def describe_numeric_1d(series):
            stat_index = (['count', 'mean', 'std'] +
                            formatted_percentiles)
            d = ([series.count(), series.mean(), series.std()] +
                    series.quantile(percentiles).tolist())
            return pd.Series(d, index=stat_index, name=series.name)

        #Getting the count of unique values for cateogrical data
        def describe_categorical_1d(data):
            names = ['count', 'unique']
            objcounts = data.value_counts()
            count_unique = len(objcounts[objcounts != 0])
            result = [data.count(), count_unique]
            if result[1] > 0:
                top, freq = objcounts.index[0], objcounts.iloc[0]

                if is_datetime64_any_dtype(data):
                    tz = data.dt.tz
                    asint = data.dropna().values.view('i8')
                    top = Timestamp(top)
                    if top.tzinfo is not None and tz is not None:
                        # Don't tz_localize(None) if key is already tz-aware
                        top = top.tz_convert(tz)
                    else:
                        top = top.tz_localize(tz)
                    names += ['top', 'freq', 'first', 'last']
                    result += [top, freq,
                                Timestamp(asint.min(), tz=tz),
                                Timestamp(asint.max(), tz=tz)]
                else:
                    names += ['top', 'freq']
                    result += [top, freq]

            return pd.Series(result, index=names, name=data.name)

        #Determining the dara type of the data being described
        def describe_1d(data):
            if is_bool_dtype(data):
                return describe_categorical_1d(data)
            elif is_numeric_dtype(data):
                return describe_numeric_1d(data)
            elif is_timedelta64_dtype(data):
                return describe_numeric_1d(data)
            else:
                return describe_categorical_1d(data)

        if self.ndim == 1:
            return describe_1d(self)
        elif (include is None) and (exclude is None):
            # when some numerics are found, keep only numerics
            data = self.select_dtypes(include=[np.number])
            if len(data.columns) == 0:
                data = self
        elif include == 'all':
            if exclude is not None:
                msg = "exclude must be None when include is 'all'"
                raise ValueError(msg)
            data = self
        else:
            data = self.select_dtypes(include=include, exclude=exclude)

        ldesc = [describe_1d(s) for _, s in data.iteritems()]
        # set a convenient order for rows
        names = []
        ldesc_indexes = sorted((x.index for x in ldesc), key=len)
        for idxnames in ldesc_indexes:
            for name in idxnames:
                if name not in names:
                    names.append(name)

        #Once dataframe is returned, concat to an index
        d = pd.concat(ldesc, join_axes=pd.Index([names]), axis=1)

        #Copy the columns and transpose the data
        d.columns = data.columns.copy()
        almost_fuzz = d.T

        #Create the fuzzy percentiles
        almost_fuzz['25%'] = (almost_fuzz['20%'] + almost_fuzz['30%'])/2
        almost_fuzz['50%'] = (almost_fuzz['45%'] + almost_fuzz['55.0%'])/2
        almost_fuzz['75%'] = (almost_fuzz['70%'] + almost_fuzz['80%'])/2
        
        #Determine which columns are necessary for the fuzzy describe and transpose
        fuzzy = almost_fuzz[['count','mean','std','25%','50%','75%']].T
        fuzzy_clean = pd.DataFrame()

        #Must now drop columns with counts less than 10
        for i in fuzzy.columns:
            if fuzzy[i][0] >= 10:
                fuzzy_clean = pd.concat([fuzzy_clean,fuzzy[i]], axis = 1, sort = False)
            else:
                print("Column "+i+" cannot be included in the describe as it is has a count less than 10")
                pass
        return fuzzy_clean