import pandas as pd
from sweetviz.sv_types import FeatureType
from sweetviz.from_profiling_pandas import is_boolean, is_numeric, is_categorical, could_be_numeric


def determine_feature_type(series: pd.Series, counts: dict,
        must_be_this_type: FeatureType, which_dataframe: str) -> object:
    # Replace infinite values with NaNs to avoid issues with histograms
    # TODO: INFINITE VALUE HANDLING/WARNING
    # series.replace(to_replace=[np.inf, np.NINF, np.PINF], value=np.nan,
    #                inplace=True)
    if counts["value_counts_without_nan"].index.inferred_type.startswith("mixed"):
        raise TypeError(f"\n\nColumn [{series.name}] has a 'mixed' inferred_type (as determined by Pandas).\n"
                        f"This is is not currently supported; column types should not contain mixed data.\n"
                        f"e.g. only floats or strings, but not a combination.\n\n"
                        f"POSSIBLE RESOLUTIONS:\n"
                        f"BEST -> Make sure series [{series.name}] only contains a certain type of data (numerical OR string).\n"
                        f"OR -> Convert series [{series.name}] to a string (if makes sense) so it will be picked up as CATEGORICAL or TEXT.\n"
                        f"     One way to do this is:\n"
                        f"     df['{series.name}'] = df['{series.name}'].astype(str)\n"
                        f"OR -> Convert series [{series.name}] to a numerical value (if makes sense):\n"
                        f"     One way to do this is:\n"
                        f"     df['{series.name}'] = pd.to_numeric(df['{series.name}'], errors='coerce')\n"
                        f"     # (errors='coerce' will transform string values to NaN, that can then be replaced if desired;"
                        f" consult Pandas manual pages for more details)\n"
                        )

    try:
        # TODO: must_be_this_type ENFORCING
        if counts["distinct_count_without_nan"] == 0:
            # Empty
            var_type = FeatureType.TYPE_ALL_NAN
            # var_type = FeatureType.TYPE_UNSUPPORTED
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
    # CAT/BOOL -> NUM
    # NUM -> CAT
    # NUM -> TEXT
    if must_be_this_type != FeatureType.TYPE_UNKNOWN and \
                must_be_this_type != var_type and \
                must_be_this_type != FeatureType.TYPE_ALL_NAN and \
                var_type != FeatureType.TYPE_ALL_NAN:
        if var_type == FeatureType.TYPE_TEXT and must_be_this_type == FeatureType.TYPE_CAT:
            var_type = FeatureType.TYPE_CAT
        elif (var_type == FeatureType.TYPE_CAT or var_type == FeatureType.TYPE_BOOL ) and \
            must_be_this_type == FeatureType.TYPE_TEXT:
            var_type = FeatureType.TYPE_TEXT
        elif (var_type == FeatureType.TYPE_CAT or var_type == FeatureType.TYPE_BOOL) and \
             must_be_this_type == FeatureType.TYPE_NUM:
            # Trickiest: Coerce into numerical
            if could_be_numeric(series):
                var_type = FeatureType.TYPE_NUM
            else:
                raise TypeError(f"\n\nCannot force series '{series.name}' in {which_dataframe} to be converted from its {var_type} to\n"
                                f"DESIRED type {must_be_this_type}. Check documentation for the possible coercion possibilities.\n"
                                f"POSSIBLE RESOLUTIONS:\n"
                                f" -> Use the feat_cfg parameter (see docs on git) to force the column to be a specific type (may or may not help depending on the type)\n"
                                f" -> Modify the source data to be more explicitly of a single specific type\n"
                                f" -> This could also be caused by a feature type mismatch between source and compare dataframes:\n"
                                f"    In that case, make sure the source and compared dataframes are compatible.\n")
        elif var_type == FeatureType.TYPE_NUM and must_be_this_type == FeatureType.TYPE_CAT:
            var_type = FeatureType.TYPE_CAT
        elif var_type == FeatureType.TYPE_BOOL and must_be_this_type == FeatureType.TYPE_CAT:
            var_type = FeatureType.TYPE_CAT
        elif var_type == FeatureType.TYPE_NUM and must_be_this_type == FeatureType.TYPE_TEXT:
            var_type = FeatureType.TYPE_TEXT
        else:
            raise TypeError(f"\n\nCannot convert series '{series.name}' in {which_dataframe} from its {var_type}\n"
                            f"to the desired type {must_be_this_type}.\nCheck documentation for the possible coercion possibilities.\n"
                            f"POSSIBLE RESOLUTIONS:\n"
                            f" -> Use the feat_cfg parameter (see docs on git) to force the column to be a specific type (may or may not help depending on the type)\n"
                            f" -> Modify the source data to be more explicitly of a single specific type\n"
                            f" -> This could also be caused by a feature type mismatch between source and compare dataframes:\n"
                            f"    In that case, make sure the source and compared dataframes are compatible.\n")
    return var_type
