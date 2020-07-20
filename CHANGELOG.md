# Changelog

### 1.0beta2 - BETA START - 2020-07-19
##### Added
- Post-report-generation descriptive text for Jupyter/Colab
- Re-added horizontal scrollbar
- Link to check for updates in header
##### Fixed/Updated
- All-NaN columns will not crash and get added to the report (as empty text feature)
- Fixed detail tab title overflowing to 2 lines when multiple words
- Fixed progress bar resetting to 0% when reaching 100%
- Updated README
- Fixed images on Pypi
### 1.0alpha8 - 2020-07-18
##### Added
- Support for categorical Pandas data type
##### Fixed
- MANY crash and general stability/compatibility issues! The library is now much more robust with regard to supporting different data and conditions.
### 1.0alpha7 - 2020-06-09
##### Fixed
- Fixed "ValueError: index must be monotonic..." crash with some datasets (#10)
### 1.0alpha6 - ALPHA START - 2020-06-08
##### Fixed
- Forcing feature names to be strings, to avoid crashing if numerical (#9)
- Improved error message in case of mixed type feature (#3)
##### Added
- Added CHANGELOG.md!
