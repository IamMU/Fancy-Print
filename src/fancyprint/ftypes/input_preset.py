#######################
# IMPORTING LIBRARIES #
#######################
from dataclasses import dataclass
from .color import Color
from .separator_preset import SeparatorPreset


################
# Data Classes #
################
@dataclass
class InputPreset:
    """The separator preset data class is used to customize the input function"""
    ##############
    # SEPARATORS #
    ##############
    separator_preset: SeparatorPreset = SeparatorPreset()

    #############
    # LEFT SIDE #
    #############
    delimiter_left: str = "|"
    delimiter_left_color: Color = Color.CYAN

    delimiter_left_prompt_separator_left: str = "-"
    delimiter_left_prompt_separator_left_color: Color = Color.CYAN

    delimiter_left_prompt_separator_right: str = "-"
    delimiter_left_prompt_separator_right_color: Color = Color.CYAN

    input_separator_left: str = ">"
    input_separator_left_color: Color = Color.RED

    ##############
    # INPUT TEXT #
    ##############
    input_text_color: Color = Color.MAGENTA
