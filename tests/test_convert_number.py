"""Test convert number."""

import pytest

from src.number_converter.main import convert_number


def test_unexpected_case() -> None:
    """Test unexpected case alias."""
    with pytest.raises(KeyError):
        convert_number(1, 'wrong case', 'N')  # type: ignore[arg-type]


def test_unexpected_gender() -> None:
    """Test unexpected gender alias."""
    with pytest.raises(KeyError):
        convert_number(1, 'F', 'wrong gender')  # type: ignore[arg-type]
