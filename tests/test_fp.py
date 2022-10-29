import os
from fancyprint import pretty_print
import pytest


def test_sample():
    with not pytest.raises(OSError):
        pretty_print("hi", test_mode=True, testing_terminal_width=150)
