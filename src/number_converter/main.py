"""Converting an integer to numeral."""

from .base import FactorConverterABC, NumberConverterABC
from .types import (
    CASES,
    GENDERS,
    Case,
    CaseGroup,
    CaseType,
    Factor,
    Gender,
    GenderType,
)

MAX_NUMBER = 999_999_999_999
LAST_DIGIT_DIVISOR = 10


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


def get_numeral(
    converter: NumberConverterABC,
    number: int,
    gender: GenderType,
    case: CaseType,
) -> str:
    """Get numeral in the thousand factor.

    >>> from .cases import NUMERAL_CASES
    >>> converter = NumberConverter(NUMERAL_CASES)
    >>> get_numeral(converter, 31, 'M', 'G')
    'тридцати одного'
    >>> get_numeral(converter, 122, 'N', 'I')
    'ста двадцатью двумя'
    """
    if not (0 <= number <= 999):
        raise ValueError(f'Number must be between 0 and 999, got {number}')

    numerals: list[str] = []

    # The hundreds are converted separately.
    if hundreds := number // Factor.HUNDREDS:
        hundreds_part = hundreds * Factor.HUNDREDS
        numeral = converter.get_text(hundreds_part, gender, case)
        numerals.append(numeral)

    if tens := number // Factor.TENS % LAST_DIGIT_DIVISOR:
        if tens == 1:
            # The numbers 10, ..., 19 are converted separately.
            tens_part = number % Factor.HUNDREDS
            numeral = converter.get_text(tens_part, gender, case)
            numerals.append(numeral)
            return ' '.join(numerals)
        else:
            # The tens 20, 30, ..., 90 are converted separately.
            tens_part = tens * Factor.TENS
            numeral = converter.get_text(tens_part, gender, case)
            numerals.append(numeral)

    # The units are converted separately.
    if units := number % LAST_DIGIT_DIVISOR:
        numeral = converter.get_text(units, gender, case)
        numerals.append(numeral)

    return ' '.join(numerals)


class NumberConverter(NumberConverterABC):
    """The converter of integer to numeral."""

    def __init__(self, numeral_cases: dict[int, Case]) -> None:
        """Construct the converter."""
        self._numeral_cases = numeral_cases

    def get_text(
        self,
        case_number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get the text representation of number."""
        cases = self._numeral_cases[case_number]
        case_obj: Gender | str = getattr(cases, CASES[case])
        try:
            return getattr(case_obj, GENDERS[gender])  # type: ignore[no-any-return]
        except AttributeError:
            return case_obj  # type: ignore[return-value]


class FactorConverter(FactorConverterABC):
    """The converter of number period to numeral."""

    def __init__(
        self,
        factor_cases: dict[Factor, dict[CaseGroup, Case]],
    ) -> None:
        """Construct the converter."""
        self._factor_cases = factor_cases

    def get_text(self, number: int, case: CaseType, factor: Factor) -> str:
        """Get the number period numeral."""
        case_group = CaseGroup.from_number(number)
        cases = self._factor_cases[factor][case_group]
        return getattr(cases, CASES[case])  # type: ignore[no-any-return]


def convert_number_(
    number: int,
    gender: GenderType,
    case: CaseType,
    number_converter: NumberConverterABC,
    factor_converter: FactorConverterABC,
) -> str:
    """Return the word representation of number."""
    validate_number(number)

    if number == 0:
        return number_converter.get_text(0, gender, case)

    remaining = number
    factor_exponent = 0
    parts: list[str] = []

    while remaining:
        # The number is determines by parts
        # that are multiples of a thousand.
        digits = remaining % Factor.THOUSANDS
        remaining //= Factor.THOUSANDS

        if digits > 0:
            factor = Factor(Factor.THOUSANDS**factor_exponent)

            numeral_part = get_numeral(
                number_converter,
                digits,
                # The factor determines the gender of the multiplicand.
                gender if factor < Factor.THOUSANDS else factor.gender,
                case,
            )
            parts.insert(0, numeral_part)

            # Factors of a number are converted separately.
            if factor >= Factor.THOUSANDS:
                factor_text = factor_converter.get_text(digits, case, factor)
                parts.insert(1, factor_text)

        factor_exponent += 1

    return ' '.join(parts)
