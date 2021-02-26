# sweetviz public interface
# -----------------------------------------------------------------------------------
__title__ = 'sweetviz'
__version__ = "2.0.9"
__author__ = "Francois Bertrand"
__license__ = 'MIT'

# These are the main API functions
from sweetviz.sv_public import analyze, compare, compare_intra
from sweetviz.feature_config import FeatureConfig

# This is the main report class; holds the report data
# and is used to output the final report
from sweetviz.dataframe_report import DataframeReport

# This is the config_parser, use to customize settings
from sweetviz.config import config as config_parser
