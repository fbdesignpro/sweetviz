# Changelog

#### 1.0beta5 - 2020-07-27
- **Fixed:** indexing issues that were causing warnings and report inconsistencies
- **Fixed:** selection issues in the reports

#### 1.0beta4 - 2020-07-23
- **Added:** __version__and other metadata
- **Fixed:** "KeyError" crash
- **Fixed:** error for coercion of boolean series to categorical
- **Enhanced:** error reporting output for type coercions

#### 1.0beta3 - BETA START - 2020-07-19
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

#### 1.0alpha6 - ALPHA START - 2020-06-08
- **Fixed:** forcing feature names to be strings, to avoid crashing if numerical (#9)
- **Improved:** error message in case of mixed type feature (#3)
- **Added:** CHANGELOG.md!
