import numpy as np
import html
from operator import itemgetter
from jinja2 import Environment, PackageLoader
import sweetviz.sv_html_formatters
from sweetviz.config import config
from sweetviz.sv_types import NumWithPercent, FeatureType, OTHERS_GROUPED
from sweetviz.graph_associations import CORRELATION_ERROR
from sweetviz.graph_associations import CORRELATION_IDENTICAL
from functools import cmp_to_key

package_loader = PackageLoader("sweetviz", "templates")
jinja2_env = Environment(lstrip_blocks = True,
                         trim_blocks = True,
                         loader = package_loader)
jinja2_env.filters["fmt_int_commas"] = sweetviz.sv_html_formatters.fmt_int_commas
jinja2_env.filters["fmt_int_limit"] = sweetviz.sv_html_formatters.fmt_int_limit
jinja2_env.filters["fmt_assoc"] = sweetviz.sv_html_formatters.fmt_assoc
jinja2_env.filters["fmt_percent_parentheses"] = sweetviz.sv_html_formatters.fmt_percent_parentheses
jinja2_env.filters["fmt_percent"] = sweetviz.sv_html_formatters.fmt_percent
jinja2_env.filters["fmt_percent1d"] = sweetviz.sv_html_formatters.fmt_percent1d
jinja2_env.filters["fmt_smart"] = sweetviz.sv_html_formatters.fmt_smart
jinja2_env.filters["fmt_RAM"] = sweetviz.sv_html_formatters.fmt_RAM
jinja2_env.filters["fmt_smart_range"] = sweetviz.sv_html_formatters.fmt_smart_range
jinja2_env.filters["fmt_div_icon_missing"] = sweetviz.sv_html_formatters.fmt_div_icon_missing
jinja2_env.filters["fmt_div_color_override_missing"] = sweetviz.sv_html_formatters.fmt_div_color_override_missing
jinja2_env.globals["hello"] = "Superduper"

def load_layout_globals_from_config():
    jinja2_env.globals["FeatureType"] = FeatureType

    layout_globals = dict()
    general_globals = dict()
    for element in config["Layout"]:
        layout_globals[element] = config["Layout"].getint(element)
    general_globals['use_cjk_font'] = config["General"].getint("use_cjk_font")
    general_globals['association_min_to_bold'] = config["General"].getfloat("association_min_to_bold")
    jinja2_env.globals["layout"] = layout_globals
    jinja2_env.globals["general"] = general_globals


def set_summary_positions(dataframe_report):
    if dataframe_report._target is not None:
        dataframe_report._target["summary_pos"] = 0.0
    for feature in dataframe_report._features.values():
        render_index = feature["order_index"] if dataframe_report._target is None else \
            (feature["order_index"] + 1)
        feature["summary_pos"] = render_index * config["Layout"].getint("summary_spacing")
        feature["summary_pos"] = 0.0


def generate_html_detail(dataframe_report):
    # Need to generate final data for numeric and categorical
    all_detail = list(dataframe_report._features.values())
    if dataframe_report._target is not None:
        all_detail.append(dataframe_report._target)

    for feature in (all_detail):
        compare_dict = feature.get("compare")
        if feature["type"] == FeatureType.TYPE_CAT or \
                feature["type"] == FeatureType.TYPE_BOOL:
            feature["html_detail"] = generate_html_detail_cat(feature, compare_dict, dataframe_report)
        elif feature["type"] == FeatureType.TYPE_NUM:
            feature["html_detail"] = generate_html_detail_numeric(feature, compare_dict, dataframe_report)
        elif feature["type"] == FeatureType.TYPE_TEXT:
            feature["html_detail"] = generate_html_detail_text(feature, compare_dict, dataframe_report)


def generate_html_dataframe_page(dataframe_report):
    template = jinja2_env.get_template('dataframe_page.html')
    # Add in total page size (160 is hardcoded from the top of page-all-summaries in CSS)
    # This could be programmatically set
    dataframe_report.page_height = 160 + (dataframe_report.num_summaries * (config["Layout"].getint("summary_height_per_element")))
    if dataframe_report.page_layout == "widescreen":
        padding_type = "full_page_padding_widescreen"
    else:
        padding_type = "full_page_padding_vertical"
    padding = config["Layout"].getint(padding_type)
    dataframe_report.page_height += padding
    # scaling = dict()
    # scaling["main_column"] = scale
    # scaling= scale
    output = template.render(dataframe=dataframe_report, version=sweetviz.__version__)
    return output


def generate_html_dataframe_summary(dataframe_report):
    template = jinja2_env.get_template('dataframe_summary.html')
    output = template.render(dataframe=dataframe_report)
    return output

def generate_html_associations(dataframe_report, which):
    template = jinja2_env.get_template('dataframe_associations.html')
    output = template.render(dataframe=dataframe_report, which=which)
    return output

# SUMMARIES
# ----------------------------------------------------------------------------------------------
def create_summary_numeric_group_data(feature_dict: dict, compare_dict: dict):
    stats = feature_dict["stats"]
    def get_compare(stat_name):
        if compare_dict is not None:
            return compare_dict["stats"][stat_name]
        return 0

    group_1 = list()
    group_1.append({'name':'MAX', 'value':stats["max"], 'compare_value':get_compare('max')})
    group_1.append({'name':'95%', 'value':stats["perc95"], 'compare_value':get_compare('perc95')})
    group_1.append({'name':'Q3', 'value':stats["perc75"], 'compare_value':get_compare('perc75')})
    if stats["mean"] > stats["perc50"]:
        group_1.append({'name':'AVG', 'value':stats["mean"], 'compare_value':get_compare('mean')})
        group_1.append({'name':'MEDIAN', 'value':stats["perc50"], 'compare_value':get_compare('perc50')})
    else:
        group_1.append({'name': 'MEDIAN', 'value': stats["perc50"], 'compare_value': get_compare('perc50')})
        group_1.append({'name': 'AVG', 'value': stats["mean"], 'compare_value': get_compare('mean')})
    group_1.append({'name':'Q1', 'value':stats["perc25"], 'compare_value':get_compare('perc25')})
    group_1.append({'name':'5%', 'value':stats["perc5"], 'compare_value':get_compare('perc5')})
    group_1.append({'name':'MIN', 'value':stats["min"], 'compare_value':get_compare('min')})

    group_2 = list()
    group_2.append({'name':'RANGE', 'value':stats["range"], 'compare_value':get_compare('range')})
    group_2.append({'name':'IQR', 'value':stats["iqr"], 'compare_value':get_compare('iqr')})
    group_2.append({'name':'STD', 'value':stats["std"], 'compare_value':get_compare('std')})
    group_2.append({'name':'VAR', 'value':stats["variance"], 'compare_value':get_compare('variance')})
    group_2.append({'name':'', 'value':"", 'compare_value':""})
    group_2.append({'name':'KURT.', 'value':stats["kurtosis"], 'compare_value':get_compare('kurtosis')})
    group_2.append({'name':'SKEW', 'value':stats["skewness"], 'compare_value':get_compare('skewness')})
    group_2.append({'name':'SUM', 'value':stats["sum"], 'compare_value':get_compare('sum')})
    return group_1, group_2

def generate_html_summary_numeric(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_summary_numeric.html')
    group_1, group_2 = create_summary_numeric_group_data(feature_dict, compare_dict)

    # Edge case fix for if there is only data in the compare
    if compare_dict is not None:
        if np.isnan(feature_dict["stats"]["range"]) and \
             np.isnan(compare_dict["stats"]["range"]) == False:
            feature_dict["stats"]["range"] = compare_dict["stats"]["range"]

    # NEW: Move numbers if there is not enough room
    def formatted_range(val):
        if isinstance(val, str):
            return ""
        return sweetviz.sv_html_formatters.fmt_smart_range(val, feature_dict["stats"]["range"])
    longest = max([len(formatted_range(x["value"])) for x in group_1])
    if longest > 7:
        group_1_width_suffix = "-wide"
    else:
        group_1_width_suffix = ""

    def formatted(val):
        if isinstance(val, str):
            return ""
        return sweetviz.sv_html_formatters.fmt_smart(val)
    longest = max([len(formatted(x["value"])) for x in group_2])
    if longest > 7:
        group_2_width_suffix = "-wide"
    else:
        group_2_width_suffix = ""

    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict,
                             group_1=group_1, group_2=group_2,
                             group_1_width_suffix=group_1_width_suffix,
                             group_2_width_suffix=group_2_width_suffix
                             )
    return output

def generate_html_summary_cat(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_summary_cat.html')
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict)
    return output


def generate_html_summary_text(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_summary_text.html')

    # Set some parameters for breakdown columns
    # ------------------------------------
    cols = dict()
    # Cols: Move text if there is a comparison pair display
    cur_x = config["Layout"].getint("pair_spacing")
    padding =config["Layout"].getint("col_spacing")
    if compare_dict is not None:
        cols["compare"] = cur_x
        cur_x = cur_x + config["Layout"].getint("pair_spacing")
    cur_x = cur_x + padding
    cols["text"] = cur_x
    cols["text_width"] = config["Layout"].getint("summary_text_max_width") - cur_x
    cols["full_text_width"] = config["Layout"].getint("summary_text_max_width")

    max_text_rows = config["Summary_Stats"].getint("summary_max_text_rows")

    # Filter final row list to display, add "other"
    # ------------------------------------
    full_list = feature_dict["detail"]["full_count"]
    feature_dict["detail"]["summary_count"] = full_list[:max_text_rows]
    summary_list = feature_dict["detail"]["summary_count"]

    # Clipping text only for memory purposes (display will be handled by the browser)
    max_text_display_length = config["Summary_Stats"].getint("text_max_string_len")
    for elem in summary_list:
        elem["name"] = elem["name"][:max_text_display_length]

    if len(summary_list) == max_text_rows:
        total = feature_dict["base_stats"]["num_values"].number
        cur_count = sum(row_data["count"].number for row_data in summary_list)
        other = total - cur_count
        row = dict()
        row["name"] = OTHERS_GROUPED.strip()
        row["count"] = NumWithPercent(other, total)
        row["target_stats"] = None
        row["target_stats_compare"] = None
        if compare_dict is not None:
            total = compare_dict["base_stats"]["num_values"].number
            cur_count = sum( \
                (row_data["count_compare"].number if row_data.get("count_compare") else 0) \
                for row_data in summary_list)
            other = total - cur_count
            row["count_compare"] = NumWithPercent(other, total)
        else:
            row["count_compare"] = None
        if row["count"].number > 0 or (row.get("count_compare") and row.get("count_compare").number > 0):
            summary_list.append(row)

    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict, \
                             cols=cols)
    return output


# Target versions of summaries
def generate_html_summary_target_numeric(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_summary_target_numeric.html')
    group_1, group_2 = create_summary_numeric_group_data(feature_dict, compare_dict)
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict, \
                             group_1=group_1, group_2=group_2)
    return output


def generate_html_summary_target_cat(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_summary_target_cat.html')
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict)
    return output


# DETAILS
# ----------------------------------------------------------------------------------------------
# negative value (< 0) when the left item should be sorted before the right item
def cmp_assoc_values(item1, item2):
    if item1[1] == CORRELATION_ERROR or item1[1] == CORRELATION_IDENTICAL:
        return -1
    if item2[1] == CORRELATION_ERROR or item2[1] == CORRELATION_IDENTICAL:
        return 1
    return abs(item1[1]) - abs(item2[1])

def add_is_target_or_not(association_list, target_name):
    returned = list()
    for it in association_list:
        if it[0] == target_name:
            returned.append([it[0], it[1], True])
        else:
            returned.append([it[0], it[1], False])
    return returned

def generate_html_detail_numeric(feature_dict: dict, compare_dict: dict, dataframe_report):
    template = jinja2_env.get_template('feature_detail_numeric.html')

    # Set some parameters for detail columns
    # ------------------------------------
    # Vertical
    spacing = config["Layout"].getint("cat_detail_col_spacing")
    cols = dict()
    detail_layout = dict()
    detail_layout["graph_y"] = config["Layout"].getint("cat_detail_graph_y")
    # detail_layout["breakdown_y"] = detail_layout["graph_y"] \
    #                                + feature_dict["detail_graphs"][0].size_in_inches[1] * 100 \
    #                                + config["Layout"].getint("cat_detail_breakdown_y_offset")
    # detail_layout["breakdown_height"] = 900 - detail_layout["breakdown_y"]

    # Set up ASSOCIATION data
    # ------------------------------------
    feature_name = feature_dict["name"]
    if dataframe_report._associations is not None:
        numerical = dataframe_report._associations[feature_name]
        # Filter by datatype NUMERICAL
        numerical = {k: v for k, v in numerical.items() \
                       if dataframe_report.get_type(k) == FeatureType.TYPE_NUM and k != feature_name}

        categorical = dataframe_report._associations[feature_name]
        # Filter by datatype CATEGORICAL
        categorical = {k: v for k, v in categorical.items() \
                      if dataframe_report.get_type(k) == FeatureType.TYPE_BOOL or
                      dataframe_report.get_type(k) == FeatureType.TYPE_CAT}

        # Sort & get top
        max_num = config["Detail_Stats"].getint("max_num_top_associations")
        numerical = sorted(numerical.items(), key=cmp_to_key(cmp_assoc_values), reverse=True)[:max_num]
        categorical = sorted(categorical.items(), key=itemgetter(1), reverse=True)[:max_num]

        # Set who's the target, for highlighting
        if dataframe_report._target is not None:
            numerical = add_is_target_or_not(numerical, dataframe_report._target["name"])
            categorical = add_is_target_or_not(categorical, dataframe_report._target["name"])
    else:
        max_num = None
        numerical = None
        categorical = None

    output = template.render(feature_dict=feature_dict, compare_dict=compare_dict, \
                             dataframe=dataframe_report, cols=cols, detail_layout=detail_layout, \
                             numerical=numerical, categorical=categorical)
    return output


def generate_html_detail_cat(feature_dict: dict, compare_dict: dict, dataframe_report):
    template = jinja2_env.get_template('feature_detail_cat.html')

    # Set some parameters for detail breakdown
    # ------------------------------------------
    # Vertical
    spacing = config["Layout"].getint("cat_detail_col_spacing")
    cols = dict()
    detail_layout = dict()
    detail_layout["graph_y"] = config["Layout"].getint("cat_detail_graph_y")
    detail_layout["breakdown_y"] = detail_layout["graph_y"] \
                                + feature_dict["detail_graphs"][0].size_in_inches[1] * 100 \
                                + config["Layout"].getint("cat_detail_breakdown_y_offset")
    detail_layout["breakdown_height"] = 910 - detail_layout["breakdown_y"]

    if dataframe_report.get_target_type() == FeatureType.TYPE_NUM:
        # Need 2 lines for the breakdown header area
        detail_layout["breakdown_header_class"] = "breakdown-row-header-2-lines"
        detail_layout["breakdown_hr_class"] = "breakdown-hr-2-lines"
    else:
        detail_layout["breakdown_header_class"] = "breakdown-row-header"
        detail_layout["breakdown_hr_class"] = "breakdown-hr"

    # Column Layout
    # ------------------------
    # Find name width
    count_row_data = feature_dict["detail"]["full_count"]
    longest_cat = max(map(lambda row : len(str(row['name'])), count_row_data))
    longest_width = longest_cat * config["Layout"].getint("character_width_estimate")
    # Set columns
    #cur_x = config["Layout"].getint("cat_detail_col_1_x")
    # 230px->48 = 4.8
    # 37px->6 = 6.2
    # 216px->44 = 4.9
    cur_x = longest_width + config["Layout"].getint("cat_detail_col_x_padding_after_name")
    cur_x = min(cur_x, config["Layout"].getint("cat_detail_col_1_max_x"))

    cols["name_max_len"] = cur_x
    cols["source"] = cur_x
    cur_x = cur_x + spacing
    if compare_dict is not None:
        cols["compare"] = cur_x
        cur_x = cur_x + spacing
    if dataframe_report.get_target_type() is not None:
        cur_x = cur_x + config["Layout"].getint("cat_detail_col_target_extra_spacing")
        cols["source_target"] = cur_x
        cur_x = cur_x + spacing
        if "compare" in dataframe_report._target:
            cols["compare_target"] = cur_x
            cur_x = cur_x + spacing

    max_rows = config["Detail_Stats"].getint("max_num_breakdown_categories")
    feature_dict["detail"]["detail_count"] = feature_dict["detail"]["full_count"][:max_rows]

    # Set up ASSOCIATION data
    # ------------------------------------
    feature_name = feature_dict["name"]
    if dataframe_report._associations is not None:
        # Filter by datatype CATEGORICAL
        influencing = dataframe_report._associations[feature_name]
        influencing = { k: v for k, v in influencing.items() \
                        if (dataframe_report.get_type(k) == FeatureType.TYPE_BOOL or
                            dataframe_report.get_type(k) == FeatureType.TYPE_CAT) and
                            k != feature_name }

        # Filter by datatype CATEGORICAL
        influenced = dataframe_report.get_what_influences_me(feature_name)
        influenced = { k: v for k, v in influenced.items() \
                        if (dataframe_report.get_type(k) == FeatureType.TYPE_BOOL or
                            dataframe_report.get_type(k) == FeatureType.TYPE_CAT) and
                            k != feature_name }

        # NUM-CAT
        corr_ratio = dataframe_report._associations[feature_name]
        corr_ratio = { k: v for k, v in corr_ratio.items() \
                        if dataframe_report.get_type(k) == FeatureType.TYPE_NUM and
                            k != feature_name }

        # Sort & get top
        max_num = config["Detail_Stats"].getint("max_num_top_associations")
        influencing = sorted(influencing.items(), key=itemgetter(1), reverse=True)[:max_num]
        influenced = sorted(influenced.items(), key=itemgetter(1), reverse=True)[:max_num]
        corr_ratio = sorted(corr_ratio.items(), key=itemgetter(1), reverse=True)[:max_num]

        # Set who's the target, for highlighting
        if dataframe_report._target is not None:
            influencing = add_is_target_or_not(influencing, dataframe_report._target["name"])
            influenced = add_is_target_or_not(influenced, dataframe_report._target["name"])
            corr_ratio = add_is_target_or_not(corr_ratio, dataframe_report._target["name"])
    else:
        influencing = None
        influenced = None
        corr_ratio = None
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict, \
                             dataframe = dataframe_report, cols=cols, detail_layout=detail_layout,
                             influencing=influencing, influenced=influenced, corr_ratio=corr_ratio)
    return output


def generate_html_detail_text(feature_dict: dict, compare_dict: dict, dataframe_report):
    template = jinja2_env.get_template('feature_detail_text.html')

    # Set some parameters for detail columns
    # ------------------------------------
    cols = dict()
    # Cols: Move text if there is a comparison pair display
    cur_x = config["Layout"].getint("pair_spacing")
    padding =config["Layout"].getint("col_spacing")
    if compare_dict is not None:
        cols["compare"] = cur_x
        cur_x = cur_x + config["Layout"].getint("pair_spacing")
    cur_x = cur_x + padding
    cols["text"] = cur_x
    cols["text_width"] = config["Layout"].getint("detail_text_max_width") - cur_x
    cols["full_text_width"] = config["Layout"].getint("detail_text_max_width")

    max_text_rows = config["Detail_Stats"].getint("detail_max_text_rows")

    # Filter final row list to display, add "other"
    # ------------------------------------
    full_list = feature_dict["detail"]["full_count"]
    feature_dict["detail"]["detail_count"] = full_list[:max_text_rows]
    detail_list = feature_dict["detail"]["detail_count"]

    # Clipping text only for memory purposes (display will be handled by the browser)
    max_text_display_length = config["Summary_Stats"].getint("text_max_string_len")
    for elem in detail_list:
        elem["name"] = elem["name"][:max_text_display_length]

    # Add "others"
    if len(detail_list) == max_text_rows:
        total = feature_dict["base_stats"]["num_values"].number
        cur_count = sum(row_data["count"].number for row_data in detail_list)
        other = total - cur_count
        row = dict()
        row["name"] = OTHERS_GROUPED.strip()
        row["count"] = NumWithPercent(other, total)
        row["target_stats"] = None
        row["target_stats_compare"] = None
        if compare_dict is not None:
            total = compare_dict["base_stats"]["num_values"].number
            cur_count = sum( \
                (row_data["count_compare"].number if row_data.get("count_compare") else 0) \
                for row_data in detail_list)
            other = total - cur_count
            row["count_compare"] = NumWithPercent(other, total)
        else:
            row["count_compare"] = None
        if row["count"].number > 0 or (row.get("count_compare") and row.get("count_compare").number > 0):
            detail_list.append(row)

    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict, \
                             dataframe = dataframe_report, cols=cols)
    return output


#UNUSED yet:
#UNUSED yet:
#UNUSED yet:
def generate_html_detail_target_numeric(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_detail_numeric.html')
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict)
    return output


# UNUSED yet:
# UNUSED yet:
# UNUSED yet:
def generate_html_detail_target_cat(feature_dict: dict, compare_dict: dict):
    template = jinja2_env.get_template('feature_detail_cat.html')
    output = template.render(feature_dict = feature_dict, compare_dict = compare_dict)
    return output
