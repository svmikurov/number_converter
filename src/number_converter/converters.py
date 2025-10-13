"""Numeral converters."""

from typing import override

from .base import FactorConverterABC, NumberConverterABC
from .cases import HUNDREDS_ENDINGS, TENS_ENDINGS
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
    """The converter of integer to numeral.

    Parameters
    ----------
    numeral_cases : `dict[int, Case]`
        Mapping of numbers with their string representation,
        which has a special declension.

    """

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
        """Get a text representation of number with special declension.

        Parameters
        ----------
        case_number : `int`
            A number that has a special declension.
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
            If case number has no a special declension.

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
                f'Got unexpected case number: {case_number}, '
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

        Parameters
        ----------
        number : `int`
            The number that will be converted into a numeral.
        gender : `GenderType`
            Grammatical gender of a numeral.
        case : `CaseType`
            Case of the numeral.

        Returns
        -------
        `str`
            The string representation of integer.

        Raises
        ------
        ValueError
            If the number is not non-negative
            or not less than a billion.

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
        if hundreds_base := number // Factor.HUNDREDS:
            # Hundreds numerals 100, ..., 400 have a text definition
            # as grammatical rule exceptions.
            if hundreds_base in {1, 2, 3, 4}:
                hundreds = hundreds_base * Factor.HUNDREDS
                numerals.append(self.get_numeral(hundreds, gender, case))

            # Hundreds numerals 500, ..., 900 are created dynamically
            # via grammatical rule.
            else:
                numeral_base = self.get_numeral(hundreds_base, gender, case)
                numeral_ending = getattr(HUNDREDS_ENDINGS, CASES[case])
                numerals.append(numeral_base + str(numeral_ending))

        # The tens are converted separately.
        if tens_base := number // Factor.TENS % LAST_DIGIT_DIVISOR:
            if tens_base == 1:
                # Tens numerals 10, ..., 19 have a text definition
                # as grammatical rule exceptions.
                tens = number % Factor.HUNDREDS
                numerals.append(self.get_numeral(tens, gender, case))
                return ' '.join(numerals)

            elif tens_base in {2, 3, 4, 9}:
                # Tens numerals 20, 30, 40, 90 have a text definition.
                tens = tens_base * Factor.TENS
                numerals.append(self.get_numeral(tens, gender, case))

            else:
                # The tens 50, ..., 80 are created dynamically
                # via grammatical rule.
                numeral_base = self.get_numeral(tens_base, gender, case)
                numeral_ending = getattr(TENS_ENDINGS, CASES[case])
                numerals.append(numeral_base + str(numeral_ending))

        # The units are converted separately.
        if units := number % LAST_DIGIT_DIVISOR:
            numerals.append(self.get_numeral(units, gender, case))

        return ' '.join(numerals)


class FactorConverter(FactorConverterABC):
    """The converter of number factor to numeral.

    Attributes
    ----------
    factor_cases : `dict[Factor, dict[CaseGroup, Case]]`
        Mapping of factor enumeration instance with factor case groups.

    """

    def __init__(
        self,
        factor_cases: dict[Factor, dict[CaseGroup, Case]],
    ) -> None:
        """Construct the converter."""
        self._factor_cases = factor_cases

    @override
    def get_text(self, number: int, case: CaseType, factor: Factor) -> str:
        """Get the numeral for number factor.

        Parameters
        ----------
        number : `int`
            The number that comes before the factor.
            Determines the declination of the factor.
        case : `CaseType`
            Grammatical case for the factor.
        factor: `Factor`
            The factor to convert.

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
