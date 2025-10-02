"""Function for converting an integer to text in words."""

import logging

from . import numbers
from .types import CASES, GENDERS, Case, CaseType, Gender, GenderType

log = logging.getLogger(__name__)

MAX_NUMBER = 999_999_999_999


class NumberConverter:
    """The converter of integer to numeral."""

    def __init__(
        self,
        gender: GenderType,
        case: CaseType,
        number_mapping: dict[int, Case] = numbers.numerals,
    ) -> None:
        """Construct the converter."""
        self._gender = self._set_gender(gender)
        self._case = self._set_case(case)
        self._number_mapping = number_mapping

    def get_text(self, number: int) -> str:
        """Get the text representation of number."""
        cases = self._number_mapping.get(number)
        case: Gender | str = getattr(cases, self._case)
        try:
            return str(getattr(case, self._gender))
        except AttributeError:
            return str(case)

    def _set_gender(self, value: GenderType) -> str:
        try:
            return GENDERS[value]
        except KeyError:
            log.exception(
                f"Error number converting, got unexpected '{value}' alias for "
                f'gender. Use {GenderType} aliases.'
            )
            raise

    def _set_case(self, value: CaseType) -> str:
        try:
            return CASES[value]
        except KeyError:
            log.exception(
                f"Error number converting, got unexpected '{value}' alias for "
                f'case. Use {CaseType} aliases.'
            )
            raise


def _validate_number(number: int) -> None:
    if number < 0 or number > MAX_NUMBER:
        msg = f'Error number converting, use 0 <= number < {MAX_NUMBER}'
        log.error(msg)
        raise ValueError(msg)

    if not isinstance(number, int):
        msg = f'Expected `int` number type, got `{type(number).__name__}`'
        log.error(msg)
        raise ValueError(msg)


def convert_number(number: int, gender: GenderType, case: CaseType) -> str:
    """Return the word representation of number."""
    _validate_number(number)
    converter = NumberConverter(gender, case)
    return converter.get_text(number)
