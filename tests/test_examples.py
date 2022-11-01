from codecs import unicode_escape_decode
import enum
from fancyprint.presets.unicode import Box
from fancyprint import *


options = ["Start", "Options", "Credits", "Exit"]
title = "Use Case#1: Main Menu"
title_color = "<w>"

exit_options = ["4", "exit", "q", "quit"]
errors = []
preset = Box.Hard

user_input = str()

while not user_input in exit_options:
    # Clear the screen
    os.system("clear")
    
    # Print the title
    pretty_print(title_color + title, preset=preset.printer_preset, separator_preset=preset.separator_preset)

    # Print options
    for index, value in enumerate(options):
        pretty_print(f"<b>{index+1}) <c>{value.title()}", enable_back_separator=True if index==0 else False, enable_front_separator=(False if not index == len(options)-1 else True),
                    preset=preset.printer_preset, separator_preset=preset.separator_preset)
        
    # Print the errors if any
    for i, error in enumerate(errors):
        pretty_print(error, preset=preset.printer_preset, separator_preset=preset.separator_preset, enable_back_separator=True if i == 0 else False, enable_front_separator=True if i == len(errors)-1 else False)
        
    # Get user input
    user_input = pretty_input("Enter a Option", preset=preset.input_preset).lower()
    
    # Add erros if any
    if not user_input in options:
        errors.append(f"<r>Option <g>'<y>{user_input}<g>'<r> is not valid!")
    else:
        pass
    