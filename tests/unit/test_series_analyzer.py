"""Unit tests for sweetviz.series_analyzer."""
import numpy as np
import pandas as pd
import pytest

import sweetviz.series_analyzer as sa
from sweetviz.sv_types import FeatureToProcess, FeatureType


@pytest.fixture
def numeric_series():
    """Create a numeric series for testing."""
    return pd.Series([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])


@pytest.fixture
def categorical_series():
    """Create a categorical series for testing."""
    return pd.Series(["A", "B", "A", "C", "B", "A", "B", "C", "A", "B"])


@pytest.fixture
def text_series():
    """Create a text series for testing."""
    return pd.Series(["hello world", "foo bar", "test text", "example", "data"])


@pytest.fixture
def mixed_series():
    """Create a series with mixed types (should be detected as categorical)."""
    return pd.Series([1, "a", 2, "b", 3, "c"])


@pytest.fixture
def empty_series():
    """Create an empty series."""
    return pd.Series([], dtype=float)


@pytest.fixture
def nan_series():
    """Create a series with NaN values."""
    return pd.Series([1.0, np.nan, 3.0, np.nan, 5.0])


@pytest.fixture
def single_value_series():
    """Create a series with a single value."""
    return pd.Series([42, 42, 42, 42, 42])


def test_get_counts_numeric(numeric_series):
    """Test get_counts with numeric series."""
    counts = sa.get_counts(numeric_series)

    assert isinstance(counts, dict)
    assert "value_counts_without_nan" in counts
    assert "distinct_count_without_nan" in counts
    assert "num_rows_with_data" in counts
    assert "num_rows_total" in counts

    assert counts["num_rows_total"] == 10
    assert counts["num_rows_with_data"] == 10
    assert counts["distinct_count_without_nan"] == 10


def test_get_counts_categorical(categorical_series):
    """Test get_counts with categorical series."""
    counts = sa.get_counts(categorical_series)

    assert counts["num_rows_total"] == 10
    assert counts["num_rows_with_data"] == 10
    assert counts["distinct_count_without_nan"] == 3  # A, B, C

    value_counts = counts["value_counts_without_nan"]
    assert value_counts["A"] == 4
    assert value_counts["B"] == 4
    assert value_counts["C"] == 2


def test_get_counts_empty(empty_series):
    """Test get_counts with empty series."""
    counts = sa.get_counts(empty_series)

    assert counts["num_rows_total"] == 0
    assert counts["num_rows_with_data"] == 0
    assert counts["distinct_count_without_nan"] == 0

    value_counts = counts["value_counts_without_nan"]
    assert len(value_counts) == 0


def test_get_counts_nan(nan_series):
    """Test get_counts with series containing NaN values."""
    counts = sa.get_counts(nan_series)

    assert counts["num_rows_total"] == 5
    assert counts["num_rows_with_data"] == 3  # 3 non-NaN values
    assert counts["distinct_count_without_nan"] == 3  # 1.0, 3.0, 5.0


def test_get_counts_single_value(single_value_series):
    """Test get_counts with single value series."""
    counts = sa.get_counts(single_value_series)

    assert counts["num_rows_total"] == 5
    assert counts["num_rows_with_data"] == 5
    assert counts["distinct_count_without_nan"] == 1

    value_counts = counts["value_counts_without_nan"]
    assert value_counts[42] == 5


def test_add_series_base_stats_to_dict(numeric_series):
    """Test add_series_base_stats_to_dict."""
    counts = sa.get_counts(numeric_series)
    result_dict = {}

    sa.add_series_base_stats_to_dict(numeric_series, counts, result_dict)

    assert "stats" in result_dict
    assert "base_stats" in result_dict
    base_stats = result_dict["base_stats"]

    assert base_stats["total_rows"] == 10
    assert base_stats["num_values"].count == 10
    assert base_stats["num_values"].percent == 100.0
    assert base_stats["num_missing"].count == 0
    assert base_stats["num_missing"].percent == 0.0
    assert base_stats["num_distinct"].count == 10
    assert base_stats["num_distinct"].percent == 100.0


def test_add_series_base_stats_to_dict_with_nan(nan_series):
    """Test add_series_base_stats_to_dict with NaN values."""
    counts = sa.get_counts(nan_series)
    result_dict = {}

    sa.add_series_base_stats_to_dict(nan_series, counts, result_dict)

    base_stats = result_dict["base_stats"]
    assert base_stats["total_rows"] == 5
    assert base_stats["num_values"].count == 3
    assert base_stats["num_values"].percent == 60.0
    assert base_stats["num_missing"].count == 2
    assert base_stats["num_missing"].percent == 40.0


def test_fill_out_missing_counts_in_other_series():
    """Test fill_out_missing_counts_in_other_series."""
    # Create two series with different value sets
    series1 = pd.Series(["A", "B", "A", "B"])
    series2 = pd.Series(["A", "C", "C", "D"])

    counts1 = sa.get_counts(series1)
    counts2 = sa.get_counts(series2)

    # Initially, counts1 only has A and B
    value_counts1 = counts1["value_counts_without_nan"]
    assert "A" in value_counts1
    assert "B" in value_counts1
    assert "C" not in value_counts1
    assert "D" not in value_counts1

    # Fill missing values from counts2
    sa.fill_out_missing_counts_in_other_series(counts1, counts2)

    # Now counts1 should have all values (A, B, C, D)
    value_counts1 = counts1["value_counts_without_nan"]
    assert "A" in value_counts1
    assert "B" in value_counts1
    assert "C" in value_counts1
    assert "D" in value_counts1

    # New values should have count 0
    assert value_counts1["C"] == 0
    assert value_counts1["D"] == 0


def test_analyze_feature_to_dictionary_numeric(numeric_series):
    """Test analyze_feature_to_dictionary with numeric series."""
    to_process = FeatureToProcess(
        series=numeric_series,
        series_name="test_numeric",
        feature_type=FeatureType.TYPE_NUM,
        associations={},
        associations_compare={},
        source_name="test",
        compare_name=None,
        is_target=False,
    )

    result = sa.analyze_feature_to_dictionary(to_process)

    assert isinstance(result, dict)
    assert "type" in result
    assert result["type"] == "NUM"
    assert "base_stats" in result
    assert "detail_pane" in result

    base_stats = result["base_stats"]
    assert base_stats["total_rows"] == 10
    assert base_stats["num_distinct"].count == 10


def test_analyze_feature_to_dictionary_categorical(categorical_series):
    """Test analyze_feature_to_dictionary with categorical series."""
    to_process = FeatureToProcess(
        series=categorical_series,
        series_name="test_categorical",
        feature_type=FeatureType.TYPE_CAT,
        associations={},
        associations_compare={},
        source_name="test",
        compare_name=None,
        is_target=False,
    )

    result = sa.analyze_feature_to_dictionary(to_process)

    assert isinstance(result, dict)
    assert "type" in result
    assert result["type"] == "CAT"
    assert "base_stats" in result
    assert "detail_pane" in result

    base_stats = result["base_stats"]
    assert base_stats["total_rows"] == 10
    assert base_stats["num_distinct"].count == 3  # A, B, C


def test_analyze_feature_to_dictionary_empty(empty_series):
    """Test analyze_feature_to_dictionary with empty series."""
    to_process = FeatureToProcess(
        series=empty_series,
        series_name="test_empty",
        feature_type=FeatureType.TYPE_NUM,
        associations={},
        associations_compare={},
        source_name="test",
        compare_name=None,
        is_target=False,
    )

    result = sa.analyze_feature_to_dictionary(to_process)

    assert isinstance(result, dict)
    assert "type" in result
    assert result["type"] == "NUM"

    base_stats = result["base_stats"]
    assert base_stats["total_rows"] == 0
    assert base_stats["num_values"].count == 0
    assert base_stats["num_missing"].count == 0
    assert base_stats["num_distinct"].count == 0


def test_analyze_feature_to_dictionary_as_target():
    """Test analyze_feature_to_dictionary when series is a target."""
    series = pd.Series([1, 0, 1, 0, 1])
    to_process = FeatureToProcess(
        series=series,
        series_name="target",
        feature_type=FeatureType.TYPE_BOOL,
        associations={},
        associations_compare={},
        source_name="test",
        compare_name=None,
        is_target=True,
    )

    result = sa.analyze_feature_to_dictionary(to_process)

    assert isinstance(result, dict)
    assert "type" in result
    assert result["type"] == "BOOL"
    # Target-specific stats might be different
    # This test ensures the function doesn't crash when is_target=True
