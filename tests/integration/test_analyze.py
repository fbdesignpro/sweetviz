"""Integration tests for sweetviz.analyze()."""
import pandas as pd
import pytest

import sweetviz


@pytest.fixture
def sample_dataframe():
    """Create a simple dataframe for testing."""
    return pd.DataFrame(
        {
            "numeric": [1, 2, 3, 4, 5],
            "categorical": ["A", "B", "A", "C", "B"],
            "text": ["hello", "world", "foo", "bar", "baz"],
        }
    )


def test_analyze_basic(sample_dataframe):
    """Test basic analyze functionality."""
    report = sweetviz.analyze(sample_dataframe)

    # Report should be created without errors
    assert report is not None
    assert isinstance(report, sweetviz.DataframeReport)

    # Should be able to generate HTML
    html = report.show_html()
    assert isinstance(html, str)
    assert len(html) > 0
    assert "<html" in html.lower()
    assert "<head" in html.lower()
    assert "<body" in html.lower()


def test_analyze_with_target(sample_dataframe):
    """Test analyze with target feature."""
    report = sweetviz.analyze(sample_dataframe, target_feat="categorical")
    assert report is not None

    html = report.show_html()
    assert len(html) > 0


def test_analyze_with_feature_config(sample_dataframe):
    """Test analyze with feature configuration."""
    feat_cfg = sweetviz.FeatureConfig(skip="text")
    report = sweetviz.analyze(sample_dataframe, feat_cfg=feat_cfg)
    assert report is not None

    html = report.show_html()
    assert len(html) > 0


def test_analyze_with_pairwise_analysis(sample_dataframe):
    """Test analyze with different pairwise analysis settings."""
    for setting in ["auto", "on", "off"]:
        report = sweetviz.analyze(sample_dataframe, pairwise_analysis=setting)
        assert report is not None

        html = report.show_html()
        assert len(html) > 0


def test_analyze_with_verbosity(sample_dataframe):
    """Test analyze with verbosity parameter."""
    report = sweetviz.analyze(sample_dataframe, verbosity="off")
    assert report is not None

    html = report.show_html()
    assert len(html) > 0


def test_analyze_empty_dataframe():
    """Test analyze with empty dataframe."""
    df = pd.DataFrame()
    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert len(html) > 0


def test_analyze_single_column():
    """Test analyze with single column dataframe."""
    df = pd.DataFrame({"col": [1, 2, 3]})
    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert len(html) > 0


@pytest.mark.slow
def test_analyze_large_dataframe():
    """Test analyze with larger dataframe."""
    df = pd.DataFrame(
        {
            "x": range(100),
            "y": [i * 2 for i in range(100)],
            "category": ["A", "B"] * 50,
        }
    )
    report = sweetviz.analyze(df)
    assert report is not None

    html = report.show_html()
    assert len(html) > 0
