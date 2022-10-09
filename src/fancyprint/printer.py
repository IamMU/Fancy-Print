#######################
# IMPORTING LIBRARIES #
#######################
import os
import sys

from colorama import Fore, init as colorama_init

##########################
# INITIALIZING LIBRARIES #
##########################
colorama_init(autoreset=True)


###########
# CLASSES #
###########
class Printer:
    def __init__(self):
        # Utility variables
        self.__possible_color_inputs = {
            Fore.CYAN: ["cyan", "c"],
            Fore.WHITE: ["white", "w"],
            Fore.MAGENTA: ["magenta", "m"],
            Fore.YELLOW: ["yellow", "y"],
            Fore.BLUE: ["blue", "b"],
            Fore.RED: ["red", "r"],
            Fore.GREEN: ["green", "g"],
            Fore.BLACK: ["black", "bl"],
            Fore.LIGHTCYAN_EX: ["light cyan", "lc"],
            Fore.LIGHTWHITE_EX: ["light white", "lw"],
            Fore.LIGHTMAGENTA_EX: ["light magenta", "lm"],
            Fore.LIGHTYELLOW_EX: ["light yellow", "ly"],
            Fore.LIGHTBLUE_EX: ["light blue", "lb"],
            Fore.LIGHTRED_EX: ["light red", "lr"],
            Fore.LIGHTGREEN_EX: ["light green", "lg"],
            Fore.LIGHTBLACK_EX: ["light black", "lbl"],
        }

        # Variables
        self.__delimiter_left = "|"
        self.__delimiter_left_color = Fore.CYAN
        self.__delimiter_right = "|"
        self.__delimiter_right_color = Fore.CYAN

        self.__delimiter_space = 2

        self.__separator_back = "-"
        self.__separator_back_color = Fore.MAGENTA
        self.__separator_front = "-"
        self.__separator_front_color = Fore.MAGENTA

    def __convert_color_input(self, string: str) -> str | None:
        # Make string lower case
        string = string.lower()

        # Return respective color codes
        for key in self.__possible_color_inputs.keys():
            possible_codes = self.__possible_color_inputs[key]

            if string in possible_codes:
                return key

        # Return None if not valid
        return None

    def configure_options(self, delimiter_left: str, delimiter_right: str, delimiter_left_color: str,
                          delimiter_right_color: str, separator_back: str, separator_front: str,
                          separator_back_color: str, separator_front_color: str, delimiter_space: int) -> None:
        """Configure the options for the printer, such as color and symbols
        -------------------------------------------------------------------------------
        :param delimiter_left: Symbol for the left delimiter (default: "|")
        :type delimiter_left: str

        :param delimiter_right: Symbol for the right delimiter (default: "|")
        :type delimiter_right: str
        -------------------------------------------------------------------------------
        :param delimiter_left_color: Color for the left delimiter (default: Cyan)
        :type delimiter_left_color: str

        :param delimiter_right_color: Color for the right delimiter (default: Cyan)
        :type delimiter_right_color: str
        -------------------------------------------------------------------------------
        :param separator_back: Symbol for the back separator (default: "-")
        :type separator_back: str

        :param separator_front: Symbol for the front separator (default: "-")
        :type separator_front: str
        -------------------------------------------------------------------------------
        :param separator_back_color: Color for the back separator (default: Magenta)
        :type separator_back_color: str

        :param separator_front_color: Color for the front separator (default: Magenta)
        :type separator_front_color: str
        -------------------------------------------------------------------------------
        :param delimiter_space: Space between delimiters and text (default: 2)
        :type delimiter_space: int
        """

        # Assign all the symbols
        self.__delimiter_left = delimiter_left
        self.__delimiter_right = delimiter_right

        self.__separator_front = separator_front
        self.__separator_back = separator_back

        # Assign colors to the symbols
        self.__delimiter_left_color = self.__convert_color_input(delimiter_left_color) if self.__convert_color_input(delimiter_left_color) is not None else self.__delimiter_left_color
        self.__delimiter_right_color = self.__convert_color_input(delimiter_right_color) if self.__convert_color_input(delimiter_right_color) is not None else self.__delimiter_right_color

        self.__separator_back_color = self.__convert_color_input(separator_back_color) if self.__convert_color_input(separator_back_color) is not None else self.__separator_back_color
        self.__separator_front_color = self.__convert_color_input(separator_front_color) if self.__convert_color_input(separator_front_color) is not None else self.__separator_front_color

        # Assign other symbols
        self.__delimiter_space = delimiter_space

    def test_configurations(self):
        print(f"CONFIGURATIONS:")
        print(f" - DELIMITERS:")
        print(f"     - LEFT: {self.__delimiter_left_color}{self.__delimiter_left}")
        print(f"     - RIGHT: {self.__delimiter_right_color}{self.__delimiter_right}")
        print(f"     - SPACE: {self.__delimiter_space}")
        print(f" - SEPARATORS:")
        print(f"     - BACK: {self.__separator_back_color}{self.__separator_back}")
        print(f"     - FRONT: {self.__separator_front_color}{self.__separator_front}")

    def print(self, text: str, align="center", blank_character=" ", left_delimiter=True, right_delimiter=True, back_separator=True,
              front_separator=True):
        align = align.lower()

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

        for ftext in finalized_text_buffer:
            if len(ftext) > 5:
                is_color, color_count = self.__check_color_string_in_dict(ftext, Fore.__dict__, 5)
                if is_color:
                    length_of_text = int(len(ftext) - (color_count * 5))
                else:
                    length_of_text = len(ftext)
            else:
                length_of_text = len(ftext)

            # Calculate the amount of space, taking alignment into consideration
            if align == "center":
                # Amount of space is the half of the screen width - the length of the side separators - the half of the text length
                amount_of_space = int((terminal_size_h - 2) / 2 - length_of_text / 2)

                # Make spacing variables
                space_left = blank_character * amount_of_space
                space_right = blank_character * amount_of_space
            elif align == "right":
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - 2) - length_of_text)

                space_left = blank_character * (amount_of_space - 1)
                space_right = " "
            elif align == "left":
                # Amount of space is the screen width - the side separator's length - the text length
                amount_of_space = int((terminal_size_h - 2) - length_of_text)

                space_left = " "
                space_right = blank_character * (amount_of_space - 1)

            if len(space_left) + len(space_right) + length_of_text <= terminal_size_h:
                if align == "center":
                    space_right = space_right + blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))
                elif align == "right":
                    space_left = space_left + blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))
                elif align == "left":
                    space_right = space_right + blank_character * (
                                (terminal_size_h - 2) - (len(space_left) + len(space_right) + length_of_text))

            result = f"{Fore.CYAN}|{Fore.RESET}" + space_left + ftext + space_right + f"{Fore.CYAN}|"

            finalized_text_buffer[finalized_text_buffer.index(ftext)] = result

        if back_separator:
            self.separate_line("back")

        # Print text in finalized text buffer
        for msg in finalized_text_buffer:
            print(msg)

        if front_separator:
            self.separate_line("front")

    def __check_color_string_in_dict(self, string: str, dictionary: dict, pattern_look_len: int) -> (bool, int):
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

    def separate_line(self, position: str, enable_delimiter_left=True, enable_delimiter_right=True) -> None:
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

        separator_symbol = self.__separator_front if position == "front" else self.__separator_back
        separator_color = self.__separator_front_color if position == "front" else self.__separator_back_color

        # Calculations
        left_side = f"{self.__delimiter_left_color}{self.__delimiter_left}{' ' * self.__delimiter_space}" if enable_delimiter_left else ""
        right_side = f"{' ' * self.__delimiter_space}{self.__delimiter_right_color}{self.__delimiter_right}" if enable_delimiter_right else ""

        middle = f"{separator_color}{separator_symbol * (columns - ((self.__delimiter_space*(enable_delimiter_right + enable_delimiter_left)) + enable_delimiter_right + enable_delimiter_left))}"

        # Print the separator line
        print(f"{left_side}{middle}{right_side}")


#########
# TESTS #
#########
if __name__ == "__main__":
    printer = Printer()
    printer.configure_options(delimiter_left="|", delimiter_right="|",
                              delimiter_left_color="cyan", delimiter_right_color="cyan", separator_back="-",
                              separator_front="-", separator_front_color="magenta", separator_back_color="magenta",
                              delimiter_space=2)
    printer.test_configurations()

    printer.print(text="This is some text in the center", align="center")
    printer.print(text="This is some text on the left side", align="left", back_separator=False)
    printer.print(text="This is some text on the right side", align="right", back_separator=False)