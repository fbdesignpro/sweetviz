# Change log


#### 2.3.1 - 2023-11-29

- **Enhanced/Fixed:** show_notebook() now outputs a better HTML file, and has added for it (thanks @tvdboom)

#### 2.3.0 - 2023-11-16 (Verbosity added, many long-standing fixes)

- **Added:** Parameter for **verbosity** (full, progress_only, off)
- **Fixed:** Histogram inaccuracies due to incorrect binning (thanks @troy46), fixes #116, #127
- **Fixed:** Incorrect detection of categorical series in some cases
- **Fixed:** Deprecation warnings for *is_categorical_dtype* (thanks @GegznaV), fixes #162

#### 2.2.2 - 2023-10-09

- **Updated:** jQuery to the latest version 3.7.1 (thanks @hedsnz)

#### 2.2.1 - 2023-08-24 (Major compatibility update)

- **Updated:** Updated the project to use the latest build & packaging pipelines (pyproject.toml)
- **Updated:** Using the "warnings" library directly instead of np.warningS
- **Fixed:** "KeyError: None of ['index'] are in the columns" (for pandas > 2.0)
- **Fixed:** "AttributeError: numpy has no attribute 'warning'" (for numpy > 1.23)
- **Fixed:** "AttributeError: 'DataFrame' object has no attribute 'iteritems'"
- **Fixed:** np.bool deprecation warning
- **Fixed:** Pandas 'mad()' function deprecation warning

#### 2.1.4 - 2022-06-08

- **Fixed:** removed deprecation warnings

#### 2.1.3 - 2021-07-08

- **Enhanced:** added info tag for comet.ml-generated reports

#### 2.1.2 - 2021-05-27

- **Fixed:** issue with comet.ml in a notebook environment

#### 2.1.1 - 2021-05-27

- **Fixed:** division by zero crash in some cases
- **Fixed:** association graph description text
- **Fixed:** ignoring warning due to matplotlib/numpy/pandas version mismatches

#### 2.1.0 - 2021-04-01

- **Added:** support for Comet.ml

#### 2.0.9 - 2021-02-26

- **Added:** numerical features now show "ZEROES" count in the summary tab

#### 2.0.8 - 2021-02-23

- **Fixed:** issue causing "FloatingPointError: divide by zero encountered in true_divide" in some edge cases

#### 2.0.7 - 2021-02-19

- **Enhanced:** feature counts near 0% and 100% will now show a more accurate "<1%" and ">99%"
- **Enhanced:** added more changes to feature counting to make it more consistent
- **Enhanced:** now allowing tuples (not just lists) as parameters for naming datasets
- **Fixed:** appearance of feature numbers above 100 (better alignment) and 1000 (now shown vertically)
- **Fixed:** sorting issue causing feature summaries above 2500 to disappear
- **Fixed:** progress bar issues causing it to be repeated or cause line ending issues

#### 2.0.6 - 2021-02-04

- **Fixed:** report issue introduced in 2.0.5

#### 2.0.5 - 2021-02-04

- **Fixed:** crashes due to LaTeX escape codes in feature names that were causing "Font family ['STIXGeneral'] not found" errors
- **Fixed:** better handling of features named "index"
- **Enhanced:** made feature count more consistent and clear: taking "target" into account as well as explicitly calling out when features are not present in the comparison data frame
- **Enhanced:** made "Association" buttons more obvious and color-coded (they were a bit too hard to see given their importance)

#### 2.0.4 - 2020-12-10

- **Fixed:** re-fixed unclickable buttons in some circumstances
- **Tweaked:** changed default notebook scale factor to 1.0

#### 2.0.3 - 2020-12-10

- **Fixed:** problem with overlap in some categorical values in vertical layout when scaling is applied
- **Fixed:** default layout value ignored in show_notebooks()
- **Fixed:** unclickable buttons in some circumstances

#### 2.0.2 - 2020-11-30

- **Fixed:** issue with width "%" in default value INI

## 2.0.1 - 2020-11-30 (initial 2.0 release)

- **Added:** `show_notebook(...)` for embedded notebook support (Jupyter, Colab, etc.)
- **Added:** report size scaling
- **Added:** vertical report layout
- **Added:** INI defaults for all show_xxx function parameters
- **Updated:** disallowed NaN values for target features (resolves many interpretation & reporting issues)
- **Fixed:** boolean issues with NaN/missing data
- **Fixed:** association graph label issues
- **Fixed:** association detail display issues
- **Fixed:** numerous miscellaneous issues

#### 1.1.2 - 2020-11-05 (progress bar fixes)

- **Fixed:** fixed major display issues with progress bar in notebooks
- **Updated:** improved progress bar configuration/display

#### 1.1.1 - 2020-10-18

- **Updated:** restored compact font as default

## 1.1 - 2020-10-18 (Initial Official Release)

- **Added:** CJK font support
- **Added:** color-coding for % of missing values
- **Added:** "open_browser" option for show_html()
- **Enhanced:** multiple report generation fixes and cosmetic updates
- **Enhanced:** better correlation edge-case handling
- **Enhanced:** moved logo HTML to be easier to control through INI
- **Fixed:** issues with columns named 'index' and missing columns in comparison data. Closes #60.
- **Fixed:** for issues with missing data
- **Fixed:** support for numpy.float32 data. Closes #58.
- **Fixed:** issues for data columns with a single value
- **Fixed:** issues with page height
- **Fixed:** sorting issue when >500 features
- **Fixed:** multiple minor report generation issues


#### 1.0beta6 - 2020-08-12
- **Fixed:** numerical summary showing 0.00 for small values or ranges

#### 1.0beta5 - 2020-07-27
- **Fixed:** indexing issues that were causing warnings and report inconsistencies
- **Fixed:** selection issues in the reports

#### 1.0beta4 - 2020-07-23
- **Added:** __version__and other metadata
- **Fixed:** "KeyError" crash
- **Fixed:** error for coercion of boolean series to categorical
- **Enhanced:** error reporting output for type coercions

#### 1.0beta3 - 2020-07-19 (BETA START)
- **Added:** post-report-generation descriptive text for Jupyter/Colab
- **Re-added:** horizontal scrollbar
- **Added:** link to check for updates in header
- **Fixed:** all-NaN columns will not crash and get added to the report (as empty text feature)
- **Fixed:** detail tab title overflowing to 2 lines when multiple words
- **Fixed:** progress bar resetting to 0% when reaching 100%
- **Fixed:** images on Pypi site
- **Updated:** README

#### 1.0alpha8 - 2020-07-18
- **Added:** Support for categorical Pandas data type
- **Fixed:** MANY crash and general stability/compatibility issues! The library is now much more robust with regard to supporting different data and conditions.

#### 1.0alpha7 - 2020-06-09
- **Fixed:** "ValueError: index must be monotonic..." crash with some datasets (#10)

#### 1.0alpha6 - 2020-06-08 (ALPHA START)
- **Fixed:** forcing feature names to be strings, to avoid crashing if numerical (#9)
- **Improved:** error message in case of mixed type feature (#3)
- **Added:** CHANGELOG.md!
