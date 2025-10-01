"""Test the convert to numerals."""

import pytest

from src.number_converter.main import convert_number
from src.number_converter.types import CaseType, GenderType


@pytest.mark.parametrize(
    'number, gender, case, word',
    [
        (1, 'M', 'N', 'один'),
        (1, 'F', 'G', 'одной'),
        (1, 'N', 'D', 'одному'),
        (5, 'M', 'A', 'пять'),
        (6, 'F', 'I', 'шестью'),
        (7, 'N', 'P', 'семи'),
        (50, 'M', 'N', 'пятьдесят'),
        (60, 'F', 'G', 'шестидесяти'),
        (70, 'N', 'I', 'семьюдесятью'),
    ],
)
def test_convert_numerals(
    number: int,
    gender: GenderType,
    case: CaseType,
    word: str,
) -> None:
    """Test the convert to numerals."""
    assert convert_number(number, gender, case) == word
