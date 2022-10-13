<h1 align="center">Fancy Print</h1>
<h3 align="center">An aesthetic replacement to print()</h3>

<h6 align="center"><b>Development Status:</b> Planning/Early-Stages</h6>

<p align="center">
  <a href="https://pypi.org/project/fancyprint/">
	<img src="https://img.shields.io/pypi/v/fancyprint?color=blue&label=PyPI&logo=python&logoColor=white&style=for-the-badge" alt="PyPI">
  </a>
</p>

## About

Fancy Print is a Python package that provides a replacement to the built-in `print()` function. It is designed to be aesthetically pleasing and easy to use.

## Installation

Fancy Print is available on PyPI. You can install it using `pip`:

```bash
pip install fancyprint
```

## Usage

Fancy Print provides a class called 'Printer' that can be used to replace the built-in `print()` function. It can be used as follows:

```python
from fancyprint import Printer

printer = Printer()
```

The `Printer` class has a `configure_options()` method that can be used to configure the options for the printer. We have a `PrinterConfig` type for configurations. It is to be passed to `print()` to modify the configurations for that statement. For Alignment there is an Enum [ Align.LEFT, Align.RIGHT, Align.CENTER ]. The options can be configured as follows:

```python
printer.configure_options(PrinterConfig(delimiter_left="|", delimiter_right="|",
                              delimiter_left_color="cyan", delimiter_right_color="cyan", separator_back="-",
                              separator_front="-", separator_front_color="magenta", separator_back_color="magenta",
                              delimiter_space=2))
```

The `Printer` class also has a `print()` method that can be used to print text. The `print()` method can be used as follows:

```python
from src.fancyprint import Printer
from src.fancyprint.helpers.types import PrintConfig
from src.fancyprint.helpers.constants import Align
printer=Printer()
printer.print("This is some text in the center", PrintConfig(align=Align.CENTER, blank_character=" ", left_delimiter=True, right_delimiter=True, back_separator=True,
              front_separator=True))

# Example
printer.print("Hello World!", PrintConfig(align=Align.CENTER, blank_character=" ", left_delimiter=True))

```

### Remember to keep your prints fancy! 😉
