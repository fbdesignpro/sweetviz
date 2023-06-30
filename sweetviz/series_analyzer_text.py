import html
import sweetviz.sv_html as sv_html
from sweetviz.sv_types import NumWithPercent, FeatureToProcess


def do_detail_text(to_process: FeatureToProcess, updated_dict: dict):
    updated_dict["detail"] = dict()
    detail = updated_dict["detail"]

    # Compute COUNT stats (i.e. below graph)
    # ----------------------------------------------------------------------------------------------
    detail["full_count"] = []

    num_values = updated_dict["base_stats"]["num_values"].number
    if to_process.compare_counts is not None:
        num_values_compare = updated_dict["compare"]["base_stats"]["num_values"].number

    # Iterate through ALL VALUES and get stats
    for item in to_process.source_counts["value_counts_without_nan"].items():
        row = dict()
        row["name"] = html.escape(str(item[0]))
        row["count"] = NumWithPercent(item[1], num_values)
        # Defaults to no comparison or target
        row["count_compare"] = None
        row["target_stats"] = None
        row["target_stats_compare"] = None
        if to_process.compare_counts is not None:
            # HAS COMPARE...
            if row["name"] in to_process.compare_counts["value_counts_without_nan"].index:
                # ...and value exists in COMPARE
                matching = to_process.compare_counts["value_counts_without_nan"][row["name"]]
                row["count_compare"] = NumWithPercent(matching, num_values_compare)

        detail["full_count"].append(row)

    return


def analyze(to_process: FeatureToProcess, feature_dict: dict):
    compare_dict = feature_dict.get("compare")
    feature_dict["stats"] = dict()
    if compare_dict:
        compare_dict["stats"] = dict()

    do_detail_text(to_process, feature_dict)

    if to_process.is_target():
        raise ValueError
    else:
        feature_dict["html_summary"] = sv_html.generate_html_summary_text(feature_dict, compare_dict)
