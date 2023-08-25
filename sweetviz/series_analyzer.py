import pandas as pd
from sweetviz.sv_types import NumWithPercent, FeatureType, FeatureToProcess
from sweetviz.type_detection import determine_feature_type
import sweetviz.series_analyzer_numeric
import sweetviz.series_analyzer_cat
import sweetviz.series_analyzer_text

from distutils.version import LooseVersion

def get_counts(series: pd.Series) -> dict:
    # The value_counts() function is used to get a Series containing counts of unique values.
    value_counts_with_nan = series.value_counts(dropna=False)

    # Fix for data with only a single value; reset_index was flipping the data returned
    if len(value_counts_with_nan) == 1:
        if pd.isna(value_counts_with_nan.index[0]):
            value_counts_without_nan = pd.Series()
        else:
            value_counts_without_nan = value_counts_with_nan
    else:
        reset_value_counts = value_counts_with_nan.reset_index()
        # Force column naming behavior to be similar for value_counts() being reset between 1.x and 2.x.: make sure col 0 is "index" and 1 is series.name
        # -> This is a no-op in Pandas 1.x
        reset_value_counts.rename(columns={reset_value_counts.columns[0]: "index", reset_value_counts.columns[1]:series.name}, inplace=True)

        value_counts_without_nan = (reset_value_counts.dropna().set_index("index").iloc[:, 0])
    # print(value_counts_without_nan.index.dtype.name)

    # IGNORING NAN FOR NOW AS IT CAUSES ISSUES [FIX]
    # distinct_count_with_nan = value_counts_with_nan.count()

    distinct_count_without_nan = value_counts_without_nan.count()
    return {
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
        "num_rows_with_data": series.count(),
        "num_rows_total": len(series),
        # IGNORING NAN FOR NOW AS IT CAUSES ISSUES [FIX]:
        # "value_counts_with_nan": value_counts_with_nan,
        # "distinct_count_with_nan": distinct_count_with_nan,
    }


def fill_out_missing_counts_in_other_series(my_counts:dict, other_counts:dict):
    # IGNORING NAN FOR NOW AS IT CAUSES ISSUES [FIX]
    # to_fill_list = ["value_counts_with_nan", "value_counts_without_nan"]
    to_fill_list = ["value_counts_without_nan"]
    for to_fill in to_fill_list:
        fill_using_strings = True if my_counts[to_fill].index.dtype.name in ('category', 'object') else False
        for key, value in other_counts[to_fill].items():
            if key not in my_counts[to_fill]:
                # If categorical, must do this hack to add new value
                if my_counts[to_fill].index.dtype.name == 'category':
                    my_counts[to_fill] = my_counts[to_fill].reindex(my_counts[to_fill].index.add_categories(key))

                # Add empty value at new index, but make sure we are using the right index type
                if fill_using_strings:
                    my_counts[to_fill].at[str(key)] = 0
                else:
                    my_counts[to_fill].at[key] = 0

def add_series_base_stats_to_dict(series: pd.Series, counts: dict, updated_dict: dict) -> dict:
    updated_dict["stats"] = dict()
    updated_dict["base_stats"] = dict()
    base_stats = updated_dict["base_stats"]
    num_total = counts["num_rows_total"]
    try:
        num_zeros = series[series == 0].count()
    except TypeError:
        num_zeros = 0
    non_nan = counts["num_rows_with_data"]
    base_stats["total_rows"] = num_total
    base_stats["num_values"] = NumWithPercent(non_nan, num_total)
    base_stats["num_missing"] = NumWithPercent(num_total - non_nan, num_total)
    base_stats["num_zeroes"] = NumWithPercent(num_zeros, num_total)
    base_stats["num_distinct"] = NumWithPercent(counts["distinct_count_without_nan"], num_total)


# This generates everything EXCEPT the "detail pane"
def analyze_feature_to_dictionary(to_process: FeatureToProcess) -> dict:
    # start = time.perf_counter()

    # Validation: Make sure the targets are the same length as the series
    if to_process.source_target is not None and to_process.source is not None:
        if len(to_process.source_target) != len(to_process.source):
            raise ValueError
    if to_process.compare_target is not None and to_process.compare is not None:
        if len(to_process.compare_target) != len(to_process.compare):
            raise ValueError

    # Initialize some dictionary values
    returned_feature_dict = dict()
    returned_feature_dict["name"] = to_process.source.name
    returned_feature_dict["order_index"] = to_process.order
    returned_feature_dict["is_target"] = True if to_process.order == -1 else False

    # Determine SOURCE feature type
    to_process.source_counts = get_counts(to_process.source)
    returned_feature_dict["type"] = determine_feature_type(to_process.source, to_process.source_counts,
                                                           to_process.predetermined_type, "SOURCE")
    source_type = returned_feature_dict["type"]

    # Determine COMPARED feature type & initialize
    compare_dict = None
    if to_process.compare is not None:
        to_process.compare_counts = get_counts(to_process.compare)
        compare_type = determine_feature_type(to_process.compare,
                                              to_process.compare_counts,
                                              returned_feature_dict["type"], "COMPARED")
        if compare_type != FeatureType.TYPE_ALL_NAN and \
            source_type != FeatureType.TYPE_ALL_NAN:
            # Explicitly show missing categories on each set
            if compare_type == FeatureType.TYPE_CAT or compare_type == FeatureType.TYPE_BOOL:
                fill_out_missing_counts_in_other_series(to_process.compare_counts, to_process.source_counts)
                fill_out_missing_counts_in_other_series(to_process.source_counts, to_process.compare_counts)
        returned_feature_dict["compare"] = dict()
        compare_dict = returned_feature_dict["compare"]
        compare_dict["type"] = compare_type

    # Settle all-NaN series, depending on source versus compared
    if to_process.compare is not None:
        # Settle all-Nan WITH COMPARE: Must consider all cases between source and compare
        if compare_type == FeatureType.TYPE_ALL_NAN and source_type == FeatureType.TYPE_ALL_NAN:
            returned_feature_dict["type"] = FeatureType.TYPE_TEXT
            compare_dict["type"] = FeatureType.TYPE_TEXT
        elif compare_type == FeatureType.TYPE_ALL_NAN:
            compare_dict["type"] = source_type
        elif source_type == FeatureType.TYPE_ALL_NAN:
            returned_feature_dict["type"] = compare_type
    else:
        # Settle all-Nan WITHOUT COMPARE ( trivial: consider as TEXT )
        if source_type == FeatureType.TYPE_ALL_NAN:
            returned_feature_dict["type"] = FeatureType.TYPE_TEXT

    # Establish base stats
    add_series_base_stats_to_dict(to_process.source, to_process.source_counts, returned_feature_dict)
    if to_process.compare is not None:
        add_series_base_stats_to_dict(to_process.compare, to_process.compare_counts, compare_dict)

    # Perform full analysis on source/compare/target
    if returned_feature_dict["type"] == FeatureType.TYPE_NUM:
        sweetviz.series_analyzer_numeric.analyze(to_process, returned_feature_dict)
    elif returned_feature_dict["type"] == FeatureType.TYPE_CAT:
        sweetviz.series_analyzer_cat.analyze(to_process, returned_feature_dict)
    elif returned_feature_dict["type"] == FeatureType.TYPE_BOOL:
        sweetviz.series_analyzer_cat.analyze(to_process, returned_feature_dict)
    elif returned_feature_dict["type"] == FeatureType.TYPE_TEXT:
        sweetviz.series_analyzer_text.analyze(to_process, returned_feature_dict)
    else:
        raise ValueError

    # print(f"{to_process.source.name} PROCESSED ------> "
    #       f" {time.perf_counter() - start}")

    return returned_feature_dict
