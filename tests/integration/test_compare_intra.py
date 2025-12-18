"""Integration tests for sweetviz.compare_intra()."""
import pandas as pd
import pytest

import sweetviz


@pytest.fixture
def sample_dataframe_with_condition():
    """Create a dataframe with condition for intra comparison."""
    df = pd.DataFrame(
        {
            "numeric": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "categorical": ["A", "B", "A", "C", "B", "A", "B", "C", "A", "B"],
            "text": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
            "condition": [
                True,
                False,
                True,
                False,
                True,
                False,
                True,
                False,
                True,
                False,
            ],
        }
    )
    return df


def test_compare_intra_basic(sample_dataframe_with_condition):
    """Test basic compare_intra functionality."""
    df = sample_dataframe_with_condition
    condition = df["condition"]
    names = ("True Group", "False Group")

    report = sweetviz.compare_intra(df, condition, names)

    assert report is not None
    assert isinstance(report, sweetviz.DataframeReport)

    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0
    assert "<html" in html.lower()


def test_compare_intra_with_target(sample_dataframe_with_condition):
    """Test compare_intra with target feature."""
    df = sample_dataframe_with_condition
    condition = df["condition"]
    names = ("True Group", "False Group")

    report = sweetviz.compare_intra(df, condition, names, target_feat="categorical")
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_intra_with_feature_config(sample_dataframe_with_condition):
    """Test compare_intra with feature configuration."""
    df = sample_dataframe_with_condition
    condition = df["condition"]
    names = ("True Group", "False Group")
    feat_cfg = sweetviz.FeatureConfig(skip="text")

    report = sweetviz.compare_intra(df, condition, names, feat_cfg=feat_cfg)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_intra_with_pairwise_analysis(sample_dataframe_with_condition):
    """Test compare_intra with different pairwise analysis settings."""
    df = sample_dataframe_with_condition
    condition = df["condition"]
    names = ("True Group", "False Group")

    for setting in ["auto", "on", "off"]:
        report = sweetviz.compare_intra(df, condition, names, pairwise_analysis=setting)
        assert report is not None
        html = report.show_html()
        assert len(html) > 0


def test_compare_intra_length_mismatch_error():
    """Test that length mismatch raises ValueError."""
    df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})
    condition = pd.Series([True, False, True])  # Different length

    with pytest.raises(ValueError, match="same length"):
        sweetviz.compare_intra(df, condition, ("A", "B"))


def test_compare_intra_non_boolean_condition_error():
    """Test that non-boolean condition raises ValueError."""
    df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})
    condition = pd.Series([1, 0, 1, 0, 1])  # Not boolean

    with pytest.raises(ValueError, match="boolean"):
        sweetviz.compare_intra(df, condition, ("A", "B"))


def test_compare_intra_empty_true_group_error():
    """Test that empty TRUE dataset raises ValueError."""
    df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})
    condition = pd.Series([False, False, False, False, False])  # All False

    with pytest.raises(ValueError, match="TRUE dataset is empty"):
        sweetviz.compare_intra(df, condition, ("A", "B"))


def test_compare_intra_empty_false_group_error():
    """Test that empty FALSE dataset raises ValueError."""
    df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})
    condition = pd.Series([True, True, True, True, True])  # All True

    with pytest.raises(ValueError, match="FALSE dataset is empty"):
        sweetviz.compare_intra(df, condition, ("A", "B"))


def test_compare_intra_single_column():
    """Test compare_intra with single column dataframe."""
    df = pd.DataFrame({"col": [1, 2, 3, 4, 5]})
    condition = pd.Series([True, False, True, False, True])
    names = ("True", "False")

    report = sweetviz.compare_intra(df, condition, names)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_intra_missing_values():
    """Test compare_intra with missing values."""
    df = pd.DataFrame(
        {
            "numeric": [1, None, 3, 4, None, 6, 7, 8, None, 10],
            "categorical": ["A", None, "B", None, "C", "A", None, "B", "C", None],
        }
    )
    condition = pd.Series(
        [True, False, True, False, True, False, True, False, True, False]
    )
    names = ("True", "False")

    report = sweetviz.compare_intra(df, condition, names)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


@pytest.mark.slow
def test_compare_intra_large_dataframe():
    """Test compare_intra with larger dataframe."""
    df = pd.DataFrame(
        {
            "x": range(200),
            "y": [i * 2 for i in range(200)],
            "category": ["A", "B"] * 100,
        }
    )
    condition = pd.Series([i % 2 == 0 for i in range(200)])
    names = ("Even", "Odd")

    report = sweetviz.compare_intra(df, condition, names)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0


def test_compare_intra_column_index_rename():
    """Test that column named 'index' gets renamed to avoid conflicts."""
    df = pd.DataFrame(
        {
            "index": [1, 2, 3, 4, 5],  # Column named 'index'
            "value": [10, 20, 30, 40, 50],
        }
    )
    condition = pd.Series([True, False, True, False, True])
    names = ("True", "False")

    # Should not raise an error about reserved name
    report = sweetviz.compare_intra(df, condition, names)
    assert report is not None
    html = report.show_html()
    assert len(html) > 0
