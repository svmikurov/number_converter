"""Testing exceptions raised when converting a number."""

import pytest

from src.number_converter import convert_number
from src.number_converter.types import CaseType, GenderType


@pytest.mark.parametrize(
    'number, gender, case',
    [
        (1, 'wrong case', 'N'),
        (1, 'F', 'wrong gender'),
    ],
)
def test_flag_validation(
    number: int,
    gender: GenderType,
    case: CaseType,
) -> None:
    """Test the unexpected flag."""
    with pytest.raises(KeyError):
        convert_number(number, gender, case)


@pytest.mark.parametrize(
    'number, gender, case',
    [
        (-1, 'F', 'N'),
        (10**12, 'F', 'N'),
    ],
)
def test_number_validation(
    number: int,
    gender: GenderType,
    case: CaseType,
) -> None:
    """Test unexpected number value."""
    with pytest.raises(ValueError):
        convert_number(number, gender, case)
