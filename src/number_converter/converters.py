"""To numeral a converters."""

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

LAST_DIGIT_DIVISOR = 10


class NumberConverter(NumberConverterABC):
    """The converter of integer to numeral."""

    def __init__(self, numeral_cases: dict[int, Case]) -> None:
        """Construct the converter."""
        self._numeral_cases = numeral_cases

    @override
    def get_numeral(
        self,
        case_number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get the text representation of number.

        Applies only with numbers that have a specific declension rule.

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

        Example
        -------
        >>> from .cases import NUMERAL_CASES
        >>> converter = NumberConverter(NUMERAL_CASES)
        >>> converter.get_numeral(12, 'M', 'I')
        'двенадцатью'
        >>> converter.get_numeral(1, 'F', 'P')
        'одной'

        """
        try:
            cases = self._numeral_cases[case_number]
        except KeyError as e:
            raise ValueError(
                f'Got unexpected case number, '
                f'use {sorted(self._numeral_cases)}'
            ) from e

        case_obj: Gender | str = getattr(cases, CASES[case])
        try:
            return getattr(case_obj, GENDERS[gender])  # type: ignore[no-any-return]
        except AttributeError:
            return case_obj  # type: ignore[return-value]

    @override
    def get_text(
        self,
        number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get numeral in the thousand factor.

        >>> from .cases import NUMERAL_CASES
        >>> converter = NumberConverter(NUMERAL_CASES)
        >>> converter.get_text(31, 'M', 'G')
        'тридцати одного'
        >>> converter.get_text(122, 'N', 'I')
        'ста двадцатью двумя'
        """
        if not (0 < number <= 999):
            raise ValueError(f'Number must be between 1 and 999, got {number}')

        numerals: list[str] = []

        # The hundreds are converted separately.
        if hundreds := number // Factor.HUNDREDS:
            hundreds_part = hundreds * Factor.HUNDREDS
            numeral = self.get_numeral(hundreds_part, gender, case)
            numerals.append(numeral)

        if tens := number // Factor.TENS % LAST_DIGIT_DIVISOR:
            if tens == 1:
                # The numbers 10, ..., 19 are converted separately.
                tens_part = number % Factor.HUNDREDS
                numeral = self.get_numeral(tens_part, gender, case)
                numerals.append(numeral)
                return ' '.join(numerals)
            else:
                # The tens 20, 30, ..., 90 are converted separately.
                tens_part = tens * Factor.TENS
                numeral = self.get_numeral(tens_part, gender, case)
                numerals.append(numeral)

        # The units are converted separately.
        if units := number % LAST_DIGIT_DIVISOR:
            numeral = self.get_numeral(units, gender, case)
            numerals.append(numeral)

        return ' '.join(numerals)


class FactorConverter(FactorConverterABC):
    """The converter of number period to numeral.

    Attributes
    ----------
    factor_cases : `dict[Factor, dict[CaseGroup, Case]]`
        Mapping of factor enumeration instance with case groups.

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
        case_group = CaseGroup.from_number(number)
        cases = self._factor_cases[factor][case_group]
        return getattr(cases, CASES[case])  # type: ignore[no-any-return]
