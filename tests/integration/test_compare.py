"""Integration tests for sweetviz.compare()."""
import pandas as pd
import pytest

import sweetviz


@pytest.fixture
def sample_dataframes():
    """Create sample dataframes for comparison."""
    df1 = pd.DataFrame(
        {
            "numeric": [1, 2, 3, 4, 5],
            "categorical": ["A", "B", "A", "C", "B"],
            "text": ["hello", "world", "foo", "bar", "baz"],
        }
    )
    df2 = pd.DataFrame(
        {
            "numeric": [6, 7, 8, 9, 10],
            "categorical": ["B", "C", "A", "D", "E"],
            "text": ["test1", "test2", "test3", "test4", "test5"],
        }
    )
    return df1, df2


def test_compare_basic(sample_dataframes):
    """Test basic compare functionality."""
    df1, df2 = sample_dataframes
    report = sweetviz.compare(df1, df2)

    assert report is not None
    assert isinstance(report, sweetviz.DataframeReport)

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0
    assert "<html" in html.lower()


def test_compare_with_names(sample_dataframes):
    """Test compare with dataframe names."""
    df1, df2 = sample_dataframes
    report = sweetviz.compare([df1, "Source"], [df2, "Compared"])

    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_with_target(sample_dataframes):
    """Test compare with target feature."""
    df1, df2 = sample_dataframes
    report = sweetviz.compare(df1, df2, target_feat="categorical")

    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_with_feature_config(sample_dataframes):
    """Test compare with feature configuration."""
    df1, df2 = sample_dataframes
    feat_cfg = sweetviz.FeatureConfig(skip="text")
    report = sweetviz.compare(df1, df2, feat_cfg=feat_cfg)

    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_with_pairwise_analysis(sample_dataframes):
    """Test compare with different pairwise analysis settings."""
    df1, df2 = sample_dataframes
    for setting in ["auto", "on", "off"]:
        report = sweetviz.compare(df1, df2, pairwise_analysis=setting)
        assert report is not None
        html = report.show_html()
        assert len(html) > 0


def test_compare_different_columns():
    """Test compare with dataframes having different columns."""
    df1 = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
    df2 = pd.DataFrame({"col1": [4, 5, 6], "col3": ["x", "y", "z"]})

    report = sweetviz.compare(df1, df2)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_empty_dataframes():
    """Test compare with empty dataframes."""
    df1 = pd.DataFrame()
    df2 = pd.DataFrame()

    report = sweetviz.compare(df1, df2)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_missing_values():
    """Test compare with dataframes containing missing values."""
    df1 = pd.DataFrame(
        {
            "numeric": [1, None, 3, 4, 5],
            "categorical": ["A", None, "A", "C", "B"],
        }
    )
    df2 = pd.DataFrame(
        {
            "numeric": [None, 7, 8, 9, 10],
            "categorical": ["B", "C", None, "D", "E"],
        }
    )

    report = sweetviz.compare(df1, df2)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_duplicate_column_names_error():
    """Test that duplicate column names raise an error."""
    df1 = pd.DataFrame({"col": [1, 2, 3], "col": [4, 5, 6]})  # Duplicate column names
    df2 = pd.DataFrame({"col": [7, 8, 9]})

    # Note: pandas will rename duplicate columns automatically, but sweetviz checks for duplicates
    # We'll need to create a dataframe with actual duplicate names
    # This test might need adjustment based on actual behavior
    df1 = pd.DataFrame([[1, 2], [3, 4]], columns=["col", "col"])

    with pytest.raises(ValueError, match="Duplicate column names"):
        sweetviz.compare(df1, df2)


@pytest.mark.slow
def test_compare_large_dataframes():
    """Test compare with larger dataframes."""
    df1 = pd.DataFrame(
        {
            "x": range(100),
            "y": [i * 2 for i in range(100)],
            "category": ["A", "B"] * 50,
        }
    )
    df2 = pd.DataFrame(
        {
            "x": range(100, 200),
            "y": [i * 3 for i in range(100)],
            "category": ["C", "D"] * 50,
        }
    )

    report = sweetviz.compare(df1, df2)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0
