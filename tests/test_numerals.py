"""Test number conversion to Russian numerals."""

import pytest

from src.number_converter import convert_number
from src.number_converter.types import CaseType, GenderType

HAVE_NO_GENDER = 'M'
"""Stub for gender parameter if numeral have no gender.
"""

HUNDRED_FACTOR = [
    (0, 'M', 'N', 'ноль'),
    (0, 'F', 'G', 'ноля'),
    (0, 'N', 'D', 'нолю'),
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
    (1_000, 'F', 'N', 'одна тысяча'),
    (1_001, 'M', 'N', 'одна тысяча один'),
    (2_002, 'N', 'N', 'две тысячи два'),
    (13_000, HAVE_NO_GENDER, 'N', 'тринадцать тысяч'),
    (30_000, HAVE_NO_GENDER, 'N', 'тридцать тысяч'),
    (31_000, HAVE_NO_GENDER, 'N', 'тридцать одна тысяча'),
    (32_000, HAVE_NO_GENDER, 'N', 'тридцать две тысячи'),
    (33_000, HAVE_NO_GENDER, 'N', 'тридцать три тысячи'),
    (34_000, HAVE_NO_GENDER, 'N', 'тридцать четыре тысячи'),
    (35_000, HAVE_NO_GENDER, 'N', 'тридцать пять тысяч'),
    (36_000, HAVE_NO_GENDER, 'N', 'тридцать шесть тысяч'),
    (37_000, HAVE_NO_GENDER, 'N', 'тридцать семь тысяч'),
    (38_000, HAVE_NO_GENDER, 'N', 'тридцать восемь тысяч'),
    (39_000, HAVE_NO_GENDER, 'N', 'тридцать девять тысяч'),
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
MILLION_FACTOR = [
    (14_000_000, HAVE_NO_GENDER, 'N', 'четырнадцать миллионов'),
    (40_000_000, HAVE_NO_GENDER, 'N', 'сорок миллионов'),
    (41_000_000, HAVE_NO_GENDER, 'N', 'сорок один миллион'),
    (42_000_000, HAVE_NO_GENDER, 'N', 'сорок два миллиона'),
    (43_000_000, HAVE_NO_GENDER, 'N', 'сорок три миллиона'),
    (44_000_000, HAVE_NO_GENDER, 'N', 'сорок четыре миллиона'),
    (45_000_000, HAVE_NO_GENDER, 'N', 'сорок пять миллионов'),
    (46_000_000, HAVE_NO_GENDER, 'N', 'сорок шесть миллионов'),
    (47_000_000, HAVE_NO_GENDER, 'N', 'сорок семь миллионов'),
    (48_000_000, HAVE_NO_GENDER, 'N', 'сорок восемь миллионов'),
    (49_000_000, HAVE_NO_GENDER, 'N', 'сорок девять миллионов'),
    (
        999_999_999_999,
        HAVE_NO_GENDER,
        'I',
        'девятьюстами девяноста девятью миллиардами '
        'девятьюстами девяноста девятью миллионами '
        'девятьюстами девяноста девятью тысячами '
        'девятьюстами девяноста девятью',
    ),
    (
        999_000_000_000,
        HAVE_NO_GENDER,
        'I',
        'девятьюстами девяноста девятью миллиардами',
    ),
    (
        11_001_001_001,
        'N',
        'A',
        'одиннадцать миллиардов один миллион одну тысячу одно',
    ),
]


@pytest.mark.parametrize(
    'number, gender, case, numeral',
    HUNDRED_FACTOR + THOUSAND_FACTOR + MILLION_FACTOR,
)
def test_convert_numerals(
    number: int,
    gender: GenderType,
    case: CaseType,
    numeral: str,
) -> None:
    """Test the convert to numerals."""
    assert convert_number(number, gender, case) == numeral
