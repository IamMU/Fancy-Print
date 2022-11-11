#######################
# IMPORTING LIBRARIES #
#######################
import os
import time
import re
from turtle import pos
from typing import Tuple
from typing import Type
from fancyprint.ftypes import Color, Preset, SeparatorPreset, PrinterPreset, InputPreset, Align, input_preset
from fancyprint.presets.unicode import Box
from fancyprint.utilities import exec_time


###########
# CLASSES #
###########
class Printer:
    def __init__(self, enable_dev_mode: bool = False):
        """Constructor for the printer class

        Args:
            enable_dev_mode (bool, optional): Whether to use the developer mode. Defaults to False.
        """
        ##############
        # ATTRIBUTES #
        ##############

        ###########
        # PRIVATE #
        ###########
        self.__default_preset = Box.Hard()

        self.__lines_printed = int()

    def set_default_preset(self, preset: Preset | PrinterPreset | InputPreset | SeparatorPreset,
                           change_single_preset: bool = False) -> None:
        """Changes the default preset for the printer

        Args:
            preset (Preset): New preset
            change_single_prest (bool): Whether to only change one "local" preset in the default "global" preset
        """
        # Variable for the preset type, so we don't need to calculate it again and again
        preset_type = type(preset)

        # Check if the preset type is correct
        if preset_type is not Preset:
            # If user doesn't want to change a single preset then raise a type error
            if not change_single_preset:
                raise TypeError(
                    f"""Expected Type -> Preset
           Found -> {preset_type.__name__}""")

            # If user does want to change one specific preset:

            # Variable for other preset types
            other_preset_types = [PrinterPreset, SeparatorPreset, InputPreset]

            # Check if the preset type is a valid preset
            if preset_type in other_preset_types:
                # Loop through other available preset
                for p in other_preset_types:
                    if preset_type is PrinterPreset:
                        self.default_preset.printer_preset = preset
                    elif preset_type is SeparatorPreset:
                        self.default_preset.separator_preset = preset
                    elif preset_type is InputPreset:
                        self.default_preset.input_preset = preset
            # Else raise a type error again
            else:
                raise TypeError(
                    f"""Expected Type -> {" | ".join([c.__name__ for c in other_preset_types])}
           Found -> {preset_type.__name__}""")
        else:
            # Change default preset to new preset
            self.default_preset = preset

    def get_pattern_data(self, text: str, *patterns) -> dict:
        """Returns data for x patterns

        Args:
            text (str): String to search through

        Returns:
            dict: Dictionary of all data collected
                   amount (int): Occurences of the patterns
                   combined_length (int): Length of all the pattern contents combined
        """

        #############
        # VARIABLES #
        #############
        results = list()

        occurences = int()
        collective_length = int()

        ################
        # CALCULATIONS #
        ################

        # Loop through all the patterns
        for pattern in patterns:
            # Create the regular expression
            regex = re.compile(pattern)

            # Search for all occurrences of the pattern in the text
            values = regex.findall(text)

            # Add the found occurrences in the results variable
            results.extend(values)

        # Assign the respective values
        occurences = len(results)
        collective_length = sum([len(pat) for pat in results])

        # Return the result
        return {
            "amount": occurences,
            "combined_length": collective_length,
        }

    def give_color_codes_data(self, text: str, color_code_len: int = Color.COLOR_CODE_LENGTH) -> Tuple[bool, int]:
        """Gives color code data of a string, namely if color is being used, amount of colors used, ...
        
        Args:
            text (str): The text to check
            color_code_len (int): Amount of space a color code has (Default: Color.COLOR_CODE_LENGTH)
            
        Returns:
            tuple: Tuple with the data (color used, amount of color used)
        """
        #############
        # VARIABLES #
        #############
        count = 0

        ################
        # CALCULATIONS #
        ################

        # Loop through the text
        for index, char in enumerate(text):
            # If the current character is an ansi escape sequence
            if char == "\x1b":
                # Set the pattern to the current index till current index plus the color code length, hence the entire
                # color code
                full_pattern = text[index: index + color_code_len]

                # If the code is valid then add 1 to the count
                if full_pattern in Color.__dict__.values():
                    count += 1

        #########################
        # RETURNING THE RESULTS #
        #########################

        # If the count is 0, means no color was found, else return True
        if count == 0:
            return False, count
        else:
            return True, count

    def tag_to_color(self, text: str) -> str:
        """Converts a string with color tags to a string with color (codes)

        Args:
            text (str): The text to be converted
        """
        #############
        # VARIABLES #
        #############
        result = text

        ##############
        # CONVERSION #
        ##############

        # Loop through the tags and their respective codes
        for tag in Color.tag_map.keys():
            final_code = f"<{tag}>"

            # Replace the tag with the color code (if it exists in the text)
            result = result.replace(final_code, Color.tag_map[tag])

        ########################
        # RETURNING THE RESULT #
        ########################
        return result

    def colored_to_uncolored(self, text: str, tags: bool = True) -> str:
        """Converts a string with color codes to a non-colored string
        
        Args:
            text (str): The text to convert
            tags (bool): Whether to convert from color tags
            
        Returns:
            str: Uncolored text"""
        # If remove tags
        if tags:
            # Loop through tags list
            for tag in Color.tag_map.keys():
                # Add syntax to tag
                color_code = f"<{tag}>"

                # Remove the tag from the text
                text = text.replace(color_code, "")

        # Return the result
        return text

    def get_default_preset(self) -> Preset:
        """Returns the default preset

        Returns:
            Preset: The default preset
        """
        return self.__default_preset

    def separator_line(self, position: str = "back", preset: SeparatorPreset | Preset = None,
                       enable_left_delimiter: bool = True, enable_right_delimiter: bool = True,
                       test_mode: bool = False, testing_terminal_width: int = 100) -> None:
        """Prints a separator line

        Args:
            position (str, optional): Which position the separator should use. Defaults to "back".
            preset (SeparatorPreset | Preset, optional): What preset should be used. If None, the default preset is used. Defaults to None.
            enable_left_delimiter (bool, optional): Whether to print the left delimiter. Defaults to True.
            enable_right_delimiter (bool, optional): Whether to print the right delimiter. Defaults to True.
            test_mode (bool, optional): Whether to use testing mode. Defaults to False.
            testing_terminal_width (int, optional): Artificial terminal length to be used in test mode. Defaults to 100.
        """
        #############
        # VARIABLES #
        #############

        # Make preset variable        
        preset = self.__default_preset.separator_preset if preset is None else (
            preset if type(preset) is SeparatorPreset else preset.separator_preset)

        # Make position lower
        position = position.lower()

        # Getting terminal width (in chars) | If testing mode, using custom width
        terminal_width = os.get_terminal_size().columns if not test_mode else testing_terminal_width

        # Make variables for ease use, without worrying for the position in the preset in following lines
        delimiter_left_color = preset.back_delimiter_left_color if position == "back" else preset.front_delimiter_left_color
        delimiter_left = preset.back_delimiter_left if position == "back" else preset.front_delimiter_left

        delimiter_right_color = preset.back_delimiter_right_color if position == "back" else preset.front_delimiter_right_color
        delimiter_right = preset.back_delimiter_right if position == "back" else preset.front_delimiter_right

        delimiter_space_symbol = preset.back_delimiter_space_symbol if position == "back" else preset.front_delimiter_space_symbol
        delimiter_space_amount = preset.back_delimiter_space_amount if position == "back" else preset.front_delimiter_space_amount

        separator_color = preset.back_separator_color if position == "back" else preset.front_separator_color
        separator_symbol = preset.back_separator_symbol if position == "back" else preset.front_separator_symbol

        # Sides
        middle = str()
        left_side = str()
        right_side = str()

        ################
        # CALCULATIONS #
        ################

        # Left side
        if enable_left_delimiter:
            left_side = (delimiter_left_color + delimiter_left) + (delimiter_space_symbol * delimiter_space_amount)
        else:
            left_side = delimiter_space_symbol * delimiter_space_amount

        # Right side
        if enable_right_delimiter:
            right_side = (delimiter_space_symbol * delimiter_space_amount) + (delimiter_right_color + delimiter_right)
        else:
            right_side = delimiter_space_symbol * delimiter_space_amount

        # Middle

        # Get length of the other sides
        left_side_length = len(left_side)
        right_side_length = len(right_side)

        # Remove color code length if it is used
        left_side_length -= (Color.COLOR_CODE_LENGTH if left_side_length > 0 and enable_left_delimiter else 0)
        right_side_length -= (Color.COLOR_CODE_LENGTH if right_side_length > 0 and enable_right_delimiter else 0)

        # Calculate amount of space to exclude
        exclude_space = int(terminal_width - left_side_length - right_side_length)

        middle = (separator_color + (separator_symbol * exclude_space))

        ############
        # PRINTING #
        ############

        # Print the calculated parts to the screen | Add white at end to reset color
        print(left_side + middle + right_side + Color.WHITE)

    def print(self, text: str, align: Align = Align.CENTER,
              preset: PrinterPreset | Preset = None, separator_preset: SeparatorPreset | Preset = None,

              enable_left_delimiter: bool = True, enable_right_delimiter: bool = True,

              enable_back_separator_delimiter_left: bool = True, enable_back_separator_delimiter_right: bool = True,
              enable_front_separator_delimiter_left: bool = True, enable_front_separator_delimiter_right: bool = True,

              hyphenation: bool = None,
              enable_back_separator: bool = True, enable_front_separator: bool = True,

              test_mode: bool = False, testing_terminal_width: int = 100) -> None:
        """Prints text to console/terminal

        Args:
            text (str): Text to print
            align (Align, optional): Alignment to use. Defaults to Align.CENTER.
            preset (PrinterPreset | Preset, optional): Preset to use for the printer. If None, default preset will be used. Defaults to None.
            separator_preset (SeparatorPreset | Preset, optional): Preset to use for the separator. Default preset will be used if None. Defaults to None.
            enable_back_separator_delimiter_left (bool, optional): Whether to print the left delimiter of the back separator. Defaults to True.
            enable_back_separator_delimiter_right (bool, optional): Whether to print the right delimiter of the back separator. Defaults to True.
            enable_front_separator_delimiter_left (bool, optional): Whether to print the left delimiter of the front separator. Defaults to True.
            enable_front_separator_delimiter_right (bool, optional): Whether to print the right delimiter of the front separator. Defaults to True.
            hyphenation (bool, optional): Whether to use hyphenation. If None, preset settings will be used. Defaults to None.
            enable_back_separator (bool, optional): Whether to print the back separator line. Defaults to True.
            enable_front_separator (bool, optional): Whether to print the front separator line. Defaults to True.
            test_mode (bool, optional): Whether to use test mode. Defaults to False.
            testing_terminal_width (int, optional): What artifificial terminal length to use in test mode. Defaults to 100.
        """
        #############
        # VARIABLES #
        #############

        # Preset variable
        printer_preset = self.__default_preset.printer_preset if preset is None else (
            preset if type(preset) is PrinterPreset else preset.printer_preset)
        separator_preset = self.__default_preset.separator_preset if separator_preset is None else (
            separator_preset if type(separator_preset) is SeparatorPreset else separator_preset.separator_preset)

        # Length of text (Remove all color code lengths)

        text_length = len(text) - (Color.COLOR_CODE_LENGTH * self.give_color_codes_data(text)[1])

        # Get terminal width
        terminal_width = os.get_terminal_size().columns if not test_mode else testing_terminal_width

        # Available width for text
        text_available_length = terminal_width - (printer_preset.delimiter_space_amount * 2) - \
                                (enable_left_delimiter + enable_right_delimiter)

        # List that contains lines to print
        lines = list()

        # Hyphenation variable
        hyphenation = printer_preset.hyphenation if hyphenation is None else hyphenation

        # print(f"Terminal width: {terminal_width}\nAvailable Length for text: {text_available_length}\n"
        #       f"Text Length(!COLOR): {text_length}\nText Length(COLOR): {len(text)}")

        ###################################
        # PREPARING TEXT FOR CALCULATIONS #
        ###################################

        # If given text is greater than available space, split text on lines
        if text_length > text_available_length:
            # Variables
            char_count = 0
            previous_char_count = char_count

            # Loop through the text characters
            for index, character in enumerate(text):
                # Increment character counter by 1
                char_count += 1

                # Tags amount
                tags_data = self.get_pattern_data(text[previous_char_count:char_count], r"<.>", r"<..>", r"<...>")
                tags_amount = tags_data['amount']
                # print(str(tags_amount) + f"- {text[previous_char_count:char_count]}")

                # Check if current character is a new line
                if character == "\n":
                    # Start index is previous character, i.e. where we ended the buffer in the last iteration
                    start_index = previous_char_count

                    # End index is the current character count EXCLUDING the new line character
                    end_index = char_count - 1

                    # Append the buffer to the lines list
                    lines.append(text[start_index:end_index])

                    # Update the previous character counter
                    previous_char_count = char_count
                    continue

                if index == text_length - 1:
                    # If end reached append remainder of text to list

                    # Start index is previous character counter
                    start_index = previous_char_count

                    # End index is current character counter
                    end_index = char_count

                    # Append the current buffer to the lines list
                    lines.append(text[start_index:end_index])

                    # Synchronize the previous character counter
                    previous_char_count = char_count
                # Check if the character count is the available space
                # Remove the previous character count to get the current counter
                elif (char_count - previous_char_count) == text_available_length + (tags_data["combined_length"]):
                    # Start index is previous character, i.e. where we ended the buffer in the last iteration
                    start_index = previous_char_count

                    # End index is the current character count
                    end_index = char_count

                    # Track whether to hyphenate or not
                    add_hyphen = False

                    # If hyphenation is enabled
                    if hyphenation:
                        # Index of next char is last index + 1 excluding the tags in the line
                        next_char_index = end_index + 1 - tags_amount

                        # Next character
                        next_char = text[next_char_index]

                        # Previous character is last index - 1 excluding the tags in the line
                        previous_char_index = end_index - 1 - tags_amount

                        # Previous character
                        prev_char = text[previous_char_index]

                        # Boolean to track, whether to add a hyphen
                        add_hyphen = False

                        # Check whether the current character is a space
                        if not character == " ":
                            # print(f"Previous: {prev_char}\nCurrent: {character}\nNext: {next_char}")

                            # Check if we are in the middle of a word
                            if not next_char == " " and not prev_char == " ":
                                # Make add_hyphen true
                                add_hyphen = True

                                # Add the text to the lines list, with the hyphenation
                                lines.append(text[start_index:end_index - 1] + "-")

                                # Don't add last char in previous_char_count
                                previous_char_count = char_count - 1
                            elif prev_char == " " and not character == " " and not next_char == " ":
                                # Get last space character
                                current_char = character
                                index_difference = 0

                                while not current_char == " ":
                                    index_difference -= 1
                                    current_char = text[end_index + index_difference]

                                # print(f"First Word Char: {current_char} with difference: {index_difference}")

                                # Add the entire word to next buffer
                                lines.append(
                                    text[start_index:end_index + index_difference] + " " * (index_difference * -1))

                                # Don't add the word in the previous_char_count
                                previous_char_count = char_count + index_difference

                                # Make add hyphen true
                                add_hyphen = True

                    if not add_hyphen:
                        # Append the buffer to the lines list
                        lines.append(text[start_index:end_index])

                        # Update the previous character counter
                        previous_char_count = char_count
        else:
            # Else if the text length can be fit into available space
            # Append the text to the lines list
            lines.append(text)

        ##########################
        # ALIGNMENT CALCULATIONS #
        ##########################

        # Loop through lines list and apply alignment to every line
        for line_text in lines:
            tags_data = self.get_pattern_data(line_text, "<.>", "<..>", "<...>")
            text_length = len(line_text) - tags_data["combined_length"]

            # print(f"Original Length: {len(line_text)}\nWithout Color: {text_length}")

            if align == Align.CENTER:
                # Do center alignment

                # Amount of space that should be on both sides
                amount_of_space_per_side = int((text_available_length / 2) - text_length / 2)

                # Left and right spaces are amount of space needed times the delimiter symbol
                space_left = printer_preset.delimiter_space_symbol * amount_of_space_per_side
                space_right = printer_preset.delimiter_space_symbol * amount_of_space_per_side

                # Check if all the alignment is good, if there are gaps fix them

                # Variable to track the side
                i = 0
                while ((len(space_left) + len(space_right)) + text_length) < text_available_length:
                    # Add empty space to right and left until it's good
                    if i == 0:
                        space_right += printer_preset.delimiter_space_symbol
                        i = 1
                    elif i == 1:
                        space_left += printer_preset.delimiter_space_symbol
                        i = 0

                # Update the list
                lines[
                    lines.index(line_text)] = f"{printer_preset.delimiter_left_color if enable_left_delimiter else ''}" \
                                              f"{printer_preset.delimiter_left if enable_left_delimiter else ''}" \
                                              f"{(printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_left_delimiter else '')}" \
                                              f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                              f"{printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right_color if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right if enable_right_delimiter else ''}"

                # Check i
            elif align == Align.LEFT:
                # Do left alignment

                # Amount of space on the right is just available space - the text length
                amount_of_space = int(text_available_length - text_length)

                # Space right is just the amount of space * the symbol
                space_right = amount_of_space * printer_preset.delimiter_space_symbol

                # There is no space on the left side because it is aligned there
                space_left = ""

                # Update the list
                lines[
                    lines.index(line_text)] = f"{printer_preset.delimiter_left_color if enable_left_delimiter else ''}" \
                                              f"{printer_preset.delimiter_left if enable_left_delimiter else ''}" \
                                              f"{(printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_left_delimiter else '')}" \
                                              f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                              f"{printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right_color if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right if enable_right_delimiter else ''}"
            else:
                # Do right alignment

                # Amount of space is just available space - the text length
                amount_of_space = int(text_available_length - text_length)

                # Space on the left is amount of space * the delimiter symbol
                space_left = printer_preset.delimiter_space_symbol * amount_of_space

                # There's no space on the right because the text is right aligned
                space_right = ""

                # Update the list
                lines[
                    lines.index(line_text)] = f"{printer_preset.delimiter_left_color if enable_left_delimiter else ''}" \
                                              f"{printer_preset.delimiter_left if enable_left_delimiter else ''}" \
                                              f"{(printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_left_delimiter else '')}" \
                                              f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                              f"{printer_preset.delimiter_space_symbol * printer_preset.delimiter_space_amount if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right_color if enable_right_delimiter else ''}" \
                                              f"{printer_preset.delimiter_right if enable_right_delimiter else ''}"

        ############
        # PRINTING #
        ############

        # Printing back separator
        if enable_back_separator:
            # Print the separator
            self.separator_line(position="back",
                                preset=separator_preset,
                                test_mode=True if test_mode == True else False,
                                testing_terminal_width=testing_terminal_width,
                                )

        # Loop through the lines list
        for line in lines:
            # Print all lines, with tags converted to color codes, add white to set color back to white
            print(self.tag_to_color(line + "<w>"))

        # Printing front separator
        if enable_front_separator:
            # Print the separator
            self.separator_line(position="front",
                                preset=separator_preset,
                                test_mode=True if test_mode == True else False,
                                testing_terminal_width=testing_terminal_width,
                                )

    def get_input(self, prompt: str = "", preset: Preset | InputPreset = None, separator_preset: Preset | SeparatorPreset = None,
                  enable_back_separator: bool = True, enable_front_separator: bool = True) -> str:
        """Get Input

        Args:
            prompt (str, optional): The prompt for the input. Defaults to "".
            preset (Preset | InputPreset, optional): The preset to use, if None the default will be used. Defaults to None.
            enable_back_separator (bool, optional): Whether to print the back separator. Defaults to True.
            enable_front_separator (bool, optional): Whether to print the front separator. Defaults to True.

        Returns:
            str: Input from user
        """
        #############
        # VARIABLES #
        #############
        user_input = str()

        preset = self.__default_preset.input_preset if preset is None else (preset if type(preset) is InputPreset else preset.input_preset)
        separator_preset = self.__default_preset.separator_preset if separator_preset is None else (separator_preset if type(separator_preset) is SeparatorPreset else separator_preset.separator_preset)

        #################
        # GETTING INPUT #
        #################

        # Print back separator
        if enable_back_separator:
            # Position is back and give the back preset
            self.separator_line(position="back", preset=separator_preset)

        # Print the input prompt
        user_input = input(
            f"{preset.delimiter_left_color}{preset.delimiter_left}{preset.delimiter_left_prompt_separator_left_color}{preset.delimiter_left_prompt_separator_left}{prompt}" \
            f"{preset.delimiter_left_prompt_separator_right_color}{preset.delimiter_left_prompt_separator_right}{preset.input_separator_left_color}{preset.input_separator_left}" \
            f"{preset.input_text_color}")

        # Print front separator
        if enable_front_separator:
            # Position is front and give the front preset
            self.separator_line(position="front", preset=separator_preset)

        #############
        # RETURNING #
        #############
        return user_input


#########
# TESTS #
#########
if __name__ == "__main__":
    ##############################
    # EXECUTION TIME MEASUREMENT #
    ##############################
    start_time = time.time()

    #######################
    # EXECUTION VARIABLES #
    #######################
    lines_printed = 0
    amount_of_times_to_test = 100000
    total_time_required = int()

    #########
    # TESTS #
    #########
    printer = Printer()

    start_time = time.time()

    # text_string = "Hi this is some <r>Red<w>, and some <b>Blue<w>, and some <lg>Light Green"
    # print(printer.get_pattern_data(text_string, r"<.>", r"<..>", r"<...>"))
    # printer.separator_line()
    # printer.separator_line(position="front", enable_left_delimiter=False)
    # printer.separator_line(enable_right_delimiter=False)
    # printer.separator_line(enable_left_delimiter=False, enable_right_delimiter=False)
    # default = printer.get_default_preset()
    # default.separator_preset.back_delimiter_space_amount = 10
    # printer.separator_line(preset=default)
    # printer.separator_line(enable_left_delimiter=False, preset=default)
    # printer.separator_line(enable_right_delimiter=False,preset=default)
    # printer.separator_line(enable_left_delimiter=False, enable_right_delimiter=False, preset=default)
    printer.set_default_preset(preset=Preset(separator_preset=Box.DoubleLiner().separator_preset, input_preset=Box.DoubleLiner().input_preset, printer_preset=Box.DoubleLiner().printer_preset))
    printer.print("Hi")
    printer.print("Hi", align=Align.LEFT)
    printer.print("Hi", align=Align.RIGHT)
    printer.print("Hi", enable_left_delimiter=False)
    printer.print("Hi", enable_right_delimiter=False)
    printer.get_input("Enter Something")

    end_time = time.time()

    execution_time = end_time - start_time

    ##############################
    # EXECUTION TIME MEASUREMENT #
    ##############################

    print(
        f"Execution took {execution_time :.10f}s with {lines_printed} {'lines' if lines_printed > 1 else 'line'} printed!")
