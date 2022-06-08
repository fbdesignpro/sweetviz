import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sweetviz.sv_types import FeatureType
import sweetviz.graph
from sweetviz.config import config
import itertools
import matplotlib.patches as patches
from textwrap import wrap

# Portions of this file contain code from the following repository:
# https://github.com/dylan-profiler/heatmaps
#
# Used under the following license:
#
# BSD 3-Clause License
#
# Copyright (c) 2019, Drazen Zaric
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# A name for a custom index column that likely will not be used by users
UNIQUE_INDEX_NAME = 'indexZZ8vr$#RVwadfaFASDFSA'

# Something to detect correlation errors to display
# TODO: Better/more intuitive display of correlation errors (right now just show up as empty)
CORRELATION_ERROR = 83572398457329.0
CORRELATION_IDENTICAL = 1357239845732.0

def wrap_custom(source_text, separator_chars, width=70, keep_separators = True):
    current_length = 0
    latest_separator = -1
    current_chunk_start = 0
    output = ""
    char_index = 0
    while char_index < len(source_text):
        if source_text[char_index] in separator_chars:
            latest_separator = char_index
        output += source_text[char_index]
        current_length += 1
        if current_length == width:
            if latest_separator >= current_chunk_start:
                # Valid earlier separator, cut there
                cutting_length = char_index - latest_separator
                if not keep_separators:
                    cutting_length += 1
                if cutting_length:
                    output = output[:-cutting_length]
                output += "\n"
                current_chunk_start = latest_separator + 1
                char_index = current_chunk_start
            else:
                # No separator found, hard cut
                output += "\n"
                current_chunk_start = char_index + 1
                latest_separator = current_chunk_start - 1
                char_index += 1
            current_length = 0
        else:
            char_index += 1
    return output

class GraphAssoc(sweetviz.graph.Graph):
    def __init__(self, dataframe_report, which_graph: str, association_data):
        self.set_style(["graph_base.mplstyle"])

        # Set categories to use first (some may be unused but no need to optimize this)
        categoricals = [dataframe_report[feature]["name"] for feature in dataframe_report._features \
                        if dataframe_report[feature]["type"] in [FeatureType.TYPE_CAT,
                                                                 FeatureType.TYPE_BOOL]]
        nums = [dataframe_report[feature]["name"] for feature in dataframe_report._features \
                if dataframe_report[feature]["type"] == FeatureType.TYPE_NUM]
        combined = [dataframe_report[feature]["name"] for feature in dataframe_report._features \
                    if dataframe_report[feature]["type"] in [FeatureType.TYPE_CAT,
                                                             FeatureType.TYPE_BOOL,
                                                             FeatureType.TYPE_NUM] and \
                        feature in association_data]
        # Add target at beginning
        if dataframe_report._target is not None and dataframe_report._target["name"] in association_data:
            for list_of_features in [categoricals, nums, combined]:
                list_of_features.insert(0, dataframe_report._target["name"])

        if len(association_data) == 0 or len(combined) == 0:
            f, axs = plt.subplots(1, 1, figsize=(1,1))
            self.graph_base64 = self.get_encoded_base64(f)
            plt.close(f)
            return

        # Build graph_data dataframe with the information we need for the type of graph we want
        if which_graph == "all":
            # ALL
            graph_data = make_zero_square_dataframe(combined)

            for feature in combined:
                for associated_feature_name in combined:
                    associated_feature_val = association_data[feature].get( \
                        associated_feature_name)
                    if associated_feature_val is not None:
                        graph_data.at[combined.index(feature), associated_feature_name] = \
                            associated_feature_val
            # Workaround
            graph_data[UNIQUE_INDEX_NAME] = combined
            graph_data.set_index(UNIQUE_INDEX_NAME, inplace=True)
            # matplotlib.use('tkagg')
            # corrplot(graph_data)
            # plt.show()


        elif which_graph == "cat-cat":
            # CATEGORY-CATEGORY
            # Associations: _associations[FEATURE][GIVES INFORMATION ABOUT THIS FEATURE]
            graph_data = make_zero_square_dataframe(categoricals)

            for feature in categoricals:
                for associated_feature_name in categoricals:
                    associated_feature_val = association_data[feature].get( \
                        associated_feature_name)
                    if associated_feature_val is not None:
                        graph_data.at[categoricals.index(feature), associated_feature_name] = \
                            associated_feature_val
            # Workaround
            graph_data['index'] = categoricals
            graph_data.set_index('index', inplace=True)

        elif which_graph == "num-num":
            # NUM-NUM
            graph_data = make_zero_square_dataframe(nums)

            for feature in nums:
                for associated_feature_name in nums:
                    associated_feature_val = association_data[feature].get( \
                        associated_feature_name)
                    if associated_feature_val is not None:
                        # Make symmetrical, values in both
                        graph_data.at[nums.index(feature), associated_feature_name] = \
                            associated_feature_val
                        graph_data.at[nums.index(associated_feature_name), feature] = \
                            associated_feature_val
            # Workaround
            graph_data['index'] = nums
            graph_data.set_index('index', inplace=True)

        elif which_graph == "cat-num":
            # CAT-NUM

            # RECTANGULAR: rows are categories. Still, make a square, with categories first
            # (we will just not render the Unused rows/cols)
            graph_data = pd.DataFrame()
            # Add columns
            empty_row_dict = dict()
            for feature in nums:
                graph_data[feature] = pd.Series()
                empty_row_dict[feature] = 0.0
            if len(nums) > len(categoricals):
                for i in range(len(categoricals), len(nums)):
                    graph_data[str(i)+"PAD"] = pd.Series()
                    empty_row_dict[str(i)+"PAD"] = 0.0

            # Add series
            for categorical in categoricals:
                graph_data = graph_data.append(pd.Series(empty_row_dict, name=categorical))
            if len(categoricals) > len(nums):
                for i in range(len(nums), len(categoricals)):
                    graph_data = graph_data.append(pd.Series(empty_row_dict, name=str(i)+"RPAD"))

            # MUST DROP INDEX GRRRR
            orig_index = graph_data.index.values
            graph_data.reset_index(drop=True, inplace=True)

            for feature in categoricals:
                for associated_feature_name in nums:
                    associated_feature_val = association_data[feature].get( \
                        associated_feature_name)
                    if associated_feature_val is not None:
                        graph_data.at[categoricals.index(feature), associated_feature_name] = \
                            associated_feature_val
            # Workaround
            graph_data['index'] = orig_index
            graph_data.set_index('index', inplace=True)

        # Finalize Graph
        #plt.subplots_adjust(bottom=0.15, right=0.85, top=0.97, left=0.15)
        f = corrplot(graph_data, dataframe_report)
        self.graph_base64 = self.get_encoded_base64(f)
        plt.close(f)
        return


def make_zero_square_dataframe(features):
    new_dataframe = pd.DataFrame()
    # Add columns
    # empty_row_dict = dict()
    for feature in features:
        new_dataframe[feature] = pd.Series(dtype=float)
        # empty_row_dict[feature] = 0.0
    new_dataframe = new_dataframe.reindex(list(range(0, len(features)))).reset_index(drop=True).fillna(0.0)
    # Add series
    # for categorical in features:
    #     # UPDATE: series.append is deprecated!
    #     new_dataframe = new_dataframe.append(pd.Series(empty_row_dict, name=feature))
    #     # new_dataframe = pd.concat([new_dataframe, pd.Series(empty_row_dict, name=feature)], axis=1, join='outer', ignore_index=False)
    # MUST DROP INDEX GRRRR
    return new_dataframe.reset_index(drop=True)

def heatmap(y, x, figure_size, **kwargs):
    if 'color' in kwargs:
        color = kwargs['color']
    else:
        color = [1]*len(x)

    palette = []
    n_colors = 256
    for i in range(0,128):
        palette.append( (0.85, (0.85/128)*i, (0.85/128)*i ))
    for i in range(128,256):
        palette.append( (0.85 - 0.85*(i-128.0)/128.0, 0.85 - 0.85*(i-128.0)/128.0, 0.85 ))

    if 'color_range' in kwargs:
        color_min, color_max = kwargs['color_range']
    else:
        color_min, color_max = min(color), max(color) # Range of values that will be mapped to the palette, i.e. min and max possible correlation

    def value_to_color(val):
        if color_min == color_max:
            return palette[-1]
        else:
            # For now, return "max positive" correlation color
            if val == CORRELATION_IDENTICAL:
                return palette[(n_colors - 1)]
            if val == CORRELATION_ERROR:
                return palette[(n_colors - 1)]
            val_position = float((val - color_min)) / (color_max - color_min) # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            # LOG IT
            val_position = math.pow(val_position, 0.925)
            ind = int(val_position * (n_colors - 1)) # target index in the color palette
            return palette[ind]

    if 'size' in kwargs:
        size = kwargs['size']
    else:
        size = [1]*len(x)

    if 'size_range' in kwargs:
        size_min, size_max = kwargs['size_range'][0], kwargs['size_range'][1]
    else:
        size_min, size_max = min(size), max(size)

    size_scale = kwargs.get('size_scale', 500)

    # Scale with num squares
    size_scale = size_scale / len(x)
    def value_to_size(val):
        if val == 0:
            return 0.0
        if val == abs(CORRELATION_IDENTICAL):
            return 1.0
        # TODO: Better/more intuitive display of correlation errors
        if val == abs(CORRELATION_ERROR):
            return 0.0
        if size_min == size_max:
            return 1 * size_scale
        else:
            val_position = (val - size_min) * 0.999 / (size_max - size_min) + 0.001 # position of value in the input range, relative to the length of the input range
            val_position = min(max(val_position, 0), 1) # bound the position betwen 0 and 1
            # LOG IT
            val_position = math.pow(val_position, 0.5)
            return val_position
            # val_position = int(val_position*2)+4
            # return int(size_scale)
            # return val_position * int(size_scale)

    def do_wrapping(label, length):
        return wrap_custom(label, ["_", "-"], length)
        # return '\n'.join(wrap(label, 15))
    wrap_x = 12 # at top/bottom
    wrap_y = 13
    if 'x_order' in kwargs:
        x_names = [t for t in kwargs['x_order']]
    else:
        x_names = [t for t in sorted(set([v for v in x]))]
    # Wrap to help avoid overflow
    x_names = [do_wrapping(label, wrap_x) for label in x_names]

    x_to_num = {p[1]:p[0] for p in enumerate(x_names)}

    if 'y_order' in kwargs:
        y_names = [t for t in kwargs['y_order']]
    else:
        y_names = [t for t in sorted(set([v for v in y]))]
    # Wrap to help avoid overflow
    y_names = [do_wrapping(label, wrap_y) for label in y_names]

    y_to_num = {p[1]:p[0] for p in enumerate(y_names)}

    figure, axs = plt.subplots(1, 1, figsize=figure_size)

    plot_grid = plt.GridSpec(1, 15, figure = figure) # Setup a 1x10 grid
    # plot_grid = plt.GridSpec(1, 15, hspace=0.2, wspace=0.1, figure = f) # Setup a 1x10 grid
    ax = plt.subplot(plot_grid[:,:-1]) # Use the left 14/15ths of the grid for the main plot

    marker = kwargs.get('marker', 's')

    kwargs_pass_on = {k:v for k,v in kwargs.items() if k not in [
         'color', 'palette', 'color_range', 'size', 'size_range', 'size_scale', 'marker', 'x_order', 'y_order'
    ]}

    ax.tick_params(labelbottom='on', labeltop='on')
    ax.set_xticks([v for k,v in x_to_num.items()])
    ax.set_xticklabels([k for k in x_to_num], rotation=90, horizontalalignment='center', linespacing=0.8)
    ax.set_yticks([v for k,v in y_to_num.items()])
    ax.set_yticklabels([k for k in y_to_num], linespacing=0.85)

    ax.grid(False, 'major')
    ax.grid(True, 'minor')
    ax.set_xticks([t + 0.5 for t in ax.get_xticks()], minor=True)
    ax.set_yticks([t + 0.5 for t in ax.get_yticks()], minor=True)

    ax.set_xlim([-0.5, max([v for v in x_to_num.values()]) + 0.5])
    ax.set_ylim([-0.5, max([v for v in y_to_num.values()]) + 0.5])
    ax.set_facecolor('#F1F1F1')
    # figure.show()
    #figure.savefig("ASSOCTEST")
    delta_in_pix = ax.transData.transform((1, 1)) - ax.transData.transform((0, 0))

    index = 0
    for cur_x, cur_y in zip(x,y):
        wrapped_x_name = do_wrapping(cur_x, wrap_x)
        wrapped_y_name = do_wrapping(cur_y, wrap_y)
        before_coordinate = np.array(ax.transData.transform((x_to_num[wrapped_x_name]-0.5, y_to_num[wrapped_y_name] -0.5)))
        after_coordinate = np.array(ax.transData.transform((x_to_num[wrapped_x_name]+0.5, y_to_num[wrapped_y_name] +0.5)))
        before_pixels = np.round(before_coordinate, 0)
        after_pixels = np.round(after_coordinate, 0)
        desired_fraction = value_to_size(size[index])
        if desired_fraction == 0.0:
            index = index + 1
            continue
        if kwargs["dataframe_report"][cur_x]["type"] == FeatureType.TYPE_NUM and \
            kwargs["dataframe_report"][cur_y]["type"] == FeatureType.TYPE_NUM:
            use_rectangle = False
        else:
            use_rectangle = True
            # desired_fraction = desired_fraction / 0.707
        delta_in_pix = after_pixels - before_pixels
        gap = np.round((1.0 - desired_fraction) * delta_in_pix / 2, 0)
        start = before_pixels + gap[0]
        ending = after_pixels - gap[0]
        start[0] = start[0] + 1
        ending[1] = ending[1] - 1
        start_doc = ax.transData.inverted().transform(start)
        ending_doc = ax.transData.inverted().transform(ending)
        cur_size = ending_doc - start_doc
        # cur_size = 0.50
        # bottom_left = ax.transData.transform((x_to_num[cur_x]-0.5, y_to_num[cur_y]))
        # print(f"{bottom_left[0]}")
        if use_rectangle:
            cur_rect = patches.Rectangle((start_doc[0], start_doc[1]),
                                         cur_size[0], cur_size[1], facecolor=value_to_color(color[index]),
                                         antialiased=True)
        else:
            cur_rect = patches.Circle((start_doc[0] + cur_size[0] / 2, start_doc[1] + cur_size[1] / 2),
                                          cur_size[1] / 2, facecolor=value_to_color(color[index]),
                                         antialiased=True)
        cur_rect.set_antialiased(True)
        ax.add_patch(cur_rect)
        index = index + 1
    # ax.scatter(
    #     x=[x_to_num[v] for v in x],
    #     y=[y_to_num[v] for v in y],
    #     marker=marker,
    #     s=[value_to_size(v) for v in size],
    #     c=[value_to_color(v) for v in color],
    #     **kwargs_pass_on
    # )

    # Add color legend on the right side of the plot
    if color_min < color_max:
        ax = plt.subplot(plot_grid[:,-1]) # Use the rightmost column of the plot

        col_x = [0]*len(palette) # Fixed x coordinate for the bars
        bar_y=np.linspace(color_min, color_max, n_colors) # y coordinates for each of the n_colors bars
        ax.set_ylim(-1, 1)
        bar_height = bar_y[1] - bar_y[0]
        ax.barh(
            y=bar_y,
            width=[5]*len(palette), # Make bars 5 units wide
            left=col_x, # Make bars start at 0
            height=bar_height,
            color=palette,
            linewidth=0
        )
        ax.set_xlim(1, 2) # Bars are going from 0 to 5, so lets crop the plot somewhere in the middle
        ax.grid(False) # Hide grid
        ax.set_facecolor('white') # Make background white
        ax.set_xticks([]) # Remove horizontal ticks
        ax.set_yticks(np.linspace(min(bar_y), max(bar_y), 3)) # Show vertical ticks for min, middle and max
        ax.yaxis.tick_right() # Show vertical ticks on the right
    return figure

def filter_best_corr(correlation_dataframe):
    top_values = dict()
    for features in itertools.product(correlation_dataframe.index.values, \
        correlation_dataframe.columns):
        val = correlation_dataframe[features[0]][features[1]]
        for f in features:
            if f not in top_values.keys():
                top_values[f] = val
            elif val > top_values[f]:
                top_values[f] = val
    ordered = {k: v for k, v in sorted(top_values.items(), key=lambda item: item[1])}

def corrplot(correlation_dataframe, dataframe_report, size_scale=100, marker='s'):
    #              PassengerId  Survived    Pclass  ...     SibSp     Parch      Fare
    # PassengerId     1.000000 -0.005007 -0.035144  ... -0.057527 -0.001652  0.012658
    # Survived       -0.005007  1.000000 -0.338481  ... -0.035322  0.081629  0.257307
    # Pclass         -0.035144 -0.338481  1.000000  ...  0.083081  0.018443 -0.549500
    # Age             0.036847 -0.077221 -0.369226  ... -0.308247 -0.189119  0.096067
    # SibSp          -0.057527 -0.035322  0.083081  ...  1.000000  0.414838  0.159651
    # Parch          -0.001652  0.081629  0.018443  ...  0.414838  1.000000  0.216225
    # Fare            0.012658  0.257307 -0.549500  ...  0.159651  0.216225  1.000000
    # filter_best_corr(correlation_dataframe)
    sweetviz.graph.Graph.set_style(["graph_base.mplstyle"])
    corr = pd.melt(correlation_dataframe.reset_index(), id_vars=UNIQUE_INDEX_NAME)
    corr.columns = ['x', 'y', 'value']
    # e.g.:
    #              x            y     value
    # 0   PassengerId  PassengerId  1.000000
    # 1      Survived  PassengerId -0.005007
    # 2        Pclass  PassengerId -0.035144
    # 3           Age  PassengerId  0.036847
    # 4         SibSp  PassengerId -0.057527
    # 5         Parch  PassengerId -0.001652
    # 6          Fare  PassengerId  0.012658
    # 7   PassengerId     Survived -0.005007
    # 8      Survived     Survived  1.000000
    # 9        Pclass     Survived -0.338481
    # 10          Age     Survived -0.077221
    # 11        SibSp     Survived -0.035322
    # 12        Parch     Survived  0.081629
    # 13         Fare     Survived  0.257307
    # 14  PassengerId       Pclass -0.035144

    return heatmap(
        corr['x'], corr['y'],
        figure_size=(config["Associations"].getfloat("association_graph_width"),
                 config["Associations"].getfloat("association_graph_height")),
        color=corr['value'], color_range=[-1, 1],
        palette=None,
        size=corr['value'].abs(), size_range=[0,1],
        marker=marker,
        x_order=correlation_dataframe.columns,
        y_order=correlation_dataframe.columns[::-1],
        size_scale=config["Associations"].getfloat("association_graph_size_scale"),
        dataframe_report = dataframe_report
    )

