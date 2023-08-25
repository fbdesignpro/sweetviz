import numpy as np
import pandas as pd
from sweetviz.graph_numeric import GraphNumeric
import sweetviz.sv_html as sv_html
from sweetviz.sv_types import NumWithPercent, FeatureType, FeatureToProcess
from sweetviz.config import config


def do_stats_numeric(series: pd.Series, updated_dict: dict):
    stats = updated_dict["stats"]
    stats["max"] = series.max()
    stats["mean"] = series.mean()
    for percentile, value in series.quantile([0.95, 0.75, 0.50, 0.25, 0.05]).to_dict().items():
        stats[f"perc{int(percentile*100)}"] = value
    stats["min"] = series.min()

    stats["range"] = stats["max"] - stats["min"]
    stats["iqr"] = stats["perc75"] - stats["perc25"]

    stats["std"] = series.std()
    stats["variance"] = series.var()
    stats["kurtosis"] = series.kurt()
    stats["skewness"] = series.skew()
    stats["sum"] = series.sum()
    # MAD was unused!!!
    # stats["mad"] = (series - series.mean()).abs().mean() # deprecated: series.mad()
    stats["cv"] = stats["std"] / stats["mean"] if stats["mean"] else np.NaN
    return updated_dict


def do_detail_numeric(series: pd.Series, counts: dict, counts_compare: dict, updated_dict: dict):
    updated_dict["detail"] = dict()
    detail = updated_dict["detail"]
    total_num = float(updated_dict["base_stats"]["num_values"])
    num_to_show = config["Detail_Stats"].getint("max_num_numeric_top_values")

    detail["frequent_values"] = list()
    detail["min_values"] = list()
    detail["max_values"] = list()
    frequent_values = pd.DataFrame(counts["value_counts_without_nan"].head(num_to_show))
    min_values = pd.DataFrame(counts["value_counts_without_nan"].sort_index( \
            ascending=True).head(num_to_show))
    max_values = pd.DataFrame(counts["value_counts_without_nan"].sort_index( \
            ascending=False)).head(num_to_show)

    if counts_compare is not None:
        this_compare_count = counts_compare["value_counts_without_nan"]
        compare_total_num = float(updated_dict["compare"]["base_stats"]["num_values"])
    else:
        this_compare_count = None
    for frequent, min_value, max_value in zip(frequent_values.itertuples(), \
                                              min_values.itertuples(), max_values.itertuples()):
        def get_comparison_num(feature_name):
            this_comparison = None
            if this_compare_count is not None:
                try:
                    this_comparison = this_compare_count.get(feature_name)
                except TypeError:
                    # Workaround for cases where source dataset has ints only, but compare has floats...
                    pass
                    #...this was incorrect as it could have created false matches:
                    # if this_compare_count.index.dtype.name.find('int') != -1:
                    #     this_comparison = this_compare_count.get(np.int64(feature_name))
                    # else:
                    #     this_comparison = None
                if this_comparison is not None:
                    this_comparison = NumWithPercent(this_comparison, compare_total_num)
                else:
                    # If there is a comparison array but no matching value, insert 0
                    # ("none" is the absence of value)
                    this_comparison = NumWithPercent(0, compare_total_num)
            return this_comparison
        detail["frequent_values"].append((frequent[0], NumWithPercent(frequent[1], total_num),
                                          get_comparison_num(frequent[0])))
        detail["min_values"].append((min_value[0], NumWithPercent(min_value[1], total_num),
                                     get_comparison_num(min_value[0])))
        detail["max_values"].append((max_value[0], NumWithPercent(max_value[1], total_num),
                                     get_comparison_num(max_value[0])))
        # detail["min_values"] = pd.DataFrame(counts["value_counts_without_nan"].sort_index( \
        #     ascending=True).tail(num_to_show))

# detail["frequent_values"] = pd.DataFrame(counts["value_counts_without_nan"].head(num_to_show))
    # detail["frequent_values"]["percent"] = detail["frequent_values"] / total_num * 100.0
    #
    # detail["min_values"] = pd.DataFrame(counts["value_counts_without_nan"].sort_index( \
    #     ascending=True).tail(num_to_show))
    # detail["min_values"]["percent"] = detail["min_values"] / total_num * 100.0
    #
    # detail["max_values"] = pd.DataFrame(counts["value_counts_without_nan"].sort_index( \
    #     ascending=False)).tail(num_to_show)
    # detail["max_values"]["percent"] = detail["max_values"] / total_num * 100.0


def analyze(to_process: FeatureToProcess, feature_dict: dict):
    do_stats_numeric(to_process.source, feature_dict)
    compare_dict = feature_dict.get("compare")
    if compare_dict:
        do_stats_numeric(to_process.compare, compare_dict)

    do_detail_numeric(to_process.source, to_process.source_counts, to_process.compare_counts, feature_dict)

    feature_dict["minigraph"] = GraphNumeric("mini", to_process)
    feature_dict["detail_graphs"] = list()
    for num_bins in [0, 5, 15, 30]:
        new_graph = GraphNumeric("detail-"+str(num_bins), to_process)
        if new_graph:
            feature_dict["detail_graphs"].append(new_graph)

    if to_process.is_target():
        feature_dict["html_summary"] = sv_html.generate_html_summary_target_numeric(feature_dict, compare_dict)
    else:
        feature_dict["html_summary"] = sv_html.generate_html_summary_numeric(feature_dict, compare_dict)