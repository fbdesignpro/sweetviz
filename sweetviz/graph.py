import matplotlib
import os.path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from io import BytesIO
import base64
from pkg_resources import resource_filename
from pandas.plotting import register_matplotlib_converters

from sweetviz import sv_html_formatters
from sweetviz.config import config

register_matplotlib_converters()
#matplotlib.use('SVG')
#matplotlib.use('tkagg')
plt.rcParams['svg.fonttype'] = 'path'
# plt.rcParams['svg.fonttype'] = 'none'

COLOR_TARGET_SOURCE = "#004bd1"
COLOR_TARGET_COMPARE = "#e54600"

class Graph:
    def __init__(self):
        self.index_for_css = "graph"
        # Some graphs save the underlying data
        self.data = {}
        return

    @staticmethod
    def get_encoded_base64(figure):
        as_raw_bytes = BytesIO()
        figure.savefig(as_raw_bytes, format='png', transparent=True)
        as_raw_bytes.seek(0)
        return base64.b64encode(as_raw_bytes.read())

    @staticmethod
    # ADDED can_use_cjk, because the tighter default font is better for numeric graphs
    def set_style(style_filename_list, can_use_cjk = True):
        # graph_font_filename = resource_filename(__name__, os.path.join("fonts", "Roboto-Medium.ttf"))

         # WORKAROUND: createFontList deprecation in mpl >=3.2
        if hasattr(fm.fontManager, "addfont"):
            font_dirs = [resource_filename(__name__, "fonts"), ]
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            for font_found in font_files:
                fm.fontManager.addfont(font_found)
        else:
            font_dirs = [resource_filename(__name__, "fonts"), ]
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            font_list = fm.createFontList(font_files)
            fm.fontManager.ttflist.extend(font_list)
            fm.fontManager.ttflist = font_list

        styles_in_final_location = list()
        for source_name in style_filename_list:
            styles_in_final_location.append(resource_filename(__name__, os.path.join("mpl_styles",
                                                                                     source_name)))
        # fm.FontProperties(fname=graph_font_filename)

        # Apply style
        matplotlib.style.use(styles_in_final_location)

        # NEW: support for CJK characters, apply override after setting the style
        if config["General"].getint("use_cjk_font") != 0 and can_use_cjk:
            plt.rcParams['font.family'] = 'Noto Sans CJK JP'


    @staticmethod
    def format_smart(x, pos=None):
        return sv_html_formatters.fmt_smart(x)
