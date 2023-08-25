import numpy as np
import pandas as pd


def count_fraction_of_true(series: pd.Series):
    # We are assuming this is called by a Boolean series
    if series.dtype != bool and series.dtype != "Int64":
        raise ValueError
    num_true = series.sum()
    total = float(series.count())
    return num_true / total if total > 0.0 else 0.0, num_true
