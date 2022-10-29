from fancyprint.ftypes import PrinterPreset, Color
from fancyprint.printer import *

my_custom_printer_preset = PrinterPreset(
    delimiter_left="<",
    delimiter_left_color=Color.RED,

    delimiter_right=">",
    delimiter_right_color=Color.RED,

    delimiter_space_amount=10,
    delimiter_space_symbol=" ",

    hyphenation=False
)

pretty_print("Hi, this is some text", preset=my_custom_printer_preset)
