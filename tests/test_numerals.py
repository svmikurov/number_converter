"""Test the convert to numerals."""

import pytest

from src.number_converter.main import convert_number
from src.number_converter.types import CaseType, GenderType

HAVE_NO_GENDER = 'M'
"""Stub for gender parameter if numeral have no gender.
"""

HUNDRED_FACTOR = [
    (1, 'M', 'N', 'один'),
    (1, 'F', 'G', 'одной'),
    (1, 'N', 'D', 'одному'),
    (2, 'M', 'A', 'два'),
    (2, 'F', 'I', 'двумя'),
    (2, 'N', 'P', 'двух'),
    (5, HAVE_NO_GENDER, 'A', 'пять'),
    (6, HAVE_NO_GENDER, 'I', 'шестью'),
    (7, HAVE_NO_GENDER, 'P', 'семи'),
    (10, HAVE_NO_GENDER, 'N', 'десять'),
    (19, HAVE_NO_GENDER, 'N', 'девятнадцать'),
    (20, HAVE_NO_GENDER, 'N', 'двадцать'),
    (22, 'F', 'N', 'двадцать две'),
    (50, HAVE_NO_GENDER, 'N', 'пятьдесят'),
    (60, HAVE_NO_GENDER, 'G', 'шестидесяти'),
    (70, HAVE_NO_GENDER, 'I', 'семьюдесятью'),
    (200, HAVE_NO_GENDER, 'N', 'двести'),
    (249, HAVE_NO_GENDER, 'N', 'двести сорок девять'),
    (300, HAVE_NO_GENDER, 'G', 'трёхсот'),
    (400, HAVE_NO_GENDER, 'D', 'четырёмстам'),
    (500, HAVE_NO_GENDER, 'G', 'пятисот'),
    (600, HAVE_NO_GENDER, 'D', 'шестистам'),
    (700, HAVE_NO_GENDER, 'A', 'семьсот'),
    (800, HAVE_NO_GENDER, 'I', 'восьмьюстами'),
    (900, HAVE_NO_GENDER, 'P', 'девятистах'),
]
THOUSAND_FACTOR = [
    (
        154_323,
        'M',
        'N',
        'сто пятьдесят четыре тысячи триста двадцать три',
    ),
    (
        154_323,
        'M',
        'I',
        'ста пятьюдесятью четырьмя тысячами тремястами двадцатью тремя',
    ),
]


@pytest.mark.parametrize(
    'number, gender, case, numeral',
    HUNDRED_FACTOR + THOUSAND_FACTOR,
)
def test_convert_numerals(
    number: int,
    gender: GenderType,
    case: CaseType,
    numeral: str,
) -> None:
    """Test the convert to numerals."""
    assert convert_number(number, gender, case) == numeral
