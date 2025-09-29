"""Test a simple numbers converting."""

import pytest

from src.number_converter.main import convert_number
from src.number_converter.types import CaseType, GenderType


@pytest.mark.parametrize(
    'number, gender, case, word',
    [
        (1, 'M', 'N', 'один'),
        (1, 'F', 'N', 'одна'),
        (1, 'N', 'N', 'одно'),
        (1, 'F', 'P', 'одной'),
    ],
)
def test_convert_simple_number(
    number: int,
    gender: GenderType,
    case: CaseType,
    word: str,
) -> None:
    """Test the simple number converting."""
    assert convert_number(number, gender, case) == word
