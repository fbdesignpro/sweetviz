import configparser
import os


try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources


config = configparser.ConfigParser()
# print("Config: " + os.path.abspath('sweetviz_defaults.ini'))
the_open = pkg_resources.open_text("sweetviz", 'sweetviz_defaults.ini')
config.read_file(the_open)
the_open.close()
# config.read_file(open('sweetviz_defaults.ini'))

