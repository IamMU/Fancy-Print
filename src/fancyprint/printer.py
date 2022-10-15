#######################
# IMPORTING LIBRARIES #
#######################
import os
from typing import Tuple, Optional
from colorama import init as colorama_init, Fore
import re
from helpers import COLORS
from helpers import LogLevel, PrinterConfig, LogConfig, LogColor, PrintConfig, Align

from ftypes import Color, Preset, SeparatorPreset, PrinterPreset
###########
# CLASSES #
###########


class Printer:
    def __init__(self):
        """
        Initialize the printer
        """
        colorama_init(autoreset=True)

        # Configurations
        self.global_config = PrinterConfig()

    def configure_options(self, config: PrinterConfig) -> None:
        """Configure the printer options
        :param config: The configuration object
        :type config: Config
        """
        self.global_config = config


    def test_configurations(self) -> None:
        print(f"CONFIGURATIONS:")
        print(f" - DELIMITERS:")
        print(f"     - LEFT:  {self.global_config.delimiter_left_color}{self.global_config.delimiter_left}")
        print(f"     - RIGHT: {self.global_config.delimiter_right_color}{self.global_config.delimiter_right}")
        print(f"     - SPACE: {self.global_config.delimiter_space}")
        print(f" - SEPARATORS:")
        print(f"     - BACK:  {self.global_config.separator_back_color}{self.global_config.separator_back}")
        print(f"     - FRONT: {self.global_config.separator_front_color}{self.global_config.separator_front}")

    def convert_tags_to_color(self,text):
        pattern = r"<(.*?)>"
        result = text
        tag_content = re.findall(pattern, result, flags=0)

        for color in COLORS.keys():
            if color in tag_content:
                result = result.replace(f"<{color}>", COLORS[color])

        return result

    def print(self, text: str, print_config=PrintConfig()):
        text=self.convert_tags_to_color(text)
        colored_text = text

        for color in Fore.__dict__:
            text = text.replace(Fore.__dict__[color], "")

        uncolored_text = text

        # Get updated terminal size
        terminal_size_h = os.get_terminal_size().columns

        # Lengths
        colored_text_length = len(colored_text)
        uncolored_text_length = len(uncolored_text)

        # Buffers
        uncolored_text_buffer = list()
        colored_text_insertion_buffer = list()
        finalized_text_buffer = list()

        # Calculating buffers
        available_char_space = terminal_size_h - self.global_config.delimiter_space
        if len(uncolored_text) >= available_char_space:
            # Variables for calculation
            position_counter = 0
            last_position = position_counter
            current_text_buffer = str()

            # Calculate uncolored buffer
            for index, unc_char in enumerate(uncolored_text):
                position_counter = (index + 1) - last_position

                # Add the character to the current text buffer
                current_text_buffer += unc_char

                # Check if position counter is greater than available space
                if position_counter >= available_char_space:
                    # Add the character in the current_text_buffer to the uncolored buffer
                    uncolored_text_buffer.append(current_text_buffer)

                    # Set last position to current
                    last_position = position_counter + last_position

                    # Reset the position counter
                    position_counter = 0

                    # Reset current text buffer
                    current_text_buffer = ""

                # Check if position counter(+ last position to make it current) is last character
                if position_counter + last_position >= uncolored_text_length:
                    # Add the character in the current_text_buffer to the uncolored buffer
                    uncolored_text_buffer.append(current_text_buffer)

                    # Set last position to 0 because end of loop
                    last_position = 0

                    # Reset the position counter
                    position_counter = 0

                    # Reset current text buffer
                    current_text_buffer = ""

            color_code_chars_length = 5
            without_color_index = 0
            # Calculate color insertion buffer
            for index, c_char in enumerate(colored_text):
                if c_char == "\x1b":
                    if not without_color_index - color_code_chars_length <= 0:
                        without_color_index -= color_code_chars_length

                    colored_text_insertion_buffer.append(((without_color_index,
                                                           without_color_index + color_code_chars_length),
                                                          c_char + colored_text[
                                                                   index + 1:index + color_code_chars_length]))

                    without_color_index += 1
                    continue

                without_color_index += 1
        else:
            uncolored_text_buffer.append(uncolored_text)
            colored_text_insertion_buffer.append(colored_text)

            finalized_text_buffer.append(colored_text)

        if len(uncolored_text) >= available_char_space:

            last_color = ""
            for unc_text in uncolored_text_buffer:
                res = ""
                skip_parent_iteration = False
                last_index = 0
                for index, char in enumerate(unc_text):
                    if len(colored_text_insertion_buffer) > 0:
                        for color_insertion in colored_text_insertion_buffer:
                            i = color_insertion[0][0]
                            v = color_insertion[1]

                            if index == i:
                                res += v + char
                                last_color = v
                                colored_text_insertion_buffer.remove(color_insertion)
                                skip_parent_iteration = True

                    if skip_parent_iteration:
                        skip_parent_iteration = False
                        continue

                    res += char

                if not index == last_index:
                    res = last_color + res
                    last_index = index

                finalized_text_buffer.append(res)

        for finalized_text in finalized_text_buffer:
            if len(finalized_text) > 5:
                is_color, color_count = self.__check_color_string_in_dict(finalized_text, Fore.__dict__, 5)
                length_of_text = len(finalized_text) if not is_color else len(finalized_text) - color_count - 4
            else:
                length_of_text = len(finalized_text)

            # Calculate the amount of space, taking alignment into consideration
            if print_config.align == Align.CENTER:
                # Amount of space is the half of the screen width - the length of the side separators - the half of the text length
                amount_of_space = int((((terminal_size_h - self.global_config.delimiter_space - 2) / 2) - (length_of_text / 2)))
                amount_of_space = int(((terminal_size_h - self.global_config.delimiter_space - 2)/2) - (length_of_text/2))
                print(amount_of_space)

                # Make spacing variables
                space_left = " " * amount_of_space
                space_right = " " * amount_of_space
            elif print_config.align == Align.RIGHT:
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - self.global_config.delimiter_space - 2) - length_of_text)

                space_left = print_config.blank_character * (amount_of_space)
                space_right = " " * self.global_config.delimiter_space
            elif print_config.align == Align.LEFT:
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - self.global_config.delimiter_space - 2) - length_of_text)

                space_left = " " * self.global_config.delimiter_space
                space_right = print_config.blank_character * (amount_of_space)

            # if len(space_left) + len(space_right) + length_of_text < terminal_size_h:
            #     if print_config.align == Align.CENTER:
            #         space_right = space_right + print_config.blank_character * (
            #                     (terminal_size_h - self.global_config.delimiter_space) - (len(space_left) + len(space_right) + length_of_text))
            #     elif print_config.align == Align.RIGHT:
            #         space_left = space_left + print_config.blank_character * (
            #                     (terminal_size_h - self.global_config.delimiter_space) - (len(space_left) + len(space_right) + length_of_text))
            #     elif print_config.align == Align.LEFT:
            #         space_right = space_right + print_config.blank_character * (
            #                     (terminal_size_h - self.global_config.delimiter_space) - (len(space_left) + len(space_right) + length_of_text))

            result = f"{Fore.CYAN}|{Fore.RESET}" + space_left + finalized_text + space_right + f"{Fore.CYAN}|"

            finalized_text_buffer[finalized_text_buffer.index(finalized_text)] = result

        if print_config.back_separator:
            self.separate_line("back")

        # Print text in finalized text buffer
        for msg in finalized_text_buffer:
            print(msg)

        if print_config.front_separator:
            self.separate_line("front")

    def log(self, message: str, log_config=LogConfig()):
        # log level color and string
        level = str(log_config.level.value)
        color = LogColor[log_config.level.name].value

        # level string formatting
        level_str = log_config.level_padding_char * (log_config.level_padding - len(level)) + f"[ {level} ]"

        # Indentation
        indent = "****" * log_config.hierarchy_level

        # Message separation
        messages = message.split('\n')

        for i, msg in enumerate(messages):
            text = f"{indent}{color}{level_str} {msg}" if i == 0 else f"{indent}{'*' * (len(level_str) )}{color} {msg}"
            self.print(f"{text}", PrintConfig(align=Align.LEFT, back_separator=False, front_separator=False))

    def __check_color_string_in_dict(self, string: str, dictionary: dict, pattern_look_len: int) -> Tuple[bool, int]:
        count = 0
        for index, char in enumerate(string):
            if char == "\x1b":
                full_pattern = string[index: index + pattern_look_len]

                if full_pattern in dictionary.values():
                    count += 1

        if count == 0:
            return False, count
        else:
            return True, count

    def separate_line(self, delimiter_left="|", delimiter_left_color=Fore.WHITE, enable_delimiter_left=True,
                      delimiter_right="|", delimiter_right_color=Fore.WHITE, enable_delimiter_right=True,
                      separator="-", separator_color=Fore.WHITE, enable_separator=True) -> None:
        """Prints a separator line
        :param position: The position of the separator ( back/front )
        :type position: str

        :param enable_delimiter_left: If left delimiter is to be displayed or not (default: True)
        :type enable_delimiter_left: bool

        :param enable_delimiter_right: If right delimiter is to be displayed or not (default: True)
        :type enable_delimiter_right: bool
        """
        # Variables

        # Get the width of terminal
        columns = os.get_terminal_size().columns

        # Calculations
        left_side = f"{self.global_config.delimiter_left_color}{delimiter_left}{' ' * self.global_config.delimiter_space}" if enable_delimiter_left else ""
        right_side = f"{' ' * self.global_config.delimiter_space}{self.global_config.delimiter_right_color}{delimiter_right}" if enable_delimiter_right else ""

        middle = f"{separator_color}{separator_symbol * (columns - ((self.global_config.delimiter_space*(enable_delimiter_right + enable_delimiter_left)) + enable_delimiter_right + enable_delimiter_left))}"

        # Print the separator line
        print(f"{left_side}{middle}{right_side}")


def separate_line(preset: SeparatorPreset | Preset = None,
                  delimiter_left: str = "|", delimiter_left_color: Color = Color.CYAN,
                  enable_left_delimiter: bool = True,
                  delimiter_right: str = "|", delimiter_right_color: Color = Color.CYAN,
                  enable_right_delimiter: bool = True,
                  delimiter_space_amount: int = 0, delimiter_space_symbol: str = " ",
                  separator_symbol: str = "-", separator_color: Color = Color.MAGENTA,
                  enable_separator: bool = True) -> None:
    # Check if preset is being used or not
    if preset is None:
        # Do nothing, all variables will be same
        pass
    else:
        # If some preset is being used, check if it is global or not, else raise a type error
        if type(preset) == SeparatorPreset:
            # Assign all variables to respective preset values
            delimiter_left = preset.delimiter_left
            delimiter_left_color = preset.delimiter_left_color

            delimiter_right = preset.delimiter_right
            delimiter_right_color = preset.delimiter_right_color

            separator_symbol = preset.separator_symbol
            separator_color = preset.separator_color

            delimiter_space_amount = preset.delimiter_space_amount
            delimiter_space_symbol = preset.delimiter_space_symbol
        elif type(preset) == Preset:
            # Assign all separator-valid values to respective variables
            delimiter_left = preset.separator_preset.delimiter_left
            delimiter_left_color = preset.separator_preset.delimiter_left_color

            delimiter_right = preset.separator_preset.delimiter_right
            delimiter_right_color = preset.separator_preset.delimiter_right_color

            separator_symbol = preset.separator_preset.separator_symbol
            separator_color = preset.separator_preset.separator_color

            delimiter_space_amount = preset.separator_preset.delimiter_space_amount
            delimiter_space_symbol = preset.separator_preset.delimiter_space_symbol
        else:
            raise TypeError(f"Expected types: SeperatorPreset or Preset | Found: {type(preset).__name__}")

    # Calculate things to print

    # Getting terminal width (in chars)
    terminal_width = os.get_terminal_size().columns

    # Calculating the left side
    left_side = f"{(delimiter_left_color + delimiter_left + (delimiter_space_symbol * delimiter_space_amount)) if enable_left_delimiter else ''}"

    # Calculating the right side
    right_side = f"{((delimiter_space_symbol * delimiter_space_amount) + delimiter_right_color + delimiter_right) if enable_right_delimiter else ''}"

    # Calculating the middle

    # Seperator symbol length is terminal width - 1 per delimiter - amount of delimiter space
    middle = f"{separator_color}{separator_symbol * int(terminal_width - (enable_right_delimiter + enable_right_delimiter) + delimiter_space_amount)}"

    # Printing everything to terminal
    print(f"{left_side}{middle}{right_side}")


#########
# TESTS #
#########
if __name__ == "__main__":
    # printer = Printer()
    #
    # #################
    # # DEFAULT TESTS #
    # #################
    #
    # # All must work else not ready for production
    # # test_text = f"Hi there, I am a collection of characters!" * 2
    # #
    # # printer.print(test_text)
    # # printer.print(test_text, PrintConfig(
    # #     align=Align.LEFT,
    # #     back_separator=False
    # # ))
    # # printer.print(test_text, PrintConfig(
    # #     align=Align.RIGHT,
    # #     back_separator=False
    # # ))
    #
    # printer.separate_line("back", delimiter_left="╭", delimiter_right="╮")
    separate_line()
