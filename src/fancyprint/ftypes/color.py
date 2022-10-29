#######################
# IMPORTING LIBRARIES #
#######################
from dataclasses import dataclass
from colorama import Fore


#########
# ENUMS #
#########
@dataclass
class Color:
    """The Color enum contains all possible colors that can be used in fancy print!"""

    # MAIN COLORS
    WHITE = Fore.WHITE
    RED = Fore.RED
    YELLOW = Fore.YELLOW
    GREEN = Fore.GREEN
    CYAN = Fore.CYAN
    BLUE = Fore.BLUE
    BLACK = Fore.BLACK
    MAGENTA = Fore.MAGENTA

    # LIGHT VERSIONS
    DIM_WHITE = Fore.LIGHTWHITE_EX
    LIGHT_RED = Fore.RED
    LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    LIGHT_CYAN = Fore.LIGHTCYAN_EX
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    LIGHT_BLACK = Fore.LIGHTBLACK_EX
    LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX

    # TAGS
    tag_map = {
        # MAIN COLORS
        "w": WHITE,
        "r": RED,
        "y": YELLOW,
        "g": GREEN,
        "c": CYAN,
        "b": BLUE,
        "bl": BLACK,
        "m": MAGENTA,
        # Uncomment when solution for this found
        # # LIGHT VERSIONS
        # "lw": DIM_WHITE,
        # "lr": RED,
        # "ly": LIGHT_YELLOW,
        # "lg": LIGHT_GREEN,
        # "lc": LIGHT_CYAN,
        # "lb": LIGHT_BLUE,
        # "lbl": LIGHT_BLACK,
        # "lm": LIGHT_MAGENTA,
    }

    # OTHER
    COLOR_CODE_LENGTH = 5
