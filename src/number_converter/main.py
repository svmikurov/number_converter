"""Function for converting an integer to text in words."""

import logging

from . import numbers
from .types import CASES, GENDERS, Case, CaseType, Gender, GenderType

log = logging.getLogger(__name__)

MAX_NUMBER = 999_999_999_999

HUNDRED_FACTOR = 100
TEN_FACTOR = 10
LAST_DIGIT_DEVISOR = 10


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


def _get_count_cycles(number: int) -> int:
    """Get count of cycles by number length.

    Example:
    -------
        >>> _get_count_cycles(444)
        1
        >>> _get_count_cycles(4_444)
        2

    """
    digit_count_on_cycle = 3
    return int(int(len(str(number)) - 1) // digit_count_on_cycle) + 1


def convert_number(number: int, gender: GenderType, case: CaseType) -> str:
    """Return the word representation of number."""
    _validate_number(number)
    converter = NumberConverter(gender, case)
    count_cycles = _get_count_cycles(number)
    numeral_parts: list[str] = []

    for _ in range(count_cycles):
        if hundreds_digit := number // HUNDRED_FACTOR % LAST_DIGIT_DEVISOR:
            numeral_parts.append(
                converter.get_text(hundreds_digit * HUNDRED_FACTOR)
            )

        if tens_digit := number // TEN_FACTOR % LAST_DIGIT_DEVISOR:
            if tens_digit == 1:
                numeral_parts.append(
                    converter.get_text(number % HUNDRED_FACTOR)
                )
                continue
            else:
                numeral_parts.append(
                    converter.get_text(tens_digit * TEN_FACTOR)
                )

        if units_digit := number % LAST_DIGIT_DEVISOR:
            numeral_parts.append(converter.get_text(units_digit))

    return ' '.join(numeral_parts)
