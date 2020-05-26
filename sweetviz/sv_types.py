from enum import Enum, unique
import pandas as pd


# Adding spaces to avoid collisions: this should NEVER be in a dataset :)
OTHERS_GROUPED = "     (Other)"

@unique
class FeatureType(Enum):
    TYPE_CAT = "CAT"
    TYPE_BOOL = "BOOL"
    TYPE_NUM = "NUM"
    TYPE_TEXT = "TEXT"
    TYPE_UNSUPPORTED = "UNSUPPORTED"
    TYPE_UNKNOWN = "UNKNOWN"
    TYPE_SKIPPED = "SKIPPED"


class NumWithPercent:
    def __init__(self, number, total_for_percentage):
        # Meant to be very flexible, negative numbers are allowed etc.
        if total_for_percentage == 0:
            self.number = None
            self.perc = None
            # raise ValueError
        else:
            self.number = number
            self.perc = 100.0 * number / total_for_percentage

    def __int__(self):
        return self.number

    def __float__(self):
        return float(self.number)

    def __repr__(self):
        if self.number is not None:
            return f"{self.number} ({self.perc:.2f}%)"
        else:
            return "[INVALID]"

class FeatureToProcess:
    def __init__(self, order: int, source: pd.Series, compare=None, source_target=None,
                 compare_target=None, predetermined_type: FeatureType = None,
                 predetermined_type_target: FeatureType = None):
        self.order = order

        self.source = source
        self.source_counts = None
        self.source_target  = source_target

        self.compare = compare
        self.compare_counts = None
        self.compare_target = compare_target

        if predetermined_type:
            self.predetermined_type = predetermined_type
        else:
            self.predetermined_type = FeatureType.TYPE_UNKNOWN

        # Validate TARGET type
        if predetermined_type_target:
            if predetermined_type_target not in (FeatureType.TYPE_BOOL,
                                                 FeatureType.TYPE_NUM):
                raise ValueError
            self.predetermined_type_target = predetermined_type_target
        else:
            self.predetermined_type_target = FeatureType.TYPE_UNKNOWN

    def is_target(self):
        return self.order == -1

    def __repr__(self):
        out = str()
        if self.source is not None:
            out = out + f"Src: {self.source.name} "
            if self.source_target is not None:
                out = out + f"(Target: {self.source_target.name}) "
        if self.compare is not None:
            out = out + f"[WITH COMPARISON]"
        return out
