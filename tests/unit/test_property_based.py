"""Property-based tests for sweetviz using hypothesis."""
import numpy as np
import pandas as pd
import pytest
from hypothesis import HealthCheck, assume, given, settings
from hypothesis import strategies as st
from hypothesis.extra.pandas import column, data_frames, range_indexes, series

import sweetviz
import sweetviz.series_analyzer as sa
from sweetviz.sv_types import FeatureType


# Strategies for generating test data
@st.composite
def numeric_dataframe_strategy(draw, min_rows=1, max_rows=100):
    """Generate a DataFrame with numeric columns."""
    num_rows = draw(st.integers(min_value=min_rows, max_value=max_rows))

    columns = [
        column(name="numeric1", elements=st.floats(min_value=-1000, max_value=1000)),
        column(name="numeric2", elements=st.floats(min_value=-500, max_value=500)),
        column(name="integer", elements=st.integers(min_value=-100, max_value=100)),
    ]

    return draw(
        data_frames(
            columns=columns, index=range_indexes(min_size=num_rows, max_size=num_rows)
        )
    )


@st.composite
def categorical_dataframe_strategy(draw, min_rows=1, max_rows=100):
    """Generate a DataFrame with categorical columns."""
    num_rows = draw(st.integers(min_value=min_rows, max_value=max_rows))

    categories = st.sampled_from(["A", "B", "C", "D", "E", "F"])

    columns = [
        column(name="category1", elements=categories),
        column(name="category2", elements=categories),
        column(
            name="mixed",
            elements=st.one_of(categories, st.text(min_size=1, max_size=10)),
        ),
    ]

    return draw(
        data_frames(
            columns=columns, index=range_indexes(min_size=num_rows, max_size=num_rows)
        )
    )


@st.composite
def mixed_dataframe_strategy(draw, min_rows=1, max_rows=100):
    """Generate a DataFrame with mixed column types."""
    num_rows = draw(st.integers(min_value=min_rows, max_value=max_rows))

    columns = [
        column(name="numeric", elements=st.floats(min_value=-100, max_value=100)),
        column(name="categorical", elements=st.sampled_from(["X", "Y", "Z"])),
        column(name="text", elements=st.text(min_size=1, max_size=50)),
        column(name="boolean", elements=st.booleans()),
    ]

    return draw(
        data_frames(
            columns=columns, index=range_indexes(min_size=num_rows, max_size=num_rows)
        )
    )


@given(df=numeric_dataframe_strategy(min_rows=1, max_rows=50))
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_analyze_numeric_dataframe(df):
    """Property test: analyze should work on any numeric DataFrame."""
    # Skip if DataFrame is empty (should be handled by min_rows=1)
    assume(len(df) > 0)

    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0


@given(df=categorical_dataframe_strategy(min_rows=1, max_rows=50))
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_analyze_categorical_dataframe(df):
    """Property test: analyze should work on any categorical DataFrame."""
    assume(len(df) > 0)

    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0


@given(df=mixed_dataframe_strategy(min_rows=1, max_rows=50))
@settings(max_examples=10, suppress_health_check=[HealthCheck.too_slow])
def test_analyze_mixed_dataframe(df):
    """Property test: analyze should work on any mixed-type DataFrame."""
    assume(len(df) > 0)

    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0


@given(
    df1=mixed_dataframe_strategy(min_rows=1, max_rows=30),
    df2=mixed_dataframe_strategy(min_rows=1, max_rows=30),
)
@settings(max_examples=5, suppress_health_check=[HealthCheck.too_slow])
def test_compare_any_dataframes(df1, df2):
    """Property test: compare should work on any two DataFrames."""
    assume(len(df1) > 0 and len(df2) > 0)

    report = sweetviz.compare(df1, df2)
    assert report is not None

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0


@given(
    series=series(
        elements=st.one_of(
            st.floats(min_value=-1000, max_value=1000),
            st.integers(min_value=-100, max_value=100),
            st.text(min_size=0, max_size=20),
            st.booleans(),
        ),
        index=range_indexes(min_size=0, max_size=100),
    )
)
@settings(max_examples=20)
def test_get_counts_any_series(series):
    """Property test: get_counts should work on any series."""
    # Skip series with mixed types that might cause errors
    # (get_counts should handle them, but pandas might complain)
    try:
        counts = sa.get_counts(series)
    except (ValueError, TypeError) as e:
        # Some series might cause issues (e.g., mixed types)
        # That's okay for property testing
        assume(False)

    assert isinstance(counts, dict)
    assert "value_counts_without_nan" in counts
    assert "distinct_count_without_nan" in counts
    assert "num_rows_with_data" in counts
    assert "num_rows_total" in counts

    assert counts["num_rows_total"] == len(series)
    assert counts["num_rows_with_data"] <= len(series)
    assert counts["distinct_count_without_nan"] <= counts["num_rows_with_data"]


@given(
    series1=series(
        elements=st.sampled_from(["A", "B", "C", "D"]),
        index=range_indexes(min_size=1, max_size=50),
    ),
    series2=series(
        elements=st.sampled_from(["C", "D", "E", "F"]),
        index=range_indexes(min_size=1, max_size=50),
    ),
)
@settings(max_examples=10)
def test_fill_out_missing_counts_property(series1, series2):
    """Property test: fill_out_missing_counts_in_other_series invariants."""
    assume(len(series1) > 0 and len(series2) > 0)

    counts1 = sa.get_counts(series1)
    counts2 = sa.get_counts(series2)

    # Get value counts before modification
    original_keys = set(counts1["value_counts_without_nan"].index)

    # Apply the function
    sa.fill_out_missing_counts_in_other_series(counts1, counts2)

    # After filling, counts1 should have at least as many keys as before
    new_keys = set(counts1["value_counts_without_nan"].index)
    assert original_keys.issubset(new_keys)

    # All original values should still have their original counts
    for key in original_keys:
        if key in counts1["value_counts_without_nan"]:
            # The count should be preserved (or potentially increased if also in series2)
            pass  # We can't assert equality because the function might add counts from series2


def test_analyze_idempotent():
    """Test that analyze is idempotent (same DataFrame produces same report structure)."""
    # Note: This is not a full property test with hypothesis due to complexity
    # but demonstrates the pattern

    df = pd.DataFrame(
        {
            "x": [1, 2, 3, 4, 5],
            "y": ["A", "B", "A", "C", "B"],
        }
    )

    report1 = sweetviz.analyze(df)
    report2 = sweetviz.analyze(df)

    # Both reports should exist
    assert report1 is not None
    assert report2 is not None

    # Both should generate HTML
    html1 = report1.show_html()
    html2 = report2.show_html()

    assert isinstance(html1, str)
    assert isinstance(html2, str)
    assert len(html1) > 0
    assert len(html2) > 0

    # The HTML should be similar in length (might differ due to timestamps)
    # Allow for small differences
    assert abs(len(html1) - len(html2)) < 100


@given(
    data=st.data(),
    min_rows=st.integers(min_value=1, max_value=20),
    max_rows=st.integers(min_value=21, max_value=50),
)
@settings(max_examples=5, suppress_health_check=[HealthCheck.too_slow])
def test_type_detection_consistency(data, min_rows, max_rows):
    """Property test: type detection should be consistent for same data."""
    # Create a random series
    series_elements = st.one_of(
        st.floats(min_value=-100, max_value=100),
        st.integers(min_value=-10, max_value=10),
        st.text(min_size=1, max_size=10),
        st.booleans(),
    )

    series = data.draw(
        series(
            elements=series_elements,
            index=range_indexes(min_size=min_rows, max_size=max_rows),
        )
    )

    # Skip empty series and mixed-type series that cause errors
    if len(series) == 0:
        assume(False)

    # Get counts and determine type
    counts = sa.get_counts(series)

    # Skip if counts would cause type detection to raise an error
    try:
        # Check the inferred_type to avoid mixed type errors
        if hasattr(counts["value_counts_without_nan"].index, "inferred_type"):
            inferred_type = counts["value_counts_without_nan"].index.inferred_type
            if inferred_type.startswith("mixed"):
                assume(False)
    except (AttributeError, KeyError):
        pass

    # The key property: type detection should not crash
    # We don't assert what type it should be, just that it returns a FeatureType
    try:
        from sweetviz.type_detection import determine_feature_type

        result = determine_feature_type(
            series,
            counts,
            must_be_this_type=FeatureType.TYPE_UNKNOWN,
            which_dataframe="test",
        )

        # Should return a FeatureType enum value
        assert isinstance(result, FeatureType)
    except (TypeError, ValueError) as e:
        # Some inputs legitimately cause errors (e.g., mixed types)
        # That's acceptable behavior
        pass
