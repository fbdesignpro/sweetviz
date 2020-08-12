from decimal import Decimal


def fmt_int_commas(value: float) -> str:
    return f"{value:,}"


def fmt_int_limit(value: float) -> str:
    # Use commas until 1 million, then "12.5M" etc.
    if value is None:
        # Support for empty fields
        return "---"
    if value > 999999:
        return f"{value/1000000:.1f}M"
    return f"{value:,}"


def fmt_percent_parentheses(value: float) -> str:
    # This returns the percentage as a rounded number. 100% is only used if truly 100%
    rounded = round(value)
    if rounded == 100 and value != 100.0:
        rounded = 99
    return f"({rounded:.0f}%)"


def fmt_percent(value: float) -> str:
    # This returns the percentage as a rounded number. 100% is only used if truly 100%
    if value is None:
        # Support for empty fields
        return "---"
    rounded = round(value)
    if rounded == 100 and value != 100.0:
        rounded = 99
    return f"{rounded:.0f}%"


def fmt_percent1d(value: float) -> str:
    return f"{value:.1f}%"


def fmt_smart(value: float) -> str:
    # Mainly used to shall average, etc. in the second column of numerical summary
    # Keep to ~5 display digits based on scale of input number
    absolute = abs(value)

    if absolute == 0.0:
        return "0.00"
    elif absolute < 0.001:
        return f"{Decimal(value):.2e}"
    elif absolute < 0.1:
        return f"{value:.3f}"
    elif absolute < 1.0:
        return f"{value:.3f}"
    elif absolute < 10:
        return f"{value:.2f}"
    elif absolute < 100:
        return f"{value:,.1f}"
    elif absolute < 99999:
        return f"{value:,.0f}"
    elif absolute < 999999:
        return f"{value/1000.0:.0f}k"
    elif absolute < 999999999:
        return f"{value / 1000000.0:.1f}M"
    elif absolute < 999999999999:
        return f"{value/1000000000.0:.1f}B"
    else:
        return f"{value/1000000000000.0:.1f}T"

def fmt_RAM(value: float) -> str:
    # Keep to ~5 display digits based on scale of input number
    absolute = abs(value)
    if absolute < 1000:
        return f"{value:,.0f}b"
    elif absolute < 1000000:
        return f"{value/1000.0:,.1f} kb"
    elif absolute < 1000000000:
        return f"{value/1000000.0:,.1f} MB"
    else:
        return f"{value/1000000000.0:.1f} GB"

def fmt_smart_range(value: float, range: float) -> str:
    # Keep to ~5 display digits based on scale given by range number
    absolute_range = abs(range)
    if absolute_range == 0.0:
        return "0.00"
    elif absolute_range < 0.001:
        return f"{value:.5f}"
    elif absolute_range < 0.1:
        return f"{value:.3f}"
    elif absolute_range < 1.0:
        return f"{value:.3f}"
    elif absolute_range < 10:
        return f"{value:.2f}"
    elif absolute_range < 100:
        return f"{value:,.1f}"
    elif absolute_range < 99999:
        return f"{value:,.0f}"
    elif absolute_range < 999999:
        return f"{value / 1000.0:.0f}k"
    elif absolute_range < 999999999:
        return f"{value / 1000000.0:.1f}M"
    elif absolute_range < 999999999999:
        return f"{value / 1000000000.0:.1f}B"
    else :
        return f"{value / 1000000000000.0:.1f}T"

def fmt_smart_range_tight(value: float, range: float) -> str:
    # Used for graph labels
    # Keep to ~4 display digits based on scale given by range number
    absolute_range = abs(range)
    if absolute_range < 1.0:
        return f"{value:.3f}"
    elif absolute_range < 10:
        return f"{value:.2f}"
    elif absolute_range < 100:
        return f"{value:,.1f}"
    elif absolute_range < 4999:
        return f"{value:,.0f}"
    elif absolute_range < 99999:
        return f"{value / 1000.0:,.1f}k"
    elif absolute_range < 999999:
        return f"{value / 1000.0:.0f}k"
    elif absolute_range < 99999999:
        # 99.9M
        return f"{value / 1000000.0:.1f}M"
    elif absolute_range < 999999999:
        return f"{value / 1000000.0:.0f}M"
    elif absolute_range < 99999999999:
        # 99.9B
        return f"{value / 1000000000.0:.1f}B"
    elif absolute_range < 999999999999:
        return f"{value / 1000000000.0:.0f}B"
    else :
        return f"{value / 1000000000000.0:.1f}T"

