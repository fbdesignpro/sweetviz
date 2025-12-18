"""Unit tests for sweetviz.type_detection."""
import numpy as np
import pandas as pd
import pytest

import sweetviz.series_analyzer as sa
from sweetviz.sv_types import FeatureType
from sweetviz.type_detection import determine_feature_type


@pytest.fixture
def numeric_counts():
    """Create counts for numeric series."""
    series = pd.Series([1, 2, 3, 4, 5])
    return sa.get_counts(series)


@pytest.fixture
def categorical_counts():
    """Create counts for categorical series."""
    series = pd.Series(["A", "B", "A", "C", "B"])
    return sa.get_counts(series)


@pytest.fixture
def boolean_counts():
    """Create counts for boolean series."""
    series = pd.Series([True, False, True, True, False])
    return sa.get_counts(series)


@pytest.fixture
def text_counts():
    """Create counts for text series."""
    series = pd.Series(["hello world", "foo bar", "test", "example text", "data"])
    return sa.get_counts(series)


@pytest.fixture
def empty_counts():
    """Create counts for empty series."""
    series = pd.Series([], dtype=float)
    return sa.get_counts(series)


@pytest.fixture
def all_nan_counts():
    """Create counts for all-NaN series."""
    series = pd.Series([np.nan, np.nan, np.nan])
    return sa.get_counts(series)


def test_determine_feature_type_numeric(numeric_counts):
    """Test determine_feature_type with numeric data."""
    series = pd.Series([1, 2, 3, 4, 5], name="numeric_col")

    result = determine_feature_type(
        series,
        numeric_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_NUM


def test_determine_feature_type_categorical(categorical_counts):
    """Test determine_feature_type with categorical data."""
    series = pd.Series(["A", "B", "A", "C", "B"], name="categorical_col")

    result = determine_feature_type(
        series,
        categorical_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_CAT


def test_determine_feature_type_boolean(boolean_counts):
    """Test determine_feature_type with boolean data."""
    series = pd.Series([True, False, True, True, False], name="boolean_col")

    result = determine_feature_type(
        series,
        boolean_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_BOOL


def test_determine_feature_type_text(text_counts):
    """Test determine_feature_type with text data."""
    series = pd.Series(["hello world", "foo bar", "test"], name="text_col")

    result = determine_feature_type(
        series,
        text_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_TEXT


def test_determine_feature_type_empty(empty_counts):
    """Test determine_feature_type with empty series."""
    series = pd.Series([], dtype=float, name="empty_col")

    result = determine_feature_type(
        series,
        empty_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_ALL_NAN


def test_determine_feature_type_all_nan(all_nan_counts):
    """Test determine_feature_type with all-NaN series."""
    series = pd.Series([np.nan, np.nan, np.nan], name="nan_col")

    result = determine_feature_type(
        series,
        all_nan_counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    assert result == FeatureType.TYPE_ALL_NAN


def test_determine_feature_type_mixed_type_error():
    """Test determine_feature_type raises error for mixed types."""
    # Create a series with mixed types (int and str)
    series = pd.Series([1, "a", 2, "b"], name="mixed_col")
    counts = sa.get_counts(series)

    # This should raise a TypeError due to mixed inferred_type
    with pytest.raises(TypeError, match="mixed"):
        determine_feature_type(
            series,
            counts,
            must_be_this_type=FeatureType.TYPE_UNKNOWN,
            which_dataframe="test",
        )


def test_determine_feature_type_coercion_text_to_cat():
    """Test coercion from TEXT to CAT."""
    series = pd.Series(["a", "b", "c"], name="text_col")
    counts = sa.get_counts(series)

    # Force it to be categorical
    result = determine_feature_type(
        series, counts, must_be_this_type=FeatureType.TYPE_CAT, which_dataframe="test"
    )

    assert result == FeatureType.TYPE_CAT


def test_determine_feature_type_coercion_cat_to_text():
    """Test coercion from CAT to TEXT."""
    series = pd.Series(["a", "b", "a"], name="cat_col")
    counts = sa.get_counts(series)

    # Force it to be text
    result = determine_feature_type(
        series, counts, must_be_this_type=FeatureType.TYPE_TEXT, which_dataframe="test"
    )

    assert result == FeatureType.TYPE_TEXT


def test_determine_feature_type_coercion_bool_to_text():
    """Test coercion from BOOL to TEXT."""
    series = pd.Series([True, False, True], name="bool_col")
    counts = sa.get_counts(series)

    # Force it to be text
    result = determine_feature_type(
        series, counts, must_be_this_type=FeatureType.TYPE_TEXT, which_dataframe="test"
    )

    assert result == FeatureType.TYPE_TEXT


def test_determine_feature_type_coercion_numeric_to_categorical():
    """Test coercion from NUM to CAT."""
    series = pd.Series([1, 2, 3], name="num_col")
    counts = sa.get_counts(series)

    # Force it to be categorical
    result = determine_feature_type(
        series, counts, must_be_this_type=FeatureType.TYPE_CAT, which_dataframe="test"
    )

    assert result == FeatureType.TYPE_CAT


def test_determine_feature_type_coercion_numeric_to_text():
    """Test coercion from NUM to TEXT."""
    series = pd.Series([1, 2, 3], name="num_col")
    counts = sa.get_counts(series)

    # Force it to be text
    result = determine_feature_type(
        series, counts, must_be_this_type=FeatureType.TYPE_TEXT, which_dataframe="test"
    )

    assert result == FeatureType.TYPE_TEXT


def test_determine_feature_type_coercion_unsupported():
    """Test that unsupported coercions raise TypeError."""
    series = pd.Series(["a", "b", "c"], name="cat_col")
    counts = sa.get_counts(series)

    # Try to coerce CAT to NUM (should fail)
    with pytest.raises(TypeError, match="Cannot force"):
        determine_feature_type(
            series,
            counts,
            must_be_this_type=FeatureType.TYPE_NUM,
            which_dataframe="test",
        )


def test_determine_feature_type_with_numeric_looking_strings():
    """Test with strings that look numeric."""
    # Strings that look numeric should be categorical/text, not numeric
    series = pd.Series(["1", "2", "3"], name="string_numbers")
    counts = sa.get_counts(series)

    result = determine_feature_type(
        series,
        counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    # Should be CAT (short strings) not NUM
    assert result == FeatureType.TYPE_CAT


def test_determine_feature_type_single_value():
    """Test with series containing a single value."""
    series = pd.Series([42, 42, 42, 42], name="single_value")
    counts = sa.get_counts(series)

    result = determine_feature_type(
        series,
        counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    # Single numeric value should still be NUM
    assert result == FeatureType.TYPE_NUM


def test_determine_feature_type_with_nan_values():
    """Test with series containing NaN values."""
    series = pd.Series([1.0, np.nan, 3.0, np.nan, 5.0], name="with_nan")
    counts = sa.get_counts(series)

    result = determine_feature_type(
        series,
        counts,
        must_be_this_type=FeatureType.TYPE_UNKNOWN,
        which_dataframe="test",
    )

    # Should still be NUM despite NaN values
    assert result == FeatureType.TYPE_NUM
