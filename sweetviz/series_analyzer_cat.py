from sweetviz.config import config
from sweetviz.sv_types import NumWithPercent, FeatureType, FeatureToProcess
from sweetviz.graph_cat import GraphCat
import sweetviz.sv_html as sv_html
import sweetviz.utils as utils
from sweetviz.sv_types import OTHERS_GROUPED


def do_detail_categorical(to_process: FeatureToProcess, updated_dict: dict):
    updated_dict["detail"] = dict()
    detail = updated_dict["detail"]

    # Compute COUNT stats (i.e. below graph)
    # ----------------------------------------------------------------------------------------------
    detail["full_count"] = []

    # To get percentages
    num_values = updated_dict["base_stats"]["num_values"].number
    if to_process.compare_counts is not None:
        num_values_compare = updated_dict["compare"]["base_stats"]["num_values"].number

    category_counts = utils.get_clamped_value_counts(to_process.source_counts["value_counts_without_nan"], \
                                   config["Graphs"].getint("detail_graph_max_categories"))

    # Iterate through ALL VALUES and get stats
    total_num_compare = 0
    max_abs_value = 0
    for item in category_counts.items():
        row = dict()
        row["name"] = item[0]
        row["count"] = NumWithPercent(item[1], num_values)
        # Defaults to no comparison or target
        row["count_compare"] = None
        row["target_stats"] = None
        row["target_stats_compare"] = None
        row["is_total"] = None

        if to_process.source_target is not None:
            # HAS TARGET
            # TODO: OPTIMIZE: CACHE FROM GRAPH?
            if row["name"] == OTHERS_GROUPED:
                this_value_target_only = to_process.source_target[
                    ~to_process.source.isin(category_counts.keys())]
            else:
                this_value_target_only = to_process.source_target[to_process.source == row["name"]]

            if to_process.predetermined_type_target == FeatureType.TYPE_BOOL:
                # If value is only present in compared
                if len(this_value_target_only) > 0:
                    count_this_value_target_only = float(this_value_target_only.count())
                    count_true = this_value_target_only.sum()
                    row["target_stats"] = NumWithPercent(count_true, count_this_value_target_only)
                else:
                    # None will be correctly interpreted by our display, not nan
                    row["target_stats"] = None
            elif to_process.predetermined_type_target == FeatureType.TYPE_NUM:
                # If value is only present in compared
                if len(this_value_target_only) > 0:
                    row["target_stats"] = NumWithPercent(this_value_target_only.mean(), 1.0)
                    max_abs_value = max(max_abs_value, row["target_stats"].number)
                else:
                    # None will be correctly interpreted by our display, not nan
                    row["target_stats"] = None

        if to_process.compare_counts is not None:
            # HAS COMPARE...
            if row["name"] in to_process.compare_counts["value_counts_without_nan"].index:
                # ...and value exists in COMPARE
                matching = to_process.compare_counts["value_counts_without_nan"][row["name"]]
                row["count_compare"] = NumWithPercent(matching, num_values_compare)

                if to_process.compare_target is not None:
                    # TODO: OPTIMIZE: CACHE FROM GRAPH?
                    if row["name"] == OTHERS_GROUPED:
                        this_value_target_only = to_process.compare_target[
                            ~to_process.compare.isin(category_counts.keys())]
                    else:
                        this_value_target_only = to_process.compare_target[to_process.compare == row["name"]]
                    # HAS COMPARE-TARGET
                    if to_process.predetermined_type_target == FeatureType.TYPE_BOOL:
                        if len(this_value_target_only) > 0:
                            count_this_value_target_only = float(this_value_target_only.count())
                            count_true = this_value_target_only.sum()
                            row["target_stats_compare"] = NumWithPercent(count_true,
                                                                         count_this_value_target_only)
                        else:
                            # None will be correctly interpreted by our display, not nan
                            row["target_stats_compare"] = None
                    elif to_process.predetermined_type_target == FeatureType.TYPE_NUM:
                        if len(this_value_target_only) > 0:
                            row["target_stats_compare"] = NumWithPercent(this_value_target_only.mean(), 1.0)
                            max_abs_value = max(max_abs_value, row["target_stats_compare"].number)
                        else:
                            # None will be correctly interpreted by our display, not nan
                            row["target_stats_compare"] = None

        detail["full_count"].append(row)
    detail["max_range"] = max_abs_value

    # "ALL" row
    # -----------------------------------------------
    row = dict()
    row["name"] = "ALL"
    row["count"] = NumWithPercent(num_values, num_values)
    # Defaults to no comparison or target
    row["count_compare"] = None
    row["target_stats"] = None
    row["target_stats_compare"] = None
    row["is_total"] = True

    if to_process.source_target is not None:
        # HAS TARGET
        if to_process.predetermined_type_target == FeatureType.TYPE_BOOL:
            # TODO: OPTIMIZE: CACHE FROM GRAPH?
            count_this_value_target_only = float(to_process.source_target.count())
            count_true = to_process.source_target.sum()
            row["target_stats"] = NumWithPercent(count_true, count_this_value_target_only)
        elif to_process.predetermined_type_target == FeatureType.TYPE_NUM:
            # TODO: OPTIMIZE: CACHE FROM GRAPH?
            row["target_stats"] = NumWithPercent(to_process.source_target.mean(), 1.0)

    if to_process.compare_counts is not None:
        row["count_compare"] = NumWithPercent(num_values_compare, num_values_compare)
        if to_process.compare_target is not None:
            # HAS COMPARE-TARGET
            if to_process.predetermined_type_target == FeatureType.TYPE_BOOL:
                # TODO: OPTIMIZE: CACHE FROM GRAPH?
                count_this_value_target_only = float(to_process.compare_target.count())
                count_true = to_process.compare_target.sum()
                row["target_stats_compare"] = NumWithPercent(count_true, count_this_value_target_only)
            elif to_process.predetermined_type_target == FeatureType.TYPE_NUM:
                # TODO: OPTIMIZE: CACHE FROM GRAPH?
                row["target_stats_compare"] = NumWithPercent(to_process.compare_target.mean(), 1.0)
    detail["full_count"].append(row)
    return

def analyze(to_process: FeatureToProcess, feature_dict: dict):
    compare_dict = feature_dict.get("compare")
    feature_dict["stats"] = dict()
    if compare_dict:
        compare_dict["stats"] = dict()

    do_detail_categorical(to_process, feature_dict)

    feature_dict["minigraph"] = GraphCat("mini", to_process)
    feature_dict["detail_graphs"] = list()
    feature_dict["detail_graphs"].append(GraphCat("detail", to_process))

    if to_process.is_target():
        feature_dict["html_summary"] = sv_html.generate_html_summary_target_cat(feature_dict, compare_dict)
    else:
        feature_dict["html_summary"] = sv_html.generate_html_summary_cat(feature_dict, compare_dict)

    return


