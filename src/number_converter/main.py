"""Function for converting an integer to text in words."""

import logging

from .base import NumberConverterABC, PeriodConvertorABC
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

log = logging.getLogger(__name__)

MAX_NUMBER = 999_999_999_999

LAST_DIGIT_DEVISOR = 10


def _get_case_group(number: int) -> CaseGroup:
    tens = number % Factor.HUNDRED
    unit = number % Factor.TEN

    if tens in CaseGroup.OTHER:
        # Include: 5, ..., 20
        # Tens compared before units because it
        # contains: 11, ..., 14
        return CaseGroup.OTHER

    elif unit in CaseGroup.UNITS:
        # Include: 2, 3, 4, 22, 23, 24, 32, 33, 34, etc
        return CaseGroup.UNITS

    elif unit in CaseGroup.FIRST:
        # Include: 1, 21, 31, etc
        return CaseGroup.FIRST

    else:
        # Include: 25, ..., 30, 35, ..., 40, etc
        return CaseGroup.OTHER


class _NumberConverter(NumberConverterABC):
    """The converter of integer to numeral."""

    def __init__(
        self,
        number_mapping: dict[int, Case],
    ) -> None:
        """Construct the converter."""
        self._number_mapping = number_mapping

    def get_text(self, number: int, gender: GenderType, case: CaseType) -> str:
        """Get the text representation of number."""
        cases = self._number_mapping.get(number)
        case_obj: Gender | str = getattr(cases, self._get_case(case))
        try:
            return str(getattr(case_obj, self._get_gender(gender)))
        except AttributeError:
            return str(case_obj)

    def _get_gender(self, value: GenderType) -> str:
        try:
            return GENDERS[value]
        except KeyError:
            log.exception(
                f"Error number converting, got unexpected '{value}' alias for "
                f'gender. Use {GenderType} aliases.'
            )
            raise

    def _get_case(self, value: CaseType) -> str:
        try:
            return CASES[value]
        except KeyError:
            log.exception(
                f"Error number converting, got unexpected '{value}' alias for "
                f'case. Use {CaseType} aliases.'
            )
            raise


def _validate_number(number: int) -> None:
    if number < 0 or number > MAX_NUMBER:
        msg = f'Error number converting, use 0 <= number < {MAX_NUMBER}'
        log.error(msg)
        raise ValueError(msg)

    if not isinstance(number, int):
        msg = f'Expected `int` number type, got `{type(number).__name__}`'
        log.error(msg)
        raise ValueError(msg)


def _get_hundreds_numerals(
    converter: NumberConverterABC,
    number: int,
    gender: GenderType,
    case: CaseType,
) -> str:
    """Get numerals in the thousand range.

    >>> from .numbers import numerals
    >>> converter = _NumberConverter(numerals)
    >>> _get_hundreds_numerals(converter, 31, 'M', 'G')
    'тридцати одного'
    >>> converter = _NumberConverter(numerals)
    >>> _get_hundreds_numerals(converter, 122, 'N', 'I')
    'ста двадцатью двумя'
    """
    if max_number := Factor.THOUSAND - 1 < number:
        msg = (
            f'The maximum allowed number value has been exceeded:'
            f'{number} > {max_number}'
        )
        log.error(msg)
        raise ValueError(msg)

    numerals: list[str] = []

    if hundreds := number // Factor.HUNDRED % LAST_DIGIT_DEVISOR:
        numerals.append(
            converter.get_text(
                hundreds * Factor.HUNDRED,
                gender,
                case,
            )
        )

    if tens := number // Factor.TEN % LAST_DIGIT_DEVISOR:
        if tens == 1:
            numerals.append(
                converter.get_text(number % Factor.HUNDRED, gender, case)
            )
            return ' '.join(numerals)
        else:
            numerals.append(
                converter.get_text(tens * Factor.TEN, gender, case)
            )

    if unit := number % LAST_DIGIT_DEVISOR:
        numerals.append(converter.get_text(unit, gender, case))

    return ' '.join(numerals)


class _PeriodConvertor(PeriodConvertorABC):
    """The converter of number period to numeral."""

    def __init__(
        self,
        period_mapping: dict[Factor, dict[CaseGroup, Case]],
    ) -> None:
        """Construct the convector."""
        self._period = period_mapping

    def get_text(
        self,
        number: int,
        case: CaseType,
        range_name: Factor,
    ) -> str:
        """Get the number period numeral."""
        thousand_group = _get_case_group(number)
        numeral_case = self._period[range_name][thousand_group]
        numeral = getattr(numeral_case, CASES[case])

        if isinstance(numeral, str):
            return numeral
        else:
            msg = f'Expected `str` type, got {type(numeral).__name__}'
            log.error(msg)
            raise TypeError(msg)


def _convert_number(
    number: int,
    gender: GenderType,
    case: CaseType,
    number_converter: NumberConverterABC,
    range_converter: PeriodConvertorABC,
) -> str:
    """Return the word representation of number."""
    _validate_number(number)
    number_ = number
    factor_exponent = -1
    numerals: list[str] = []

    while number_:
        digits = number_ % Factor.THOUSAND
        number_ //= Factor.THOUSAND
        factor_exponent += 1
        factor = Factor(Factor.THOUSAND**factor_exponent)

        if not digits:
            continue
        else:
            digits_numerals = _get_hundreds_numerals(
                number_converter,
                digits,
                gender=gender
                if factor != Factor.THOUSAND
                else Factor.THOUSAND.gender,
                case=case,
            )
            numerals.insert(0, digits_numerals)

        if factor >= Factor.THOUSAND:
            range_numeral = range_converter.get_text(digits, case, factor)
            numerals.insert(1, range_numeral)

    return ' '.join(numerals)
