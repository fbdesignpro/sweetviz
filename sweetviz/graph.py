import matplotlib
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from io import BytesIO
import base64
import importlib_resources
from pandas.plotting import register_matplotlib_converters

from sweetviz import sv_html_formatters
from sweetviz.config import config

register_matplotlib_converters()
# matplotlib.use('SVG')
# matplotlib.use('tkagg')
plt.rcParams["svg.fonttype"] = "path"
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
    def _iter_padding_artists(axis):
        # These are the text artists most likely to get clipped when Matplotlib
        # or font metrics shift slightly across environments.
        return [
            *axis.get_xticklabels(),
            *axis.get_yticklabels(),
            axis.xaxis.get_offset_text(),
            axis.yaxis.get_offset_text(),
            axis.xaxis.label,
            axis.yaxis.label,
            axis.title,
        ]

    @staticmethod
    def _set_subplot_padding_from_pixels(figure, padding_pixels):
        figure_width_px, figure_height_px = figure.get_size_inches() * figure.dpi
        top_px, left_px, bottom_px, right_px = [float(value) for value in padding_pixels]
        figure.subplots_adjust(
            top=(1.0 - (top_px / figure_height_px)),
            left=(left_px / figure_width_px),
            bottom=(bottom_px / figure_height_px),
            right=(1.0 - (right_px / figure_width_px)),
        )

    @staticmethod
    def _normalize_padding_values(padding_value):
        if isinstance(padding_value, (int, float)):
            return [float(padding_value)] * 4
        return [float(value) for value in padding_value]

    @staticmethod
    def _get_extra_padding_for_text(figure, minimum_padding_pixels):
        minimum_padding_pixels = Graph._normalize_padding_values(minimum_padding_pixels)
        # We need one explicit draw here so Matplotlib resolves the real text
        # extents before savefig does its final render.
        figure.canvas.draw()
        renderer = figure.canvas.get_renderer()
        figure_bbox = figure.bbox
        tightest_margins = [None, None, None, None]

        for axis in figure.axes:
            for artist in Graph._iter_padding_artists(axis):
                if artist is None or not artist.get_visible():
                    continue
                if hasattr(artist, "get_text") and artist.get_text() == "":
                    continue

                try:
                    bbox = artist.get_window_extent(renderer=renderer)
                except Exception:
                    continue

                if bbox.width == 0 and bbox.height == 0:
                    continue

                current_margins = [
                    figure_bbox.y1 - bbox.y1,
                    bbox.x0 - figure_bbox.x0,
                    bbox.y0 - figure_bbox.y0,
                    figure_bbox.x1 - bbox.x1,
                ]
                for index, margin in enumerate(current_margins):
                    if tightest_margins[index] is None or margin < tightest_margins[index]:
                        tightest_margins[index] = margin

        extra_padding = []
        for required, actual in zip(minimum_padding_pixels, tightest_margins):
            actual_margin = required if actual is None else actual
            extra_padding.append(max(0.0, float(required) - actual_margin))
        return extra_padding

    @staticmethod
    def apply_pixel_padding(
        figure,
        minimum_padding_pixels,
        minimum_text_padding_pixels=4.0,
        max_passes=2,
    ):
        padding_pixels = [float(value) for value in minimum_padding_pixels]
        # Start from the historical hard-coded padding so the graphs keep the
        # same general layout, then only expand margins if rendered text would
        # otherwise touch the image edge.
        Graph._set_subplot_padding_from_pixels(figure, padding_pixels)

        for _ in range(max_passes):
            extra_padding = Graph._get_extra_padding_for_text(
                figure, minimum_text_padding_pixels
            )
            if max(extra_padding) <= 0.5:
                break
            padding_pixels = [
                current + extra for current, extra in zip(padding_pixels, extra_padding)
            ]
            # A second pass is usually enough once the first measured overflow
            # has been folded back into the subplot margins.
            Graph._set_subplot_padding_from_pixels(figure, padding_pixels)

        return padding_pixels

    @staticmethod
    def get_encoded_base64(figure):
        as_raw_bytes = BytesIO()
        figure.savefig(as_raw_bytes, format="png", transparent=True)
        as_raw_bytes.seek(0)
        return base64.b64encode(as_raw_bytes.read())

    @staticmethod
    # ADDED can_use_cjk, because the tighter default font is better for numeric graphs
    def set_style(style_filename_list, can_use_cjk=True):
        # WORKAROUND: createFontList deprecation in mpl >=3.2
        if hasattr(fm.fontManager, "addfont"):
            font_dirs = (Path(__file__).parent / "fonts",)
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            for font_found in font_files:
                fm.fontManager.addfont(font_found)
        else:
            font_dirs = (Path(__file__).parent / "fonts",)
            font_files = fm.findSystemFonts(fontpaths=font_dirs)
            create_font_list = getattr(fm, "createFontList", None)
            if create_font_list is None:
                raise RuntimeError(
                    "Matplotlib font manager is missing both addfont and createFontList"
                )
            font_list = create_font_list(font_files)
            fm.fontManager.ttflist.extend(font_list)
            fm.fontManager.ttflist = font_list

        styles_in_final_location = list()
        for source_name in style_filename_list:
            styles_in_final_location.append(
                Path(__file__).parent / "mpl_styles" / source_name
            )
        # fm.FontProperties(fname=graph_font_filename)

        # Apply style
        plt.style.use(styles_in_final_location)

        # NEW: support for CJK characters, apply override after setting the style
        if config["General"].getint("use_cjk_font") != 0 and can_use_cjk:
            plt.rcParams["font.family"] = "Noto Sans CJK JP"

    @staticmethod
    def format_smart(x, pos=None):
        return sv_html_formatters.fmt_smart(x)
