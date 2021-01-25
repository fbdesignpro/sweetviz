import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

from sweetviz import sv_math
from sweetviz import utils
from sweetviz.config import config
from sweetviz.sv_types import FeatureType, FeatureToProcess, OTHERS_GROUPED
import sweetviz.graph
from typing import List


def plot_grouped_bars(tick_names: List[str], data_lists: List[List], \
        colors: List[str], gap_percent: float, axis_obj = None, \
        orientation: str = 'vertical', **kwargs):
    if len(data_lists) > len(colors):
        raise ValueError
    num_data_lists = len(data_lists)
    locations_centered = np.arange(len(tick_names))

    usable_for_bars = 1.0 - (gap_percent / 100.0)
    bar_width = usable_for_bars / num_data_lists
    center_offset = (bar_width / 2.0) * (1 - num_data_lists % 2)
    tick_positions = locations_centered + usable_for_bars / 2.0
    category_starts = locations_centered + center_offset

    offset = 0.0
    for cur_height_list, cur_color in zip(data_lists, colors):
        if len(tick_names) != len(cur_height_list):
            raise ValueError
        if axis_obj:
            # AXIS object is already provided, use it
            if orientation == 'vertical':
                plt.xticks(locations_centered, tick_names)
                axis_obj.bar(category_starts + offset, cur_height_list, \
                             bar_width, color=cur_color, **kwargs)
            else:
                plt.yticks(locations_centered, tick_names)
                axis_obj.barh(category_starts + offset, cur_height_list, \
                             bar_width, color=cur_color, **kwargs)
        else:
            # AXIS object is not provided, use "plt."
            if orientation == 'vertical':
                plt.xticks(locations_centered, tick_names)
                plt.bar(category_starts + offset, cur_height_list, bar_width, \
                        color=cur_color, **kwargs)
            else:
                plt.yticks(locations_centered, tick_names)
                plt.barh(category_starts + offset, cur_height_list, bar_width, \
                        color=cur_color, **kwargs)
        offset = offset - bar_width
    # return category_starts + (bar_width / 2.0), bar_width
    return locations_centered, bar_width


class GraphCat(sweetviz.graph.Graph):
    def __init__(self, which_graph: str, to_process: FeatureToProcess):
        if to_process.is_target() and which_graph == "mini":
            styles = ["graph_base.mplstyle", "graph_target.mplstyle"]
        else:
            styles = ["graph_base.mplstyle"]
        self.set_style(styles)

        is_detail = which_graph.find("detail") != -1
        cycle_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']

        if which_graph == "mini":
            max_categories = config["Graphs"].getint("summary_graph_max_categories")
        elif is_detail:
            max_categories = config["Graphs"].getint("detail_graph_max_categories")
        else:
            raise ValueError
        plot_data_series = utils.get_clamped_value_counts( \
            to_process.source_counts["value_counts_without_nan"], max_categories)

        if which_graph == "mini":
            f, axs = plt.subplots(1, 1, \
                                  figsize=(config["Graphs"].getfloat("cat_summary_graph_width"),
                                           config["Graphs"].getfloat("summary_graph_height")))
            gap_percent = config["Graphs"].getfloat("summary_graph_categorical_gap")
            axs.tick_params(axis='x', direction='out', pad=0, labelsize=8, length=2)
            axs.tick_params(axis='y', direction='out', pad=2, labelsize=8, length=2)
            axs.xaxis.tick_top()
        elif is_detail:
            height = config["Graphs"].getfloat("detail_graph_height_base") \
                + config["Graphs"].getfloat("detail_graph_height_per_elem") * max(1, len(plot_data_series))
            if height > config["Graphs"].getfloat("detail_graph_categorical_max_height"):
                # Shrink height to fit, past a certain number
                height = config["Graphs"].getfloat("detail_graph_categorical_max_height")
            f, axs = plt.subplots(1, 1, \
                                  figsize=(config["Graphs"].getfloat("detail_graph_width"), height))
            gap_percent = config["Graphs"].getfloat("detail_graph_categorical_gap")
            axs.tick_params(axis='x', direction='out', pad=0, labelsize=8, length=2)
            axs.tick_params(axis='y', direction='out', pad=2, labelsize=8, length=2)
            axs.xaxis.tick_top()

        self.size_in_inches = f.get_size_inches()
        tick_names = list(plot_data_series.index)

        # To show percentages
        sum_source = sum(plot_data_series)
        plot_data_series = plot_data_series / sum_source if sum_source != 0.0 else plot_data_series * 0.0
        axs.xaxis.set_major_formatter(mtick.PercentFormatter(xmax=1.0, decimals=0))

        # MAIN DATA (renders "under" target plots)
        # -----------------------------------------------------------
        if to_process.compare is not None:
            # COMPARE
            matched_data_series = utils.get_matched_value_counts( \
                to_process.compare_counts["value_counts_without_nan"],plot_data_series)
            # Show percentages
            sum_compared = sum(matched_data_series)
            matched_data_series = matched_data_series / sum_compared if sum_compared != 0.0 else \
                matched_data_series * 0.0

            height_lists = [list(plot_data_series.values), list(matched_data_series)]
        else:
            height_lists = [list(plot_data_series.values)]

        # Reorder so it plots with max values on top, "Others" at bottom
        # Plot: index 0 at BOTTOM
        # Need to change TICK NAMES and all elements in height_lists
        # ---------------------------------------------
        reversed_height_lists = list()
        for height_list in height_lists:
            reversed_height_lists.append(list(reversed(height_list)))
        tick_names = list(reversed(tick_names))
        height_lists = reversed_height_lists

        try:
            others_index = tick_names.index(OTHERS_GROUPED)
            tick_names.insert(0, tick_names.pop(others_index))
            for height_list in height_lists:
                height_list.insert(0, height_list.pop(others_index))
        except:
            pass


        # Escape LaTeX
        tick_names_for_labels_only = tick_names
        if len(tick_names):
            if type(tick_names[0]) == str:
                tick_names_for_labels_only = [str(x).replace("$",r"\$") for x in tick_names]
        # colors = ("r", "b")
        category_centers, bar_width = \
            plot_grouped_bars(tick_names_for_labels_only, height_lists, cycle_colors, gap_percent,
                              orientation = 'horizontal', axis_obj = axs)

        # TARGET
        # -----------------------------------------------------------
        if to_process.source_target is not None:
            if to_process.predetermined_type_target == FeatureType.TYPE_NUM:
                # TARGET: IS NUMERIC
                target_values_source = list()
                names_excluding_others = [key for key in tick_names if key != OTHERS_GROUPED]
                for name in tick_names:
                    if name == OTHERS_GROUPED:
                        tick_average = to_process.source_target[ \
                            ~to_process.source.isin(names_excluding_others)].mean()
                    else:
                        tick_average = to_process.source_target[ \
                            to_process.source == name].mean()
                    target_values_source.append(tick_average)
                ax2 = axs.twiny()
                ax2.xaxis.set_major_formatter(mtick.FuncFormatter(self.format_smart))
                ax2.xaxis.tick_bottom()
                # Need to redo this for some reason after twinning:
                axs.xaxis.tick_top()
                ax2.tick_params(axis='x', direction='out', pad=2, labelsize=8, length=2)
                ax2.plot(target_values_source, category_centers,
                         marker='o', color=sweetviz.graph.COLOR_TARGET_SOURCE)

                if to_process.compare is not None and \
                        to_process.compare_target is not None:
                    # TARGET NUMERIC: with compare TARGET
                    target_values_compare = list()
                    for name in tick_names:
                        if name == OTHERS_GROUPED:
                            tick_average = to_process.compare_target[ \
                                ~to_process.compare.isin(names_excluding_others)].mean()
                        else:
                            tick_average = to_process.compare_target[ \
                                to_process.compare == name].mean()
                        target_values_compare.append(tick_average)
                    ax2.plot(target_values_compare,
                             category_centers, marker='o', color=sweetviz.graph.COLOR_TARGET_COMPARE)

            elif to_process.predetermined_type_target == FeatureType.TYPE_BOOL:
                # TARGET: IS BOOL
                # ------------------------------------
                target_values_source = list()
                names_excluding_others = [key for key in tick_names if key != OTHERS_GROUPED]
                for name in tick_names:
                    if name == OTHERS_GROUPED:
                        tick_num = sv_math.count_fraction_of_true(to_process.source_target[ \
                            ~to_process.source.isin(names_excluding_others)])[0]
                    else:
                        tick_num = sv_math.count_fraction_of_true(to_process.source_target[ \
                            to_process.source == name])[0]
                    target_values_source.append(tick_num)
                    # target_values_source.append(tick_num * plot_data_series[name])

                # ax2 = axs.twiny()
                # ax2.xaxis.set_major_formatter(mtick.FuncFormatter(self.format_smart))
                # ax2.xaxis.tick_bottom()
                # # Need to redo this for some reason after twinning:
                # axs.xaxis.tick_top()
                # ax2.tick_params(axis='x', direction='out', pad=2, labelsize=8, length=2)
                axs.plot(target_values_source, category_centers,
                         marker='o', color=sweetviz.graph.COLOR_TARGET_SOURCE)

                target_values_compare = list()
                if to_process.compare is not None and \
                        to_process.compare_target is not None:
                    # TARGET BOOL: with compare TARGET
                    for name in tick_names:
                        if name == OTHERS_GROUPED:
                            tick_num = sv_math.count_fraction_of_true(to_process.compare_target[ \
                                ~to_process.compare.isin(names_excluding_others)])[0]
                        else:
                            tick_num = sv_math.count_fraction_of_true(to_process.compare_target[ \
                                to_process.compare == name])[0]
                        target_values_compare.append(tick_num)
                        # target_values_compare.append(tick_num * matched_data_series[name])
                    axs.plot(target_values_compare, category_centers,
                             marker='o', color=sweetviz.graph.COLOR_TARGET_COMPARE)
                # else:
                #     # TARGET BOOL: NO compare TARGET -> Just fill with zeros so alignment is still good
                #     for name in tick_names:
                #         target_values_compare.append(0.0)
                # target_plot_series = [target_values_source, target_values_compare]
                # plot_grouped_bars(tick_names, target_plot_series, ('k','k'), gap_percent,
                #                   orientation='horizontal', axis_obj=axs, alpha=0.6)

        # Finalize Graph
        # -----------------------------
        # Needs only ~5 on right, but want to match num
        if which_graph == "mini":
            needed_pixels_padding = np.array([14.0, (300 + 32), 14, 45]) # TOP-LEFT-BOTTOM-RIGHT
        else:
            needed_pixels_padding = np.array([14.0, 140, 16, 45])  # TOP-LEFT-BOTTOM-RIGHT

        padding_fraction = needed_pixels_padding
        padding_fraction[0] = padding_fraction[0] / (self.size_in_inches[1] * f.dpi)
        padding_fraction[2] = padding_fraction[2] / (self.size_in_inches[1] * f.dpi)
        padding_fraction[3] = padding_fraction[3] / (self.size_in_inches[0] * f.dpi)
        padding_fraction[1] = padding_fraction[1] / (self.size_in_inches[0] * f.dpi)
        plt.subplots_adjust(top=(1.0 - padding_fraction[0]), left=padding_fraction[1], \
                bottom=padding_fraction[2], right=(1.0 - padding_fraction[3]))

        self.graph_base64 = self.get_encoded_base64(f)
        plt.close('all')
