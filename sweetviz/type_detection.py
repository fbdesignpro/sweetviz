import pandas as pd
from sweetviz.sv_types import FeatureType
from sweetviz.from_profiling_pandas import is_boolean, is_numeric, is_categorical


def determine_feature_type(series: pd.Series, counts: dict,
        must_be_this_type: FeatureType, which_dataframe: str) -> object:
    # Replace infinite values with NaNs to avoid issues with histograms
    # TODO: INFINITE VALUE HANDLING/WARNING
    # series.replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan,
    #                inplace=True)
    if counts["value_counts_without_nan"].index.inferred_type.startswith("mixed"):
        raise TypeError(f"Column {series.name} has a 'mixed' inferred_type (as determined by Pandas). "
                        f"This is is not currently supported; column types should not contain mixed data."
                        f"e.g. only float, or strings, but not a combination.")

    try:
        # TODO: must_be_this_type ENFORCING
        if counts["distinct_count_without_nan"] == 0:
            # Empty
            var_type = FeatureType.TYPE_UNSUPPORTED
        elif is_boolean(series, counts):
            var_type = FeatureType.TYPE_BOOL
        elif is_numeric(series, counts):
            var_type = FeatureType.TYPE_NUM
        elif is_categorical(series, counts):
            var_type = FeatureType.TYPE_CAT
        else:
            var_type = FeatureType.TYPE_TEXT
    except TypeError:
        var_type = FeatureType.TYPE_UNSUPPORTED

    # COERCE: only supporting the following for now:
    # TEXT -> CAT
    # CAT/BOOL -> TEXT
    # NUM -> CAT
    # NUM -> TEXT
    if must_be_this_type  != FeatureType.TYPE_UNKNOWN and \
                must_be_this_type != var_type:
        if var_type == FeatureType.TYPE_TEXT and must_be_this_type == FeatureType.TYPE_CAT:
            var_type = FeatureType.TYPE_CAT
        elif (var_type == FeatureType.TYPE_CAT or var_type == FeatureType.TYPE_BOOL ) and \
            must_be_this_type == FeatureType.TYPE_TEXT:
            var_type = FeatureType.TYPE_TEXT
        elif var_type == FeatureType.TYPE_NUM and must_be_this_type == FeatureType.TYPE_CAT:
            var_type = FeatureType.TYPE_CAT
        elif var_type == FeatureType.TYPE_NUM and must_be_this_type == FeatureType.TYPE_TEXT:
            var_type = FeatureType.TYPE_TEXT
        else:
            raise TypeError(f"Cannot force series '{series.name}' in {which_dataframe} to be from its type {var_type} to\n"
                            f"DESIRED type {must_be_this_type}. Check documentation for the possible coercion possibilities.\n"
                            f"This can be solved by changing the source data or is sometimes caused by\n"
                            f"a feature type mismatch between source and compare dataframes.")
    return var_type
