<h1 align="center">Fancy Print</h1>
<h3 align="center">An aesthetic replacement to print()</h3>


###### **Development Status:** Planning/Early-Stages

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

The `Printer` class has a `configure_options()` method that can be used to configure the options for the printer. The options can be configured as follows:

```python
printer.configure_options( delimiter_left: str, delimiter_right: str, delimiter_left_color: str,
                          delimiter_right_color: str, separator_back: str, separator_front: str,
                          separator_back_color: str, separator_front_color: str, delimiter_space: int)
```

The `Printer` class also has a `print()` method that can be used to print text. The `print()` method can be used as follows:

```python
printer.print(text: str, align="center", blank_character=" ", left_delimiter=True, right_delimiter=True, back_separator=True,
              front_separator=True)

# Example
printer.print("Hello World!", align="center", blank_character=" ", left_delimiter=True)

```

### Remember to keep your prints fancy! 😉
