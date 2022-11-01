#######################
# IMPORTING LIBRARIES #
#######################
from fancyprint.ftypes import Preset, PrinterPreset, SeparatorPreset, Color, InputPreset
from dataclasses import dataclass


###########
# PRESETS #
###########
@dataclass
class Box:
    @dataclass
    class Hard:
        # Seperator Preset
        separator_preset = SeparatorPreset(
            # Back
            back_delimiter_left="┌",
            back_delimiter_left_color=Color.WHITE,

            back_delimiter_right="┐",
            back_delimiter_right_color=Color.WHITE,

            back_separator_symbol="─",
            back_separator_color=Color.WHITE,

            back_delimiter_space_amount=0,
            back_delimiter_space_symbol=" ",

            # Front
            front_delimiter_left="└",
            front_delimiter_left_color=Color.WHITE,

            front_delimiter_right="┘",
            front_delimiter_right_color=Color.WHITE,

            front_separator_symbol="─",
            front_separator_color=Color.WHITE,

            front_delimiter_space_amount=0,
            front_delimiter_space_symbol=" ",
        )

        # Printer Preset
        printer_preset = PrinterPreset(
            delimiter_left="│",
            delimiter_left_color=Color.WHITE,

            delimiter_right="│",
            delimiter_right_color=Color.WHITE,

            delimiter_space_amount=0,
            delimiter_space_symbol=" ",

            hyphenation=True
        )
        
        # Input Preset
        input_preset = InputPreset(
            separator_preset=separator_preset,
            
            delimiter_left="├",
            delimiter_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_left="─ ",
            delimiter_left_prompt_separator_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_right=": ",
            delimiter_left_prompt_separator_right_color=Color.WHITE,
            
            input_separator_left="",
            input_separator_left_color=Color.WHITE,
            
            input_text_color=Color.YELLOW,
        )

    @dataclass
    class Round:
        # Seperator Preset
        separator_preset = SeparatorPreset(
            # Back
            back_delimiter_left="╭",
            back_delimiter_left_color=Color.WHITE,

            back_delimiter_right="╮",
            back_delimiter_right_color=Color.WHITE,

            back_separator_symbol="─",
            back_separator_color=Color.WHITE,

            back_delimiter_space_amount=0,
            back_delimiter_space_symbol=" ",

            # Front
            front_delimiter_left="╰",
            front_delimiter_left_color=Color.WHITE,

            front_delimiter_right="╯",
            front_delimiter_right_color=Color.WHITE,

            front_separator_symbol="─",
            front_separator_color=Color.WHITE,

            front_delimiter_space_amount=0,
            front_delimiter_space_symbol=" ",
        )

        # Printer Preset
        printer_preset = PrinterPreset(
            delimiter_left="│",
            delimiter_left_color=Color.WHITE,

            delimiter_right="│",
            delimiter_right_color=Color.WHITE,

            delimiter_space_amount=0,
            delimiter_space_symbol=" ",

            hyphenation=True
        )
        
        # Input Preset
        input_preset = InputPreset(
            separator_preset=separator_preset,
            
            delimiter_left="├",
            delimiter_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_left="─ ",
            delimiter_left_prompt_separator_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_right=": ",
            delimiter_left_prompt_separator_right_color=Color.WHITE,
            
            input_separator_left="",
            input_separator_left_color=Color.WHITE,
            
            input_text_color=Color.YELLOW,
        )

    @dataclass
    class DoubleLiner:
        # Seperator Preset
        separator_preset = SeparatorPreset(
            # Back
            back_delimiter_left="╔",
            back_delimiter_left_color=Color.WHITE,

            back_delimiter_right="╗",
            back_delimiter_right_color=Color.WHITE,

            back_separator_symbol="═",
            back_separator_color=Color.WHITE,

            back_delimiter_space_amount=0,
            back_delimiter_space_symbol=" ",

            # Front
            front_delimiter_left="╚",
            front_delimiter_left_color=Color.WHITE,

            front_delimiter_right="╝",
            front_delimiter_right_color=Color.WHITE,

            front_separator_symbol="═",
            front_separator_color=Color.WHITE,

            front_delimiter_space_amount=0,
            front_delimiter_space_symbol=" ",
        )

        # Printer Preset
        printer_preset = PrinterPreset(
            delimiter_left="║",
            delimiter_left_color=Color.WHITE,

            delimiter_right="║",
            delimiter_right_color=Color.WHITE,

            delimiter_space_amount=0,
            delimiter_space_symbol=" ",

            hyphenation=True
        )
        
        # Input Preset
        input_preset = InputPreset(
            separator_preset=separator_preset,
            
            delimiter_left="╠",
            delimiter_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_left="═ ",
            delimiter_left_prompt_separator_left_color=Color.WHITE,
            
            delimiter_left_prompt_separator_right=": ",
            delimiter_left_prompt_separator_right_color=Color.WHITE,
            
            input_separator_left="",
            input_separator_left_color=Color.WHITE,
            
            input_text_color=Color.YELLOW,
        )
        

#########
# TESTS #
#########
if __name__ == "__main__":
    pass
