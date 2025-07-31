# Sweetviz

[![v](https://img.shields.io/badge/version-2.3.1-blue)](https://pypi.org/project/sweetviz/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/sweetviz.svg)](https://pypi.python.org/pypi/sweetviz/)
[![PyPI license](https://img.shields.io/pypi/l/sweetviz.svg)](https://pypi.python.org/pypi/sweetviz/)

**Sweetviz** is an open-source Python library that generates beautiful, high-density visualizations to kickstart EDA (Exploratory Data Analysis) with just two lines of code. Output is a fully self-contained HTML application.

The system is built around quickly **visualizing target values** and **comparing datasets**. Its goal is to help quick analysis of target characteristics, training vs testing data, and other such data characterization tasks.

![Features](httpshttps://raw.githubusercontent.com/fbdesignpro/sweetviz/main/docs/images/features.png)

## Features

-   **Target analysis**: Shows how a target value (e.g. "Survived" in the Titanic dataset) relates to other features.
-   **Visualize and compare**:
    -   Distinct datasets (e.g. training vs test data).
    -   Intra-set characteristics (e.g. male versus female).
-   **Mixed-type associations**: Sweetviz integrates associations for numerical (Pearson's correlation), categorical (uncertainty coefficient) and categorical-numerical (correlation ratio) datatypes seamlessly, to provide maximum information for all data types.
-   **Type inference**: Automatically detects numerical, categorical and text features, with optional manual overrides.
-   **Summary information**:
    -   Type, unique values, missing values, duplicate rows, most frequent values.
    -   Numerical analysis: min/max/range, quartiles, mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness.

## Installation

Install using pip:

```sh
pip install sweetviz
```

## Basic Usage

Creating a report is a quick 2-line process:

1.  Create a `DataframeReport` object using one of: `analyze()`, `compare()` or `compare_intra()`.
2.  Use a `show_xxx()` function to render the report. You can now use either **html** or **notebook** report options, as well as scaling.

### Analyze a single dataframe

```python
import sweetviz as sv
import pandas as pd

# Load the Titanic dataset
df = pd.read_csv("titanic.csv")

# Analyze the dataset
my_report = sv.analyze(df)

# Generate the HTML report
my_report.show_html("titanic_report.html")
```

This will generate a `titanic_report.html` file in the same directory.

### Compare two dataframes

```python
# Compare two dataframes (e.g. training vs test)
my_report = sv.compare([train_df, "Training Data"], [test_df, "Test Data"], "Survived")
my_report.show_html("compare_report.html")
```

### Compare two subsets of the same dataframe

```python
# Compare two subsets of the same dataframe (e.g. male vs female)
my_report = sv.compare_intra(df, df["Sex"] == "male", ["Male", "Female"], "Survived")
my_report.show_html("compare_intra_report.html")
```

## Documentation

For more detailed documentation on all the available features and customization options, please see the [official documentation](https://pypi.org/project/sweetviz/).

## Contributing

Contributions are welcome! Please see the [contributing guidelines](https://github.com/fbdesignpro/sweetviz/blob/main/CONTRIBUTING.md) for more information.

## License

Sweetviz is licensed under the [MIT License](https://github.com/fbdesignpro/sweetviz/blob/main/LICENSE).
