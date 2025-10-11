"""Converting an integer to numeral."""

from .base import FactorConverterABC, NumberConverterABC
from .types import CaseType, Factor, GenderType

MAX_NUMBER = 999_999_999_999


def validate_number(number: int) -> None:
    """Validate the number for numeral conversion."""
    if not isinstance(number, int):
        raise TypeError(f'Expected integer, got {type(number).__name__}')

    if number < 0:
        raise ValueError(f'Number must be non-negative, got {number}')

    if number > MAX_NUMBER:
        raise ValueError(
            f'Number too large: {number}. Maximum supported: {MAX_NUMBER}'
        )


def convert_number_(
    number: int,
    gender: GenderType,
    case: CaseType,
    number_converter: NumberConverterABC,
    factor_converter: FactorConverterABC,
) -> str:
    """Return the word representation of number."""
    validate_number(number)

    # The number zero is converted separately.
    # The other number parts are separated by taking the
    # remainder from the division, which may also be zero.
    if number == 0:
        return number_converter.get_numeral(0, gender, case)

    remaining = number
    number_part_gender = gender
    factor_exponent = 0
    parts: list[str] = []

    while remaining:
        number_part = remaining % Factor.THOUSANDS
        remaining //= Factor.THOUSANDS
        factor = Factor(Factor.THOUSANDS**factor_exponent)

        if factor >= Factor.THOUSANDS and number_part:
            parts.append(factor_converter.get_text(number_part, case, factor))

            # The factor determines the gender of the number part.
            number_part_gender = factor.gender

        if number_part:
            numeral_part = number_converter.get_text(
                number_part,
                number_part_gender,
                case,
            )
            parts.append(numeral_part)

        factor_exponent += 1

    parts.reverse()
    return ' '.join(parts)
