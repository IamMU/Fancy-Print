from enum import Enum
from colorama import Fore

class LogLevel(Enum):
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    SUCCESS = "SUCCESS"

class LogColor(Enum):
    INFO = Fore.GREEN
    WARN = Fore.YELLOW
    ERROR = Fore.RED
    SUCCESS = Fore.CYAN

class Align(Enum):
    LEFT = "left"
    CENTER = "center"
    RIGHT = "right"

# might be done better
COLORS = {
    "cyan": Fore.CYAN,
    "c": Fore.CYAN,
    "white": Fore.WHITE,
    "w": Fore.WHITE,
    "magenta": Fore.MAGENTA,
    "m": Fore.MAGENTA,
    "yellow": Fore.YELLOW,
    "y": Fore.YELLOW,
    "blue": Fore.BLUE,
    "b": Fore.BLUE,
    "red": Fore.RED,
    "r": Fore.RED,
    "green": Fore.GREEN,
    "g": Fore.GREEN,
    "black": Fore.BLACK,
    "bl": Fore.BLACK,
    "lightcyan": Fore.LIGHTCYAN_EX,
    "lc": Fore.LIGHTCYAN_EX,
    "lightwhite": Fore.LIGHTWHITE_EX,
    "lw": Fore.LIGHTWHITE_EX,
    "lightmagenta": Fore.LIGHTMAGENTA_EX,
    "lm": Fore.LIGHTMAGENTA_EX,
    "lightyellow": Fore.LIGHTYELLOW_EX,
    "ly": Fore.LIGHTYELLOW_EX,
    "lightblue": Fore.LIGHTBLUE_EX,
    "lb": Fore.LIGHTBLUE_EX,
    "lightred": Fore.LIGHTRED_EX,
    "lr": Fore.LIGHTRED_EX,
    "lightgreen": Fore.LIGHTGREEN_EX,
    "lg": Fore.LIGHTGREEN_EX,
    "lightblack": Fore.LIGHTBLACK_EX,
    "lbl": Fore.LIGHTBLACK_EX
}
