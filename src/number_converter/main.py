"""Function for converting an integer to text in words."""

from . import numbers
from .types import CASES, GENDERS, Case, CaseType, GenderType


class NumberConverter:
    """The converter of integer to text in words."""

    def __init__(
        self,
        gender: GenderType,
        case: CaseType,
        number_mapping: dict[int, Case] = numbers.simple_numbers,
    ) -> None:
        """Construct the converter."""
        self._gender = gender
        self._case = case
        self._number_mapping = number_mapping

    def get_text(self, number: int) -> str:
        """Get the text representation of number."""
        case = self._number_mapping.get(number)
        gender = getattr(case, CASES[self._case])
        word: str = getattr(gender, GENDERS[self._gender])
        return word


def convert_number(number: int, gender: GenderType, case: CaseType) -> str:
    """Return the word representation of number."""
    converter = NumberConverter(gender, case)
    return converter.get_text(number)
