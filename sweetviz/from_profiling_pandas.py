from urllib.parse import urlparse
from pathlib import Path
import pandas as pd
from sweetviz.config import config

# This file contains modified functions from the profiling-pandas library,
# which you should check out at the following URL:
# https://github.com/pandas-profiling/pandas-profiling
#
# Used under the following license:
#
# The MIT License (MIT)
#
# Copyright (c) 2016 Jos Polfliet, 2019-2020 Simon Brugman
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def is_boolean(series: pd.Series, counts: dict) -> bool:
    keys = counts["value_counts_without_nan"].keys()
    if pd.api.types.is_bool_dtype(keys):
        return True
    elif (
            1 <= counts["distinct_count_without_nan"] <= 2
            and pd.api.types.is_numeric_dtype(series)
            and series[~series.isnull()].between(0, 1).all()
    ):
        return True
    elif 1 <= counts["distinct_count_without_nan"] <= 4:
        unique_values = set([str(value).lower() for value in keys.values])
        accepted_combinations = [
            ["y", "n"],
            ["yes", "no"],
            ["true", "false"],
            ["t", "f"],
        ]

        if len(unique_values) == 2 and any(
                [unique_values == set(bools) for bools in
                 accepted_combinations]
        ):
            return True
    return False


def is_categorical(series: pd.Series, counts: dict) -> bool:
    # keys = counts["value_counts_without_nan"].keys()
    # TODO: CHECK THIS CASE ACTUALLY WORKS
    # UPDATE 11-2023: NO IT DIDN'T!!! using series, not... keys (?!)
    if isinstance(series.dtype, pd.CategoricalDtype): # Deprecated in Pandas 2.1.3: pd.api.types.is_categorical_dtype(keys):
        return True
    elif pd.api.types.is_numeric_dtype(series) and \
            counts["distinct_count_without_nan"] \
            <= config["Type_Detection"].getint("max_numeric_distinct_to_be_categorical"):
        return True
    else:
        if counts["num_rows_with_data"] == 0:
            return False
        num_distinct = counts["distinct_count_without_nan"]
        fraction_distinct = num_distinct / float(counts["num_rows_with_data"])
        if fraction_distinct \
             > config["Type_Detection"].getfloat("max_text_fraction_distinct_to_be_categorical"):
            return False
        if num_distinct <= config["Type_Detection"].getint("max_text_distinct_to_be_categorical"):
            return True
    return False


def is_numeric(series: pd.Series, counts: dict) -> bool:
    return pd.api.types.is_numeric_dtype(series) and \
           counts["distinct_count_without_nan"] \
           > config["Type_Detection"].getint("max_numeric_distinct_to_be_categorical")

# For coercion, might need more testing!
def could_be_numeric(series: pd.Series) -> bool:
    return pd.api.types.is_numeric_dtype(series)


def is_url(series: pd.Series, counts: dict) -> bool:
    if counts["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str).apply(urlparse)
            return result.apply(
                lambda x: all([x.scheme, x.netloc, x.path])).all()
        except ValueError:
            return False
    else:
        return False


def str_is_path(p: str) -> bool:
    """Detects if the variable contains absolute paths. If so, we distinguish
    paths that exist and paths that are images.

    Args:
        p: the Path

    Returns:
        True is is an absolute path
    """
    try:
        path = Path(p)
        if path.is_absolute():
            return True
        else:
            return False
    except TypeError:
        return False


def is_path(series, counts) -> bool:
    if counts["distinct_count_without_nan"] > 0:
        try:
            result = series[~series.isnull()].astype(str).apply(str_is_path)
            return result.all()
        except ValueError:
            return False
    else:
        return False


def is_date(series) -> bool:
    is_date_value = pd.api.types.is_datetime64_dtype(series)
    return is_date_value


