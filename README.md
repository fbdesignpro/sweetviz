![v](https://img.shields.io/badge/version-2.3.1-blue) ![v](https://img.shields.io/badge/updated-November%2029,%20%202023-green)

### UPDATE (November 2023) -  Version 2.3.0: Verbosity parameter added, long-standing issues fixed

---
![Sweetviz Logo](http://cooltiming.com/SV/logo.png) 

_In-depth EDA **(target analysis, comparison, feature analysis, correlation)** in two lines of code!_

![Features](http://cooltiming.com/SV/features.png)

Sweetviz is an open-source Python library that generates beautiful, high-density visualizations to kickstart EDA (Exploratory Data Analysis) with just two lines of code. Output is a fully self-contained HTML application.

The system is built around quickly **visualizing target values** and **comparing datasets**. Its goal is to help quick analysis of target characteristics, training vs testing data, and other such data characterization tasks. 

Usage and parameters are described below, [you can also find an article describing its features in depth and see examples in action HERE](https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34).

**Sweetviz development is still ongoing!** Please let me know if you run into any data, compatibility or install issues! Thank you for [reporting any BUGS in the issue tracking system here](https://github.com/fbdesignpro/sweetviz/issues), and I welcome your feedback and questions on usage/features [in the brand-new GitHub "Discussions" tab right here!](https://github.com/fbdesignpro/sweetviz/discussions).

## Examples & mentions
[**Example HTML report** using the Titanic dataset](http://cooltiming.com/SWEETVIZ_REPORT.html)

[**Example Notebook w/docs** on Colab (Jupyter/other notebooks should also work)](https://colab.research.google.com/drive/1-md6YEwcVGWVnQWTBirQSYQYgdNoeSWg?usp=sharing)

[**Medium Article** describing its features in depth](https://towardsdatascience.com/powerful-eda-exploratory-data-analysis-in-just-two-lines-of-code-using-sweetviz-6c943d32f34)

KD Nugget articles:
[![KDNuggets](https://www.kdnuggets.com/images/tkb-2102-g.png)](https://www.kdnuggets.com/2021/02/powerful-exploratory-data-analysis-sweetviz.html) [![KDNuggets](https://www.kdnuggets.com/images/tkb-2103-g.png)](https://www.kdnuggets.com/2021/03/know-your-data-much-faster-sweetviz-python-library.html)

# Features
- **Target analysis** 
  - Shows how a target value (e.g. "Survived" in the Titanic dataset) relates to other features
- **Visualize and compare**
  - Distinct datasets (e.g. training vs test data)
  - Intra-set characteristics (e.g. male versus female)
- **Mixed-type associations**
  - Sweetviz integrates associations for numerical (Pearson's correlation), categorical (uncertainty coefficient) and categorical-numerical (correlation ratio) datatypes seamlessly, to provide maximum information for all data types.
- **Type inference**
  - Automatically detects numerical, categorical and text features, with optional manual overrides 
- **Summary information** 
  - Type, unique values, missing values, duplicate rows, most frequent values
  - Numerical analysis: 
    - min/max/range, quartiles, mean, mode, standard deviation, sum, median absolute deviation, coefficient of variation, kurtosis, skewness

## New & notable
- Version 2.2: Big compatibility update for python 3.7+ and numpy versions
- Version 2.1: **Comet.ml** support
- Version 2.0: **Jupyter, Colab & other notebook** support, report **scaling & vertical layout**  

_(see below for docs on these features)_

# Upgrading
Some people have experienced mixed results behavior upgrading through `pip`. To update to the latest from an existing install, it is recommended to `pip uninstall sweetviz` first, then simply install.

# Installation
Sweetviz currently supports Python 3.6+ and Pandas 0.25.3+. Reports are output using the base "os" module, so custom environments such as Google Colab which require custom file operations are not yet supported, although I am looking into a solution. 
## Using pip
The best way to install sweetviz (other than from source) is to use pip:
```
pip install sweetviz
```
#### Installation issues & fixes
In some rare cases, users have reported errors such as `ModuleNotFoundError: No module named 'sweetviz'` and `AttributeError: module 'sweetviz' has no attribute 'analyze'`.
In those cases, we suggest the following:
- Make sure none of your scripts are named `sweetviz.py`, as that interferes with the library itself. Delete or rename that script (and any associated `.pyc` files), and try again.
- Try uninstalling the library using `pip uninstall sweetviz`, then reinstalling
- The issue may stem from using multiple versions of Python, or from OS permissions. The following Stack Overflow articles have resolved many of these issues reported: [Article 1](https://stackoverflow.com/questions/32680081/importerror-after-successful-pip-installation/32680082), [Article 2](https://stackoverflow.com/questions/14295680/unable-to-import-a-module-that-is-definitely-installed), [Article 3](https://stackoverflow.com/questions/44528638/after-pip-successful-installed-modulenotfounderror) 
- If all else fails, post a bug issue [here on github](https://github.com/fbdesignpro/sweetviz/issues). Thank you for taking the time, it may help resolve the issue for you and everyone else!
# Basic Usage
Creating a report is a quick 2-line process:
1. Create a `DataframeReport` object using one of: `analyze()`, `compare()` or `compare_intra()`
2. Use a `show_xxx()` function to render the report. You can now use either **html** or **notebook** report options, as well as scaling: (more info on these options below)

![Report_Show_Options](http://cooltiming.com/SV/Layout-Anim3.gif) 

## Step 1: Create the report
There are 3 main functions for creating reports:
- analyze(...)
- compare(...)
- compare_intra(...)

#### Analyzing a single dataframe (and its optional target feature)
To analyze a single dataframe, simply use the `analyze(...)` function, then the `show_html(...)` function:
```
import sweetviz as sv

my_report = sv.analyze(my_dataframe)
my_report.show_html() # Default arguments will generate to "SWEETVIZ_REPORT.html"
```
When run, this will output a 1080p widescreen html app in your default browser:
![Widescreen demo](http://cooltiming.com/SV/demo_wide.png)
##### Optional arguments
The `analyze()` function can take multiple other arguments:
```
analyze(source: Union[pd.DataFrame, Tuple[pd.DataFrame, str]],
            target_feat: str = None,
            feat_cfg: FeatureConfig = None,
            pairwise_analysis: str = 'auto',
            verbosity: str = 'default'):
```
- **source:** Either the data frame (as in the example) or a tuple containing the data frame and a name to show in the report. 
e.g. `my_df` or `[my_df, "Training"]`
- **target_feat:** A string representing the name of the feature to be marked as "target". *Only BOOLEAN and NUMERICAL features can be targets for now.*
- **feat_cfg:** A FeatureConfig object representing features to be skipped, or to be forced a certain type in the analysis. The arguments can either be a single string or list of strings. Parameters are `skip`, `force_cat`, `force_num` and `force_text`. The "force_" arguments override the built-in type detection. They can be constructed as follows:
```
feature_config = sv.FeatureConfig(skip="PassengerId", force_text=["Age"])
```
- **verbosity:** **[NEW]** Can be set to `full`, `progress_only` (to only display the progress bar but not report generation messages) and `off` (fully quiet, except for errors or warnings). Default  verbosity can also be set in the INI override, under the "General" heading (see "The Config file" section below for details).
- **pairwise_analysis:** Correlations and other associations can take quadratic time (n^2) to complete. The default setting ("auto") will run without warning until a data set contains "association_auto_threshold" features. Past that threshold, you need to explicitly pass the parameter `pairwise_analysis="on"` (or `="off"`) since processing that many features would take a long time. This parameter also covers the generation of the association graphs (based on [Drazen Zaric's concept](https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec)):

![Pairwise sample](http://cooltiming.com/SV/pairwise.png)

#### Comparing two dataframes (e.g. Test vs Training sets)
To compare two data sets, simply use the `compare()` function. Its parameters are the same as `analyze()`, except with an inserted second parameter to cover the comparison dataframe. It is recommended to use the [dataframe, "name"] format of parameters to better differentiate between the base and compared dataframes. (e.g. `[my_df, "Train"]` vs `my_df`)
```
my_report = sv.compare([my_dataframe, "Training Data"], [test_df, "Test Data"], "Survived", feature_config)
```
#### Comparing two subsets of the same dataframe (e.g. Male vs Female)
Another way to get great insights is to use the comparison functionality to split your dataset into 2 sub-populations.

Support for this is built in through the `compare_intra()` function. This function takes a boolean series as one of the arguments, as well as an explicit "name" tuple for naming the (true, false) resulting datasets. Note that internally, this creates 2 separate dataframes to represent each resulting group. As such, it is more of a shorthand function of doing such processing manually.
```
my_report = sv.compare_intra(my_dataframe, my_dataframe["Sex"] == "male", ["Male", "Female"], "Survived", feature_config)
```
## Step 2: Show the report
Once you have created your report object (e.g. `my_report` in the examples above), simply pass it into one of the two `show' functions:

### show_html()
```
show_html(  filepath='SWEETVIZ_REPORT.html', 
            open_browser=True, 
            layout='widescreen', 
            scale=None)
```            
**show_html(...)** will create and save an HTML report at the given file path. There are options for:
- **layout**: Either `'widescreen'` or `'vertical'`. The widescreen layout displays details on the right side of the screen, as the mouse goes over each feature. The new (as of 2.0) vertical layout is more compact horizontally and enables expanding each detail area upon clicking.
- **scale**: Use a floating-point number (e.g. `scale = 0.8` or `None`) to scale the entire report. This is very useful to fit reports to any output.
- **open_browser**: Enables the automatic opening of a web browser to show the report. Since under some circumstances this is not desired (or causes issues with some IDE's), you can disable it here.

### show_notebook()
```
show_notebook(  w=None, 
                h=None, 
                scale=None,
                layout='widescreen',
                filepath=None,
                file_layout=None,
                file_scale=None)
```            
**show_notebook(...)** is new as of 2.0 and will embed an IFRAME element showing the report right inside a notebook (e.g. Jupyter, Google Colab, etc.). 

Note that since notebooks are generally a more constrained visual environment, it is probably a good idea to use custom width/height/scale values (`w`, `h`, `scale`) and even **set custom default values in an INI override** (see below). The options are:
- **w** (width): Sets the width of the output _window_ for the report (the full report may not fit; use `layout` and/or `scale` for the report itself). Can be as a percentage string (`w="100%"`) or number of pixels (`w=900`).
- **h** (height): Sets the height of the output _window_ for the report. Can be as a number of pixels (`h=700`) or "Full" to stretch the window to be as tall as all the features (`h="Full"`).
- **scale**: Same as for `show_html()`, above.
- **layout**: Same as for `show_html()`, above.
- **filepath**: An OPTIONAL output HTML report.
- **file_layout**: Layout for the OPTIONAL file output ONLY (same as `layout` for `show_html()`, above)
- **file_scale**: Scale for the OPTIONAL file output ONLY (same as `scale` for `show_html()`, above)
# Customizing defaults: the Config file
The package contains an INI file for configuration. You can override any setting by providing your own then calling this before creating a report:
```
sv.config_parser.read("Override.ini")
```
**IMPORTANT #1:** it is best to load overrides **before any other command**, as many of the INI options are used in the report generation.  

**IMPORTANT #2:** always **put the header line** (e.g. `[General]`) before a set of values in your override INI file, **otherwise your settings will be ignored**. See examples below. If setting multiple values, only include the `[General]` line once.


### Most useful config overrides
You can look into the file `sweetviz_defaults.ini` for what can be overriden (warning: much of it is a work in progress and not well documented), but the most useful overrides are as follows.

#### Default report layout, size
Override any of these (by putting them in your own INI, again do not forget the header), to avoid having to set them every time you do a "show" command:

**Important**: note the double '%' if specifying a percentage
```
[Output_Defaults]
html_layout = widescreen
html_scale = 1.0
notebook_layout = vertical
notebook_scale = 0.9
notebook_width = 100%%
notebook_height = 700
```

##### Chinese, Japanse, Korean (CJK) character support
```
[General]
use_cjk_font = 1 
```
*\*If setting multiple values for `[general]` only include the `[General]` line once*.

Will switch the font in the graphs to use a CJK-compatible font. Although this font is not as compact, it will get rid of any warnings and "unknown character" symbols for these languages.
##### Remove Sweetviz logo
```
[Layout]
show_logo = 0
```
Will remove the Sweetviz logo from the top of the page. 

##### Set default verbosity level
```
[General]
default_verbosity = off 
```
*\*If setting multiple values for `[general]` only include the `[General]` line once*.

Can be set to `full`, `progress_only` (to only display the progress bar but not report generation messages) and `off` (fully quiet, except for errors or warnings).

# Correlation/Association analysis
A major source of insight and unique feature of Sweetviz' associations graph and analysis is that **it unifies in a single graph** (and detail views):
 - Numerical correlation (between numerical features)
 - Uncertainty coefficient (for categorical-categorical)
 - Correlation ratio (for categorical-numerical)
![Pairwise sample](http://cooltiming.com/SV/pairwise.png)

 Squares represent categorical-featured-related variables and circles represent numerical-numerical correlations. Note that the trivial diagonal is left empty, for clarity.
 
IMPORTANT: categorical-categorical associations (provided by the SQUARES showing the uncertainty coefficient) are ASSYMMETRICAL, meaning that each row represents **how much the row title (on the left) gives information on each column**. _For example, "Sex", "Pclass" and "Fare" are the elements that give the most information on "Survived"._ 

For the Titanic dataset, this information is rather symmetrical but it is not always the case!

Correlations are also displayed in the detail section of each feature, with the target value highlighted when applicable. e.g.:

![Associations detail](http://cooltiming.com/SV/associations_detail.PNG)

Finally, it is worth noting these correlation/association methods shouldn’t be taken as gospel as they make some assumptions on the underlying distribution of data and relationships. However they can be a _very_ useful starting point.

# Comet.ml integration
As of 2.1, Sweetviz now fully integrates [Comet.ml](https://www.comet.ml). This means Sweetviz will **automatically log any reports generated** using `show_html()` and `show_notebook()` to your workspace, as long as your API key is set up correctly in your environment.

Additionally, you can also use the new function `report.log_comet(experiment_object)` to explicitly upload a report for a given experiment to your workspace.

You can see an example of a [Colab notebook](https://colab.research.google.com/drive/1SK1I-gU6nLchesbMtFD9ZuzJHyzleFAr?usp=sharing) to generate the report, and its corresponding report in a [Comet.ml workspace](https://www.comet.ml/fbdesignpro/sweetviz-comet/d005158117c24924b07476887cd5ddfa?experiment-tab=html).

## Comet report parameters
You can customize how the Sweetviz report looks in your Comet workspace by overriding the `[comet_ml_defaults]` section of configuration file. See above for more information on using the INI override.

You can choose to use either the `widescreen` (horizontal) or `vertical` layouts, as well as set your preferred scale, by putting the following in your override INI file:
```
[comet_ml_defaults]
html_layout = vertical
html_scale = 0.85
```

# Troubleshooting / FAQ
- **Installation issues**

Please see the "Installation issues & fixes" section at the top of this document
- **Asian characters, "RuntimeWarning: Glyph ### missing from current font"**

See section above regarding CJK characters support. If you find the need for additional character types, definitely [post a request in the issue tracking system.](https://github.com/fbdesignpro/sweetviz/issues)

- **...any other issues**

Development is ongoing so absolutely feel free to report any issues and/or suggestions [in the issue tracking system here](https://github.com/fbdesignpro/sweetviz/issues) or [in our forum (you should be able to log in with your Github account!)](https://sweetviz.fbdesignpro.com)

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
### Contributors
**A very special thanks to everyone who have contributed on Github, through reports, feedback and commits!** I want to give a special shout out to **Frank Male** who has been of tremendous help for fixing issues and setting up the new build pipeline for 2.2.0.

[![Contributors](https://contrib.rocks/image?repo=fbdesignpro/sweetviz)](https://github.com/fbdesignpro/sweetviz/graphs/contributors)

Made with [contrib.rocks](https://contrib.rocks).
### Related materials
I want Sweetviz to be a hub of the best of what's out there, a way to get the most valuable information and visualization, without reinventing the wheel.

As such, I want to point some of those great resources that were inspiring and integrated into Sweetviz:
- [Pandas-Profiling](https://github.com/pandas-profiling/pandas-profiling) was the original inspiration for this project. Some of its type-detection code was included in Sweetviz.
- [Shaked Zychlinski: The Search for Categorical Correlation](https://towardsdatascience.com/the-search-for-categorical-correlation-a1cf7f1888c9) is a great article about different types of variable interactions that was the basis of that analysis in Sweetviz.
- [Drazen Zaric: Better Heatmaps and Correlation Matrix Plots in Python](https://towardsdatascience.com/better-heatmaps-and-correlation-matrix-plots-in-python-41445d0f2bec) was the basis for our association graphs.

