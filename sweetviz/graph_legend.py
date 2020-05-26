import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.patches as patches

from sweetviz.config import config
from sweetviz import sv_html_formatters
from sweetviz.sv_types import FeatureType, FeatureToProcess
import sweetviz.graph
from matplotlib.ticker import PercentFormatter

class GraphLegend(sweetviz.graph.Graph):
    def __init__(self, dataframe_report):
        styles = ["graph_base.mplstyle"]
        self.set_style(styles)

        fig = plt.figure(
            figsize=(config["Graphs"].getfloat("legend_width"), config["Graphs"].getfloat("legend_height")))
        axs = fig.add_axes([0, 0, 1, 1])
        axs.axis('off')
        scale = axs.transAxes.transform((1,1))
        scale = [ 1.0 / x for x in scale ]
        def to_fractions(pos_in_pix):
            return (pos_in_pix[0] * scale[0], pos_in_pix[1] * scale[1])

        def to_fractionsxy(x, y):
            return (x * scale[0], y * scale[1])

        def to_fraction_seq(seq, scalar):
            return [x * scalar for x in seq]

        cycle_colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
        label_color = plt.rcParams['axes.labelcolor']

        gfx_x_source = 225
        gfx_x_compare = 350
        gfx_bar_y = 14
        gfx_line_y = 5
        bar_size = np.array([25,6])
        bar_text_offset = np.array([6,0])
        line_text_offset = np.array([0,-3])

        axs.add_patch(patches.Rectangle(to_fractionsxy(gfx_x_source, gfx_bar_y), bar_size[0] * scale[0], bar_size[1] * scale[1], facecolor=cycle_colors[0]))
        text1 = np.array([gfx_x_source,gfx_bar_y]) - bar_text_offset
        text1[1] += 1
        text1_elem = plt.text(text1[0] * scale[0], text1[1] * scale[1], "" + dataframe_report.source_name, fontsize=8, color=cycle_colors[0],
                              ha='right')

        # COMPARE value
        if dataframe_report.compare_name:
            axs.add_patch(
                patches.Rectangle(to_fractionsxy(gfx_x_compare, gfx_bar_y), bar_size[0] * scale[0], bar_size[1] * scale[1],
                                  facecolor=cycle_colors[1]))
            text2 = np.array([gfx_x_compare, gfx_bar_y]) + bar_text_offset
            text2[0] += bar_size[0]
            text2_elem = plt.text(text2[0] * scale[0], text2[1] * scale[1],
                                  "" + dataframe_report.compare_name, fontsize=8, color=cycle_colors[1])

        # TARGETS
        if dataframe_report.get_target_type() is not None:
            axs.add_line(
                matplotlib.lines.Line2D(to_fraction_seq([gfx_x_source, gfx_x_source + bar_size[0]], scale[0]),
                                        to_fraction_seq([gfx_line_y, gfx_line_y], scale[1]), lw=(1),
                                        color=sweetviz.graph.COLOR_TARGET_SOURCE, marker='o' ))
            text1[1] = gfx_line_y
            text1 += line_text_offset
            if dataframe_report.get_target_type() == FeatureType.TYPE_NUM:
                text_content = "Avg. " + dataframe_report._target["name"]
            else:
                text_content = "% " + dataframe_report._target["name"]
            text1_elem = plt.text(text1[0] * scale[0], text1[1] * scale[1], text_content, fontsize=8, color=sweetviz.graph.COLOR_TARGET_SOURCE,
                                  ha='right')

            if dataframe_report.compare_name and dataframe_report._target.get("compare"):
                axs.add_line(
                    matplotlib.lines.Line2D(
                        to_fraction_seq([gfx_x_compare, gfx_x_compare + bar_size[0]], scale[0]),
                        to_fraction_seq([gfx_line_y, gfx_line_y], scale[1]), lw=(1),
                        color=sweetviz.graph.COLOR_TARGET_COMPARE, marker='o'))

                text2[1] = gfx_line_y
                text2 += line_text_offset
                if dataframe_report.get_target_type() == FeatureType.TYPE_NUM:
                    text_content = "Avg. " + dataframe_report._target["name"]
                    #+ f" ({dataframe_report.compare_name})"
                else:
                    text_content = "% " + dataframe_report._target["name"]
                    #+ f" ({dataframe_report.compare_name})"
                text2_elem = plt.text(text2[0] * scale[0], text2[1] * scale[1], text_content, fontsize=8, color=sweetviz.graph.COLOR_TARGET_COMPARE)

        # transf = axs.transData.inverted()
        # bb = text1_elem.get_window_extent(renderer=fig.canvas.renderer)
        # bb_datacoords = bb.transformed(transf)

        self.graph_base64 = self.get_encoded_base64(fig)
        plt.close('all')
        return