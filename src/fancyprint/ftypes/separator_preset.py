#######################
# IMPORTING LIBRARIES #
#######################
from dataclasses import dataclass
from .color import Color


################
# Data Classes #
################
@dataclass
class SeparatorPreset:
    """The separator preset data class is used to customize the separator"""

    # Delimiters
    delimiter_left: str = "|"
    delimiter_left_color: Color = Color.CYAN

    delimiter_right: str = "|"
    delimiter_right_color: Color = Color.CYAN

    delimiter_space_amount: int = 0
    delimiter_space_symbol: str = " "

    # Separator
    separator_symbol: str = "-"
    separator_color: Color = Color.MAGENTA
