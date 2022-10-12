from typing import Optional
from pydantic import BaseModel, validator
from colorama import Fore
from .constants import COLORS, LogLevel, Align

class PrinterConfig(BaseModel):
        delimiter_left: Optional[str] = "|"
        delimiter_left_color: Optional[str] = Fore.CYAN
        delimiter_right: Optional[str] = "|"
        delimiter_right_color: Optional[str] = Fore.CYAN

        delimiter_space: Optional[int] = 2

        separator_back: Optional[str] = "-"
        separator_back_color: Optional[str] = Fore.MAGENTA
        separator_front: Optional[str] = "-"
        separator_front_color: Optional[str] = Fore.MAGENTA

        @validator("delimiter_left_color", each_item=True)
        def validate_delimiter_left_color(cls, v):
            return COLORS.get(v, Fore.CYAN)

        @validator("delimiter_right_color", each_item=True)
        def validate_delimiter_right_color(cls, v):
            return COLORS.get(v, Fore.CYAN)

        @validator("separator_back_color", each_item=True)
        def validate_separator_back_color(cls, v):
            return COLORS.get(v, Fore.MAGENTA)

        @validator("separator_front_color", each_item=True)
        def validate_separator_front_color(cls, v):
            return COLORS.get(v, Fore.MAGENTA)

        class Config:
            validate_assignment = True


class LogConfig(BaseModel):
        level: Optional[LogLevel] = LogLevel.INFO
        hierarchy_level: Optional[int] = 0
        color: Optional[str] = Fore.WHITE
        level_padding: Optional[int] = 8
        level_padding_char: Optional[str] = " "

        @validator("color", each_item=True)
        def validate_log_level_color(cls, v):
            return COLORS.get(v, Fore.GREEN)

        class Config:
            validate_assignment = True


class PrintConfig(BaseModel):
        align: Optional[Align] = Align.CENTER
        blank_character: Optional[str] = " "
        left_delimiter: Optional[bool] = True
        right_delimiter: Optional[bool] = True
        back_separator: Optional[bool] = True
        front_separator: Optional[bool] = True

        class Config:
            validate_assignment = True