import pandas as pd

from sweetviz.sv_types import OTHERS_GROUPED


def get_clamped_value_counts(value_counts: pd.Series, max_categories_incl_other: int) -> pd.Series:
    # Returns a Series of a maximum length, where overflowing rows are
    # put into a "Others" category (index = OTHERS_GROUPED)
    # IMPORTANT: assuming value_counts is ALREADY SORTED
    if len(value_counts) <= max_categories_incl_other:
        categories_shown_as_is = len(value_counts)
    else:
        categories_shown_as_is = max_categories_incl_other - 1

    # Fix for #10
    # clamped_series = pd.Series(value_counts[0:categories_shown_as_is])
    clamped_series = pd.Series(value_counts.head(categories_shown_as_is))

    # Fix for #10
    num_in_tail = len(value_counts) - categories_shown_as_is
    # categories_in_other = value_counts[categories_shown_as_is:]
    categories_in_other = value_counts.tail(num_in_tail)

    if len(categories_in_other) > 0:
        total_in_other = sum(categories_in_other)
        if clamped_series.index.dtype.name == 'category':
            # need to create categorical index
            clamped_series.index = clamped_series.index.add_categories([OTHERS_GROUPED])
            other_series = pd.Series([total_in_other],
                                     index=pd.CategoricalIndex([OTHERS_GROUPED], categories=clamped_series.index))

        else:
            other_series = pd.Series([total_in_other], index=[OTHERS_GROUPED])

        # UPDATE: series.append is deprecated!
        clamped_series = pd.concat([clamped_series, other_series])
        # clamped_series = clamped_series.append(other_series, ignore_index=False)
        # assert(clamped_series.equals(clamped_seriesOLD))
    return clamped_series


def get_matched_value_counts(value_counts: pd.Series, other_to_match: pd.Series) -> pd.Series:
    # Returns a "Value count" Series of another series ONLY for the values in
    # the original value_count

    matched_series = pd.Series(index=other_to_match.index, dtype=float)
    for ind in matched_series.index:
        if ind in value_counts:
            matched_series[ind] = value_counts[ind]
        else:
            matched_series[ind] = 0.0

    if OTHERS_GROUPED in matched_series.index:
        total = sum(value_counts)
        total_in_other = total - sum(matched_series)
        matched_series[OTHERS_GROUPED] = total_in_other
    # if total_in_other > 0:
    #     other_series = pd.Series([total_in_other], index = [OTHERS_GROUPED])
    #     matched_series = matched_series.append(other_series, ignore_index=False)

    return matched_series
# Thank you https://hackersandslackers.com/remove-duplicate-columns-in-pandas/


def get_duplicate_cols(df: pd.DataFrame) -> pd.Series:
    return pd.Series(df.columns).value_counts()[lambda x: x > 1]
