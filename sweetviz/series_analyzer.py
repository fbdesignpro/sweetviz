import pandas as pd
from sweetviz.sv_types import NumWithPercent, FeatureType, FeatureToProcess
from sweetviz.type_detection import determine_feature_type
import sweetviz.series_analyzer_numeric
import sweetviz.series_analyzer_cat
import sweetviz.series_analyzer_text


def get_counts(series: pd.Series) -> dict:
    # The value_counts() function is used to get a Series containing counts of unique values.
    value_counts_with_nan = series.value_counts(dropna=False)
    value_counts_without_nan = (
        value_counts_with_nan.reset_index().dropna().set_index("index").iloc[:, 0]
    )
    distinct_count_with_nan = value_counts_with_nan.count()
    distinct_count_without_nan = value_counts_without_nan.count()

    # Convert  indices to strings (helps with referencing later)
    # value_counts_without_nan.index = value_counts_without_nan.index.map(str)

    return {
        # "value_counts": value_counts_without_nan,  # Alias
        "value_counts_with_nan": value_counts_with_nan,
        "value_counts_without_nan": value_counts_without_nan,
        "distinct_count_with_nan": distinct_count_with_nan,
        "distinct_count_without_nan": distinct_count_without_nan,
        "num_rows_with_data": series.count(),
        "num_rows_total": len(series),
    }


def fill_out_missing_counts_in_other_series(my_counts:dict, other_counts:dict):
    to_fill_list = ["value_counts_with_nan", "value_counts_without_nan"]
    for to_fill in to_fill_list:
        for key, value in other_counts[to_fill].items():
            if key not in my_counts[to_fill]:
                my_counts[to_fill].at[key] = 0

def add_series_base_stats_to_dict(series: pd.Series, counts: dict, updated_dict: dict) -> dict:
    updated_dict["stats"] = dict()
    updated_dict["base_stats"] = dict()
    base_stats = updated_dict["base_stats"]
    num_total = counts["num_rows_total"]
    try:
        num_zeros = series[series == 0].sum()
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

    # Determine COMPARED feature type & initialize
    compare_dict = None
    if to_process.compare is not None:
        to_process.compare_counts = get_counts(to_process.compare)
        compare_type = determine_feature_type(to_process.compare,
                                              to_process.compare_counts,
                                              returned_feature_dict["type"], "COMPARED")
        # Explicitly show missing categories on each set
        if compare_type == FeatureType.TYPE_CAT or compare_type == FeatureType.TYPE_BOOL:
            fill_out_missing_counts_in_other_series(to_process.compare_counts, to_process.source_counts)
            fill_out_missing_counts_in_other_series(to_process.source_counts, to_process.compare_counts)
        returned_feature_dict["compare"] = dict()
        compare_dict = returned_feature_dict["compare"]
        compare_dict["type"] = compare_type

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
