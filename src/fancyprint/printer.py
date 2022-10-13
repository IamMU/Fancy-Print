#######################
# IMPORTING LIBRARIES #
#######################
import os
from typing import Tuple
from colorama import init as colorama_init, Fore
from .helpers.types import PrinterConfig,PrintConfig,LogConfig
from .helpers.constants import LogLevel,LogColor,Align,COLORS 
import re
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

    def configure_options(self, config: PrinterConfig):
        """Configure the printer options
        :param config: The configuration object
        :type config: Config
        """
        self.global_config = config

    def test_configurations(self):
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
        string = text
        tag_content=re.findall(pattern, string, flags=0)
        ha=[]
        for items in tag_content:
            if items in COLORS:
                ha.append([k for k,v in COLORS.items() if v == COLORS[items]])
                string=string.replace("<{}>".format(str(items)),str(ha[tag_content.index(items)][0]))
        return string    
    def print(self, text: str, print_config = PrintConfig()):
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
        available_char_space = terminal_size_h - 4
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
                amount_of_space = int((terminal_size_h - 2) / 2 - length_of_text / 2)

                # Make spacing variables
                space_left = print_config.blank_character * amount_of_space
                space_right = print_config.blank_character * amount_of_space
            elif print_config.align == Align.RIGHT:
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - 2) - length_of_text)

                space_left = print_config.blank_character * (amount_of_space - 1)
                space_right = " "
            elif print_config.align == Align.LEFT:
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - 2) - length_of_text)

                space_left = " "
                space_right = print_config.blank_character * (amount_of_space - 1)

            if len(space_left) + len(space_right) + length_of_text <= terminal_size_h:
                if print_config.align == Align.CENTER:
                    space_right = space_right + print_config.blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))
                elif print_config.align == Align.RIGHT:
                    space_left = space_left + print_config.blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))
                elif print_config.align == Align.LEFT:
                    space_right = space_right + print_config.blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))

            result = f"{Fore.CYAN}|{Fore.RESET}" + space_left + finalized_text + space_right + f"{Fore.CYAN}|"

            finalized_text_buffer[finalized_text_buffer.index(finalized_text)] = result

        if print_config.back_separator:
            self.separate_line("back")

        # Print text in finalized text buffer
        for msg in finalized_text_buffer:
            print(msg)

        if print_config.front_separator:
            self.separate_line("front")
    def log(self, message: str, log_config = LogConfig()):
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

    def separate_line(self, position: str, enable_delimiter_left=True, enable_delimiter_right=True):
        """Prints a separator line
        :param position: The position of the separator ( back/front )
        :type position: str

        :param enable_delimiter_left: If left delimiter is to be displayed or not (default: True)
        :type enable_delimiter_left: bool

        :param enable_delimiter_right: If right delimiter is to be displayed or not (default: True)
        :type enable_delimiter_right: bool
        """
        # Variables

        # Make position lowercase
        position = position.lower()

        # Get the width of terminal
        columns = os.get_terminal_size().columns

        separator_symbol = self.global_config.separator_front if position == "front" else self.global_config.separator_back
        separator_color = self.global_config.separator_front_color if position == "front" else self.global_config.separator_back_color

        # Calculations
        left_side = f"{self.global_config.delimiter_left_color}{self.global_config.delimiter_left}{' ' * self.global_config.delimiter_space}" if enable_delimiter_left else ""
        right_side = f"{' ' * self.global_config.delimiter_space}{self.global_config.delimiter_right_color}{self.global_config.delimiter_right}" if enable_delimiter_right else ""

        middle = f"{separator_color}{separator_symbol * (columns - ((self.global_config.delimiter_space*(enable_delimiter_right + enable_delimiter_left)) + enable_delimiter_right + enable_delimiter_left))}"

        # Print the separator line
        print(f"{left_side}{middle}{right_side}")


#########
# TESTS #
#########
if __name__ == "__main__":
    printer = Printer()
    printer.configure_options(PrinterConfig(delimiter_left="|", delimiter_right="|",
                              delimiter_left_color="cyan", delimiter_right_color="cyan", separator_back="-",
                              separator_front="-", separator_front_color="magenta", separator_back_color="magenta",
                              delimiter_space=2))
    printer.test_configurations()

    printer.print("This is some text in the center", PrintConfig(align=Align.CENTER))
    printer.print("This is some text on the left side", PrintConfig(align=Align.LEFT, back_separator=False))
    printer.print("This is some text on the right side", PrintConfig(align=Align.RIGHT, back_separator=False))

    printer.log("hello 1")
    printer.log("hello 1",  LogConfig(hierarchy_level=1))
    printer.log("hello 1",  LogConfig(hierarchy_level=2))
    printer.log("hello",  LogConfig(color=Fore.RED))
    printer.log("hello 1\nhello 1",  LogConfig(color=Fore.RED))
    printer.log("hello 1\nhello1",  LogConfig(hierarchy_level=1))

    printer.log("warn", LogConfig(level=LogLevel.WARN))
    printer.log("error", LogConfig(level=LogLevel.ERROR))
    printer.log("success", LogConfig(level=LogLevel.SUCCESS))

    printer.log("test",  LogConfig(level_padding_char='#', level_padding=20))
    printer.log("test",  LogConfig(level_padding_char='-', level_padding=20, level=LogLevel.WARN))
    printer.log("test",  LogConfig(level_padding_char='.', level_padding=20, level=LogLevel.ERROR))
    printer.log("test",  LogConfig(level_padding_char='>', level_padding=20, level=LogLevel.SUCCESS))

