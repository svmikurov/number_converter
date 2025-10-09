"""Converting an integer to numeral."""

from typing import override

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
    """The converter of integer to numeral.

    Example
    -------
    >>> from .cases import NUMERAL_CASES
    >>> converter = NumberConverter(NUMERAL_CASES)
    >>> converter.get_text(12, 'M', 'I')
    'двенадцатью'
    >>> converter.get_text(1, 'F', 'P')
    'одной'

    """

    def __init__(self, numeral_cases: dict[int, Case]) -> None:
        """Construct the converter."""
        self._numeral_cases = numeral_cases

    @override
    def get_text(
        self,
        case_number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get the text representation of number.

        Parameters
        ----------
        case_number : `int`
            A number that has a specific declension rule.
        gender : `GenderType`
            An abbreviation that determines the gender of a declension.
        case : `CaseType`
            An abbreviation that determines the case of a declension.

        Returns
        -------
        `str`
            Numeral. The textual representation of the number.

        Raises
        ------
        ValueError
            If case number has no a specific declension rule.

        """
        try:
            cases = self._numeral_cases[case_number]
        except KeyError as e:
            raise ValueError(
                f'Got unexpected case number, '
                f'use {sorted(self._numeral_cases.keys())}'
            ) from e

        case_obj: Gender | str = getattr(cases, CASES[case])
        try:
            return getattr(case_obj, GENDERS[gender])  # type: ignore[no-any-return]
        except AttributeError:
            return case_obj  # type: ignore[return-value]


class FactorConverter(FactorConverterABC):
    """The converter of number period to numeral.

    Attributes
    ----------
    factor_cases : `dict[Factor, dict[CaseGroup, Case]]`
        Mapping of factor enumeration instance with case groups.

    Example
    -------
    >>> from .cases import FACTOR_CASES
    >>> from .types import Factor
    >>> converter = FactorConverter(FACTOR_CASES)
    >>> converter.get_text(12, 'I', Factor(1_000_000))
    'миллионами'
    >>> converter.get_text(1, 'P', Factor(1_000))
    'тысяче'

    """

    def __init__(
        self,
        factor_cases: dict[Factor, dict[CaseGroup, Case]],
    ) -> None:
        """Construct the converter."""
        self._factor_cases = factor_cases

    @override
    def get_text(self, number: int, case: CaseType, factor: Factor) -> str:
        """Get the number factor numeral.

        Parameters
        ----------
        number : `int`
            The number that comes before the factor.
            Determines the declination of the factor.
        case : `CaseType`
            An abbreviation that determines the case of a declension.
        factor: `Factor`
            The factor enumeration instance.

        Returns
        -------
        `str`
            Numeral. The textual representation of the factor.

        """
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
        if number_part := remaining % Factor.THOUSANDS:
            factor = Factor(Factor.THOUSANDS**factor_exponent)

            # Factors of a number are converted separately.
            if factor >= Factor.THOUSANDS:
                factor_part = factor_converter.get_text(
                    number_part,
                    case,
                    factor,
                )
                parts.append(factor_part)

            numeral_part = get_numeral(
                number_converter,
                number_part,
                # The factor determines the gender of the multiplicand.
                gender if factor < Factor.THOUSANDS else factor.gender,
                case,
            )
            parts.append(numeral_part)

        remaining //= Factor.THOUSANDS
        factor_exponent += 1

    parts.reverse()
    return ' '.join(parts)
