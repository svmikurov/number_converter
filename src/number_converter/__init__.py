"""Converting an integer to text in words."""

__all__ = ['convert_number']

from functools import partial

from . import numbers
from .main import _convert_number, _NumberConverter, _PeriodConvertor

convert_number = partial(
    _convert_number,
    number_converter=_NumberConverter(
        number_mapping=numbers.numerals,
    ),
    range_converter=_PeriodConvertor(
        period_mapping=numbers.period_cases,
    ),
)
