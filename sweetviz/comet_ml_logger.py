try:
    from comet_ml import Experiment

    comet_installed = True
except:
    comet_installed = False


class CometLogger():
    def __init__(self):
        global comet_installed
        self._logging = False
        if comet_installed:
            try:
                self._experiment = Experiment(auto_metric_logging=False,
                                              display_summary_level=0)
                self._experiment.log_other("Created from", "sweetviz!")
                self._logging = True
            except:
                print("ERROR: comet_ml is installed, but not configured properly (e.g. check API key setup). HTML reports will not be uploaded.")

    def log_html(self, html_content):
        if self._logging:
            try:
                self._experiment.log_html(html_content)
            except:
                print("comet_ml.log_html(): error occurred during call to log_html().")
        else:
            print("comet_ml.log_html(): comet_ml is not installed or otherwise ready for logging.")

    def end(self):
        if self._logging:
            try:
                self._experiment.end()
            except:
                print("comet_ml.end(): error occurred during call to end().")
        else:
            print("comet_ml.end(): comet_ml is not installed or otherwise ready.")

