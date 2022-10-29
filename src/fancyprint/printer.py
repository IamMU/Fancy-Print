#######################
# IMPORTING LIBRARIES #
#######################
import os
import time
import re
from ftypes import Color, Preset, SeparatorPreset, PrinterPreset, Align

###########
# CLASSES #
###########


def give_color_codes_data(text: str, color_code_len: int = Color.COLOR_CODE_LENGTH) -> (bool, int):
    """Gives color code data of a string, namely if color is being used, amount of colors used, ...

    Parameters:
        text: The text to check
        color_code_len: Amount of space a color code has (Default: Color.COLOR_CODE_LENGTH)
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


def tag_to_color(text: str) -> str:
    """Converts a string with color tags to a string with color (codes)

    Parameters:
        text: The text to be converted
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


# TODO: Check if this is really needed
def colored_to_uncolored(text: str, tags: bool = True) -> str:
    """Converts a string with color codes to a non-colored string
    Parameters:
        text: The text to convert
        tags: Whether to convert from color tags"""
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


def separate_line(preset: SeparatorPreset | Preset = None,
                  delimiter_left: str = "|", delimiter_left_color: Color = Color.CYAN,
                  enable_left_delimiter: bool = True,
                  delimiter_right: str = "|", delimiter_right_color: Color = Color.CYAN,
                  enable_right_delimiter: bool = True,
                  delimiter_space_amount: int = 0, delimiter_space_symbol: str = " ",
                  separator_symbol: str = "-", separator_color: Color = Color.MAGENTA,
                  enable_separator: bool = True, test_mode: bool = False, testing_terminal_width: int = 100) -> None:
    """Prints a separator line

    Parameters:
        preset: Use a preset for customizations
        delimiter_left: Symbol for the left delimiter (Default: "|")
        delimiter_left_color: Color for the left delimiter (Default: Color.CYAN)
        enable_left_delimiter: Whether left delimiter is to be printed (Default: True)
        delimiter_right: Symbol for the right delimiter (Default: "|")
        delimiter_right_color: Color for the right delimiter (Default: Color.CYAN)
        enable_right_delimiter: Whether right delimiter is to be printed (Default: True)
        delimiter_space_symbol: Symbol for the delimiter spacing (Default: " ")
        delimiter_space_amount: Amount of delimiter space to be applied before separator symbol start/end
         (Default: 0)
        separator_symbol: Symbol for the separator (middle) (Default: "-")
        separator_color: Color for the separator (middle) (Default: Color.MAGENTA)
        enable_separator: Whether to enable the separator symbol, otherwise it will be " " (Default: True)
        test_mode: Whether to enable test mode (For developers only) (Default: False)
        testing_terminal_width: Artificial terminal width (For developers only) (Default: 100)
    """
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

    #############
    # Variables #
    #############

    # Getting terminal width (in chars) | If testing mode, using custom width
    if not test_mode:
        terminal_width = os.get_terminal_size().columns
    elif test_mode:
        terminal_width = testing_terminal_width

    # Make variables for the different areas of the separator line
    left_side = str()
    middle = str()
    right_side = str()

    ################
    # Calculations #
    ################

    # Left side
    if enable_left_delimiter:
        left_side = (delimiter_left_color + delimiter_left) + (delimiter_space_symbol * delimiter_space_amount)

    # Right side
    if enable_right_delimiter:
        right_side = (delimiter_space_symbol * delimiter_space_amount) + (delimiter_right_color + delimiter_right)

    # Middle

    # Get length of the other sides
    left_side_length = len(left_side)
    right_side_length = len(right_side)

    # Remove color code length if it is used
    left_side_length -= (Color.COLOR_CODE_LENGTH if left_side_length > 0 else 0)
    right_side_length -= (Color.COLOR_CODE_LENGTH if right_side_length > 0 else 0)

    # Calculate amount of space to exclude
    exclude_space = int(terminal_width - left_side_length - right_side_length)

    if enable_separator:
        middle = (separator_color + (separator_symbol * exclude_space))
    else:
        # Else insert blank space instead of symbol
        middle = " " * exclude_space

    ############
    # PRINTING #
    ############

    # Print the calculated parts to the screen | Add white at end to reset color
    print(left_side + middle + right_side + Color.WHITE)


def get_pattern_count(text: str, *patterns) -> int:
    """Returns amount of occurrences of x patterns in given string
    Parameters:
        text: The text to be used for searching
        *patterns: Patterns to search for"""

    #############
    # VARIABLES #
    #############
    results = list()

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

    # Return the result
    return len(results)


def pretty_print(text: str, align: Align = Align.CENTER,
                 preset: PrinterPreset | Preset = None,
                 separator_preset: SeparatorPreset | Preset = None,
                 delimiter_left: str = "|", delimiter_left_color: Color = Color.CYAN,
                 enable_left_delimiter: bool = True,
                 delimiter_space_amount: int = 0, delimiter_space_symbol: str = " ",
                 delimiter_right: str = "|", delimiter_right_color: Color = Color.CYAN,
                 enable_right_delimiter: bool = True,
                 separator_left_delimiter: str = "|", separator_left_delimiter_color: Color = Color.CYAN,
                 enable_left_separator_delimiter: bool = True,
                 separator_right_delimiter: str = "|", separator_right_delimiter_color: Color = Color.CYAN,
                 enable_right_separator_delimiter: bool = True,
                 separator_symbol: str = "-", separator_color: Color = Color.MAGENTA,
                 enable_separator_symbol: bool = True,
                 separator_delimiter_space_amount: int = 0, separator_delimiter_space_symbol: str = " ",
                 enable_back_separator: bool = True, enable_front_separator: bool = True,
                 hyphenation: bool = True,
                 test_mode: bool = False, testing_terminal_width: int = 100) -> None:
    """Prints text to console/terminal emulator.

    Parameters:
     text: The text to print
     align: The alignment for the text (Default: Align.CENTER)
     preset: Preset to use for customizations (Default: None)
     separator_preset: Preset to use for the separator (Default: None)
     delimiter_left: Symbol for the left delimiter (Default: "|")
     delimiter_left_color: Color for the left delimiter (Default: Color.CYAN)
     enable_left_delimiter: Whether to print the left delimiter (Default: True)
     delimiter_right: Symbol for the right delimiter (Default: "|")
     delimiter_right_color: Color for the right delimiter (Default: Color.CYAN)
     enable_right_delimiter: Whether to print the right delimiter (Default: True)
     delimiter_space_amount: Amount of delimiter space to print on both sides (Default: 0)
     delimiter_space_symbol: Symbol for the delimiter space area (Default: " ")
     separator_left_delimiter: Symbol for the left delimiter of both separators (Front/Back) (Default: "|")
     separator_left_delimiter_color: Color for the left delimiter of both separators (Front/Back)
      (Default: Color.CYAN)
     enable_left_separator_delimiter: Whether to enable left delimiter of both separators (Front/Back)
      (Default: True)
     separator_right_delimiter: Symbol for the right delimiter of both separators (Front/Back) (Default: "|")
     separator_right_delimiter_color: Color for the right delimiter of both separators (Front/Back)
      (Default: Color.CYAN)
     enable_right_separator_delimiter: Whether to enable the right delimiter both separators (Front/Back)
      (Default: True)
     separator_symbol: Symbol for both separators (Front/Back) (Default: "-")
     separator_color: Color for the separator symbol (Default: Color.MAGENTA)
     enable_separator_symbol: Whether to enable separator symbol (Default: True) | If False " " will be printed instead
     separator_delimiter_space_symbol: Symbol for the delimiter space in both separators (Front/Back)
      (Default: " ")
     separator_delimiter_space_amount: Amount of delimiter space for both separators (Front/Back) (Default: 0)
     enable_back_separator: Whether to print the back separator (Default: True)
     enable_front_separator: Whether to print the front separator (Default: True)
     test_mode: Whether to use artificial values (for developers only) (Default: False)
     testing_terminal_width: Artificial terminal width to be used (for developers only) (Default: False)
    """
    # Check if preset is None else assign the respective values to the respective variables

    # For printer preset
    if preset is None:
        # Do nothing if no preset is used
        pass
    else:
        # If preset is being used check if it's global or not, else raise TypeError
        if type(preset) is PrinterPreset:
            # Assign variables to respective values
            delimiter_left = preset.delimiter_left
            delimiter_left_color = preset.delimiter_left_color

            delimiter_right = preset.delimiter_right
            delimiter_right_color = preset.delimiter_right_color

            delimiter_space_symbol = preset.delimiter_space_symbol
            delimiter_space_amount = preset.delimiter_space_amount

            hyphenation = preset.hyphenation
        elif type(preset) is Preset:
            # Assign variables to respective printer preset values
            delimiter_left = preset.printer_preset.delimiter_left
            delimiter_left_color = preset.printer_preset.delimiter_left_color

            delimiter_right = preset.printer_preset.delimiter_right
            delimiter_right_color = preset.printer_preset.delimiter_right_color

            delimiter_space_symbol = preset.printer_preset.delimiter_space_symbol
            delimiter_space_amount = preset.printer_preset.delimiter_space_amount

            hyphenation = preset.printer_preset.hyphenation
        else:
            raise TypeError(f"Expected types: PrinterPreset or Preset | Found: {type(preset).__name__}")

    # For separator preset
    if separator_preset is None:
        # Do nothing if no preset is used
        pass
    else:
        # If preset is being used check if it's global or not, else raise TypeError
        if type(separator_preset) is SeparatorPreset:
            # Assign variables to respective values
            separator_left_delimiter = separator_preset.delimiter_left
            separator_left_delimiter_color = separator_preset.delimiter_left_color

            separator_right_delimiter = separator_preset.delimiter_right
            separator_right_delimiter_color = separator_preset.delimiter_right_color

            separator_delimiter_space_symbol = separator_preset.delimiter_space_symbol
            separator_delimiter_space_amount = separator_preset.delimiter_space_amount
        elif type(separator_preset) is Preset:
            # Assign variables to respective separator preset values
            separator_left_delimiter = separator_preset.separator_preset.delimiter_left
            separator_left_delimiter_color = separator_preset.separator_preset.delimiter_left_color

            separator_right_delimiter = separator_preset.separator_preset.delimiter_right
            separator_right_delimiter_color = separator_preset.separator_preset.delimiter_right_color

            separator_delimiter_space_symbol = separator_preset.separator_preset.delimiter_space_symbol
            separator_delimiter_space_amount = separator_preset.separator_preset.delimiter_space_amount
        else:
            raise TypeError(f"Expected types: SeparatorPreset or Preset | Found: {type(separator_preset).__name__}")

    #############
    # Variables #
    #############

    # Convert text tags to color
    # text = tag_to_color(text)

    # Length of text (Remove all color code lengths)
    text_length = len(text) - (Color.COLOR_CODE_LENGTH * give_color_codes_data(text)[1])

    # Get terminal width
    terminal_width = os.get_terminal_size().columns if not test_mode else testing_terminal_width

    # Available width for text
    text_available_length = terminal_width - (delimiter_space_amount * 2) - \
                            (enable_left_delimiter + enable_right_delimiter)

    # List that contains lines to print
    lines = list()

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
            tags_amount = get_pattern_count(text[previous_char_count:char_count], r"<.>", r"<..>", r"<...>")
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
            elif (char_count - previous_char_count) == text_available_length + (tags_amount * 3):
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
                            lines.append(text[start_index:end_index + index_difference] + " " * (index_difference * -1))

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
        text_length = len(line_text) - get_pattern_count(line_text, "<.>", "<..>", "<...>") * 3

        # print(f"Original Length: {len(line_text)}\nWithout Color: {text_length}")

        if align == Align.CENTER:
            # Do center alignment

            # Amount of space that should be on both sides
            amount_of_space_per_side = int((text_available_length / 2) - text_length / 2)

            # Left and right spaces are amount of space needed times the delimiter symbol
            space_left = delimiter_space_symbol * amount_of_space_per_side
            space_right = delimiter_space_symbol * amount_of_space_per_side

            # Check if all the alignment is good, if there are gaps fix them

            # Variable to track the side
            i = 0
            while ((len(space_left) + len(space_right)) + text_length) < text_available_length:
                # Add empty space to right and left until it's good
                if i == 0:
                    space_right += delimiter_space_symbol
                    i = 1
                elif i == 1:
                    space_left += delimiter_space_symbol
                    i = 0

            # Update the list
            lines[lines.index(line_text)] = f"{delimiter_left_color if enable_left_separator_delimiter else ''}" \
                                            f"{delimiter_left if enable_left_delimiter else ''}" \
                                            f"{(delimiter_space_symbol * delimiter_space_amount if enable_left_delimiter else '')}" \
                                            f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                            f"{delimiter_space_symbol * delimiter_space_amount if enable_right_delimiter else ''}" \
                                            f"{delimiter_right_color if enable_right_delimiter else ''}" \
                                            f"{delimiter_right if enable_right_delimiter else ''}"

            # Check i
        elif align == Align.LEFT:
            # Do left alignment

            # Amount of space on the right is just available space - the text length
            amount_of_space = int(text_available_length - text_length)

            # Space right is just the amount of space * the symbol
            space_right = amount_of_space * delimiter_space_symbol

            # There is no space on the left side because it is aligned there
            space_left = ""

            # Update the list
            lines[lines.index(line_text)] = f"{delimiter_left_color if enable_left_separator_delimiter else ''}" \
                                            f"{delimiter_left if enable_left_delimiter else ''}" \
                                            f"{(delimiter_space_symbol * delimiter_space_amount if enable_left_delimiter else '')}" \
                                            f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                            f"{delimiter_space_symbol * delimiter_space_amount if enable_right_delimiter else ''}" \
                                            f"{delimiter_right_color if enable_right_delimiter else ''}" \
                                            f"{delimiter_right if enable_right_delimiter else ''}"
        else:
            # Do right alignment

            # Amount of space is just available space - the text length
            amount_of_space = int(text_available_length - text_length)

            # Space on the left is amount of space * the delimiter symbol
            space_left = delimiter_space_symbol * amount_of_space

            # There's no space on the right because the text is right aligned
            space_right = ""

            # Update the list
            lines[lines.index(line_text)] = f"{delimiter_left_color if enable_left_separator_delimiter else ''}" \
                                            f"{delimiter_left if enable_left_delimiter else ''}" \
                                            f"{(delimiter_space_symbol * delimiter_space_amount if enable_left_delimiter else '')}" \
                                            f"{space_left}{Color.WHITE}{line_text}{space_right}" \
                                            f"{delimiter_space_symbol * delimiter_space_amount if enable_right_delimiter else ''}" \
                                            f"{delimiter_right_color if enable_right_delimiter else ''}" \
                                            f"{delimiter_right if enable_right_delimiter else ''}"

    ############
    # PRINTING #
    ############

    # Printing back separator
    if enable_back_separator:
        # Print the separator
        separate_line(delimiter_left=separator_left_delimiter, delimiter_left_color=separator_left_delimiter_color,
                      enable_left_delimiter=enable_left_separator_delimiter,
                      delimiter_right=separator_right_delimiter, delimiter_right_color=separator_right_delimiter_color,
                      enable_right_delimiter=enable_right_separator_delimiter,
                      delimiter_space_amount=separator_delimiter_space_amount,
                      delimiter_space_symbol=separator_delimiter_space_symbol,
                      separator_symbol=separator_symbol if enable_separator_symbol else ' ', separator_color=separator_color)

    # Loop through the lines list
    for line in lines:
        # Print all lines, with tags converted to color codes, add white to set color back to white
        print(tag_to_color(line + "<w>"))

    # Printing front separator
    if enable_front_separator:
        # Print the separator
        separate_line(delimiter_left=separator_left_delimiter, delimiter_left_color=separator_left_delimiter_color,
                      enable_left_delimiter=enable_left_separator_delimiter,
                      delimiter_right=separator_right_delimiter,
                      delimiter_right_color=separator_right_delimiter_color,
                      enable_right_delimiter=enable_right_separator_delimiter,
                      delimiter_space_amount=separator_delimiter_space_amount,
                      delimiter_space_symbol=separator_delimiter_space_symbol,
                      separator_symbol=separator_symbol if enable_separator_symbol else " ", separator_color=separator_color)


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

    #########
    # TESTS #
    #########

    ##############################
    # EXECUTION TIME MEASUREMENT #
    ##############################
    end_time = time.time()

    execution_time = end_time - start_time

    print(f"Execution took {execution_time}s with {lines_printed} {'lines' if lines_printed > 1 else 'line'} printed!")
