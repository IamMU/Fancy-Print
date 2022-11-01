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

    ########
    # BACK #
    ########

    # Delimiters
    back_delimiter_left: str = "|"
    back_delimiter_left_color: Color = Color.CYAN

    back_delimiter_right: str = "|"
    back_delimiter_right_color: Color = Color.CYAN

    back_delimiter_space_amount: int = 0
    back_delimiter_space_symbol: str = " "

    # Separator
    back_separator_symbol: str = "-"
    back_separator_color: Color = Color.MAGENTA

    #########
    # FRONT #
    #########

    # Delimiters
    front_delimiter_left: str = "|"
    front_delimiter_left_color: Color = Color.CYAN

    front_delimiter_right: str = "|"
    front_delimiter_right_color: Color = Color.CYAN

    front_delimiter_space_amount: int = 0
    front_delimiter_space_symbol: str = " "

    # Separator
    front_separator_symbol: str = "-"
    front_separator_color: Color = Color.MAGENTA