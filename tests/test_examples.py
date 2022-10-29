##############################################
# THIS FILE IS FOR MAKING PRACTICAL EXAMPLES #
##############################################

#######################
# IMPORTING LIBRARIES #
#######################
from fancyprint import pretty_print, separate_line
from fancyprint.ftypes import PrinterPreset, SeparatorPreset, Color

#############
# MAIN MENU #
#############
def main_menu(title: str, options: list, errors: list):
    # Local variables
    user_input = str()
    options = [(i + 1, v) for i, v in enumerate(options)]

    # Main Loop
    while not user_input == "q":
        # Print the title
        pretty_print(title)

        # Print the options
        for index, option in options:
            pretty_print(f"{index}) {option}", enable_back_separator=False, enable_front_separator=False)

        # Print a separator
        separate_line()

        # Print the errors
        for error in errors:
            pretty_print(f"<r>{error}", enable_back_separator=False)

        # Get input
        user_input = input("|-> ").lower()


########################
# RUNNING THE EXAMPLES #
########################
if __name__ == "__main__":
    printer_preset = PrinterPreset(
        delimiter_left="│",
        delimiter_right="│",
        delimiter_right_color=Color.WHITE,
        delimiter_left_color=Color.WHITE
    )

    separator_preset = SeparatorPreset(
        delimiter_right="╮",
        delimiter_right_color=Color.WHITE,
        delimiter_left_color=Color.WHITE,
        delimiter_left="╭",
        separator_symbol="─",
        separator_color=Color.WHITE,
    )

    pretty_print("Hi, this is some sample text", preset=printer_preset, separator_preset=separator_preset)

    for i in range(256):
        print(f"\033[38;5;{i}m0", end="")