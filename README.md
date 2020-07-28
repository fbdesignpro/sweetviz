![v](https://img.shields.io/badge/version-1.0beta5-blue) ![v](https://img.shields.io/badge/updated-27%20Jul%202020-green)

![Sweetviz Logo](http://cooltiming.com/SV/logo.png) 

Sweetviz is an open source Python library that generates beautiful, high-density visualizations to kickstart EDA (Exploratory Data Analysis) with a single line of code. Output is a fully self-contained HTML application.

The system is built around quickly **visualizing target values** and **comparing datasets**. Its goal is to help quick analysis of target characteristics, training vs testing data, and other such data characterization tasks. 

**Note: Sweetviz is in the BETA TESTING PHASE.** Core functionality is complete, please let me know if you run into any data, compatibility or install issues! Thank you for [reporting any BUGS in the issue tracking system here](https://github.com/fbdesignpro/sweetviz/issues), and I welcome your feedback and questions on usage/features [in our Discourse server (you should be able to log in with your Github account!)](https://sweetviz.fbdesignpro.com).

## Examples
- [Example report from the Titanic dataset HERE](http://cooltiming.com/SWEETVIZ_REPORT.html)
- [Article describing features in depth HERE](https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34)


# Features
![Features](http://cooltiming.com/SV/features.png)
- Target analysis
  - How target values (boolean or numerical) relate to other features
- Visualize and compare
  - Distinct datasets (e.g. training vs test data)
  - Intra-set characteristics (e.g. male versus female)
- Mixed-type associations
  - Sweetviz integrates associations for numerical (Pearson's correlation), categorical (uncertainty coefficient) and categorical-numerical (correlation ratio) datatypes seamlessly, to provide maximum information for all data types.
- Type inference: automatically detects numerical, categorical and text features, with optional manual overrides 
- Summary information: 
  - Type, unique values, missing values, duplicate rows, most frequent values
  - Numerical analysis: 
    - min/max/range, quartiles, mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness

# Upgrading
Some people have experienced mixed results behavior upgrading through `pip`. To update to the latest from an existing install, it is recommended to `pip uninstall sweetviz` first, Then simply install.

# Installation
Sweetviz currently supports Python 3.6+ and Pandas 0.25.3+. Reports are output using the base "os" module, so custom environments such as Google Colab which require custom file operations are not yet supported, although I am looking into a solution. 
## Using pip
The best way to install sweetviz (other than from source) is to use pip:
```
pip install sweetviz
```
# Basic Usage
Create a `DataframeReport` object, then use a `show_xxx` function to render the report. 

**Note: Currently the only rendering supported is to a standalone HTML file, using a "widescreen" aspect ratio (i.e. 1080p resolution or wider).** Please let me know of formats/resolutions you would like to be supported in our Discourse Forum.

There are 3 main functions for creating reports:
- analyze(...)
- compare(...)
- compare_intra(...)

## Analyzing a single dataframe (and its optional target feature)
To analyze a single dataframe, simply use the `analyze(...)` function, then the `show_html(...)` function:
```
import sweetviz as sv

my_report = sv.analyze(my_dataframe)
my_report.show_html() # Default arguments will generate to "SWEETVIZ_REPORT.html"
```
When run, this will output a 1080p widescreen html app in your default browser:
![Widescreen demo](http://cooltiming.com/SV/demo_wide.png)
### Optional arguments
The `analyze()` function can take multiple other arguments:
```
analyze(source: Union[pd.DataFrame, Tuple[pd.DataFrame, str]],
            target_feat: str = None,
            feat_cfg: FeatureConfig = None,
            pairwise_analysis: str = 'auto'):
```
- **source:** Either the data frame (as in the example) or a tuple containing the data frame and a name to show in the report. 
e.g. `my_df` or `[my_df, "Training"]`
- **target_feat:** A string representing the name of the feature to be marked as "target". *Only BOOLEAN and NUMERICAL features can be targets for now.*
- **feat_cfg:** A FeatureConfig object representing features to be skipped, or to be forced a certain type in the analysis. The arguments can either be a single string or list of strings. Parameters are `skip`, `force_cat`, `force_num` and `force_text`. The "force_" arguments override the built-in type detection. They can be constructed as follows:
```
feature_config = sv.FeatureConfig(skip="PassengerId", force_text=["Age"])
```
- **pairwise_analysis:** Correlations and other associations can take quadratic time (n^2) to complete. The default setting ("auto") will run without warning until a data set contains "association_auto_threshold" features. Past that threshold, you need to explicitly pass the parameter `pairwise_analysis="on"` (or `="off"`) since processing that many features would take a long time. This parameter also covers the generation of the association graphs (based on Drazen Zaric's concept):
![Pairwise sample](http://cooltiming.com/SV/pairwise.png)

## Comparing two dataframes (e.g. Test vs Training sets)
To compare two data sets, simply use the `compare()` function. Its parameters are the same as `analyze()`, except with an inserted second parameter to cover the comparison dataframe. It is recommended to use the [dataframe, "name"] format of parameters to better differentiate between the base and compared dataframes. (e.g. `[my_df, "Train"]` vs `my_df`)
```
my_report = sv.compare([my_dataframe, "Training Data"], [test_df, "Test Data"], "Survived", feature_config)
```
## Comparing two subsets of the same dataframe (e.g. Male vs Female)
Another way to get great insights is to use the comparison functionality to split your dataset into 2 sub-populations.

Support for this is built in through the `compare_intra()` function. This function takes a boolean series as one of the arguments, as well as an explicit "name" tuple for naming the (true, false) resulting datasets. Note that internally, this creates 2 separate dataframes to represent each resulting group. As such, it is more of a shorthand function of doing such processing manually.
```
my_report = sv.compare_intra(my_dataframe, my_dataframe["Sex"] == "male", ["Male", "Female"], feature_config)
```
# Config file
The package contains an INI file for configuration. You can override any setting by providing your own then calling this before creating a report:
```
sv.config_parser.read("Override.ini")
```
You can look into the file `sweetviz_defaults.ini` for what can be overriden (warning: much of it is a work in progress and not well documented). One example is to remove the logo from the report, so it may be used more readily in a business setting. You would create your own `Override.ini` and put the following lines:
```
[Layout]
show_logo = 0
``` 
# Contribute
This is my first open-source project! I built it to be the most useful tool possible and help as many people as possible with their data science work. If it is useful to you, your contribution is more than welcome and can take many forms:
### 1. Spread the word!
A STAR here on GitHub, and a Twitter or Instagram post are the easiest contribution and can potentially help grow this project tremendously! If you find this project useful, these quick actions from you would mean a lot and could go a long way. 

Kaggle notebooks/posts, Medium articles, YouTube video tutorials and other content take more time but will help all the more!

### 2. Report bugs & issues
I expect there to be many quirks once the project is used by more and more people with a variety of new (& "unclean") data. If you found a bug, please [open a new issue here](https://github.com/fbdesignpro/sweetviz/issues).

### 3. Suggest and discuss usage/features
To make Sweetviz as useful as possible we need to hear what you would like it to do, or what it could do better! [Head on to our Discourse server and post your suggestions there; no login required!](https://sweetviz.fbdesignpro.com).

### 4. Contribute to the development
I definitely welcome the help I can get on this project, simply get in touch on the issue tracker and/or our Discourse forum. 

Please note that after a hectic development period, the code itself right now needs a bit of cleanup. :)

# Special thanks & related materials
I want Sweetviz to be a hub of the best of what's out there, a way to get the most valuable information and visualization, without reinventing the wheel.

As such, I want to point some of those great resources that were inspiring and integrated into Sweetviz:
- [Pandas-Profiling](https://github.com/pandas-profiling/pandas-profiling) was the original inspiration for this project. Some of its type-detection code was included in Sweetviz.
- [Shaked Zychlinski: The Search for Categorical Correlation](https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9) is a great article about different types of variable interactions that was the basis of that analysis in Sweetviz.
- [Drazen Zaric: Better Heatmaps and Correlation Matrix Plots in Python](https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec) was the basis for our association graphs.

