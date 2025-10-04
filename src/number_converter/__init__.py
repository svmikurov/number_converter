"""Converting an integer to text in words."""

__all__ = ['convert_number']

from functools import partial

from .cases import FACTOR_CASES, NUMERAL_CASES
from .main import FactorConverter, NumberConverter, convert_number_

convert_number = partial(
    convert_number_,
    number_converter=NumberConverter(NUMERAL_CASES),
    factor_converter=FactorConverter(FACTOR_CASES),
)
