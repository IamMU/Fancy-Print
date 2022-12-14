#######################
# IMPORTING LIBRARIES #
#######################
from dataclasses import dataclass
from .separator_preset import SeparatorPreset
from .printer_preset import PrinterPreset
from .input_preset import InputPreset


################
# Data Classes #
################
@dataclass
class Preset:
    """The Preset dataclass can be used to create a universal Preset for fancyprint"""
    # The separator preset
    separator_preset: SeparatorPreset = SeparatorPreset()

    # The print preset
    printer_preset: PrinterPreset = PrinterPreset()

    # The input preset
    input_preset: InputPreset = InputPreset()
