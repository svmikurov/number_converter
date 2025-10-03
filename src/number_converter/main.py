"""Function for converting an integer to text in words."""

import logging

from .base import NumberConverterABC, PeriodConvertorABC
from .types import (
    CASES,
    GENDERS,
    Case,
    CaseType,
    Gender,
    GenderType,
    ThousandGroup,
)

log = logging.getLogger(__name__)

MAX_NUMBER = 999_999_999_999

RANGE_TEN = 10
RANGE_HUNDRED = 100
RANGE_THOUSAND = 1_000

LAST_DIGIT_DEVISOR = 10


class _NumberConverter(NumberConverterABC):
    """The converter of integer to numeral."""

    def __init__(
        self,
        gender: GenderType,
        case: CaseType,
        number_mapping: dict[int, Case],
    ) -> None:
        """Construct the converter."""
        self._gender = self._set_gender(gender)
        self._case = self._set_case(case)
        self._number_mapping = number_mapping

    def get_text(self, number: int) -> str:
        """Get the text representation of number."""
        cases = self._number_mapping.get(number)
        case: Gender | str = getattr(cases, self._case)
        try:
            return str(getattr(case, self._gender))
        except AttributeError:
            return str(case)

    def _set_gender(self, value: GenderType) -> str:
        try:
            return GENDERS[value]
        except KeyError:
            log.exception(
                f"Error number converting, got unexpected '{value}' alias for "
                f'gender. Use {GenderType} aliases.'
            )
            raise

    def _set_case(self, value: CaseType) -> str:
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


def _get_hundreds_numerals(converter: NumberConverterABC, number: int) -> str:
    """Get numerals in the thousand range.

    >>> from .numbers import numerals
    >>> converter = _NumberConverter('M', 'G', numerals)
    >>> _get_hundreds_numerals(converter, 31)
    'тридцати одного'
    >>> converter = _NumberConverter('N', 'I', numerals)
    >>> _get_hundreds_numerals(converter, 122)
    'ста двадцатью двумя'
    """
    if max_number := RANGE_THOUSAND - 1 < number:
        msg = (
            f'The maximum allowed number value has been exceeded:'
            f'{number} > {max_number}'
        )
        log.error(msg)
        raise ValueError(msg)

    numerals: list[str] = []

    if hundreds := number // RANGE_HUNDRED % LAST_DIGIT_DEVISOR:
        numerals.append(converter.get_text(hundreds * RANGE_HUNDRED))

    if tens := number // RANGE_TEN % LAST_DIGIT_DEVISOR:
        if tens == 1:
            numerals.append(converter.get_text(number % RANGE_HUNDRED))
            return ' '.join(numerals)
        else:
            numerals.append(converter.get_text(tens * RANGE_TEN))

    if unit := number % LAST_DIGIT_DEVISOR:
        numerals.append(converter.get_text(unit))

    return ' '.join(numerals)


class _PeriodConvertor(PeriodConvertorABC):
    """The converter of number period to numeral."""

    def __init__(
        self,
        period_mapping: dict[ThousandGroup, Case],
    ) -> None:
        """Construct the convector."""
        self._period_mapping = period_mapping

    def get_text(self, number: int, case: CaseType) -> str:
        """Get the number period numeral."""
        thousand_group = self._get_thousand_group(number)
        numeral_case = self._period_mapping[thousand_group]
        numeral = getattr(numeral_case, CASES[case])

        if isinstance(numeral, str):
            return numeral
        else:
            msg = f'Expected `str` type, got {type(numeral).__name__}'
            log.error(msg)
            raise TypeError(msg)

    @staticmethod
    def _get_thousand_group(number: int) -> ThousandGroup:
        tens = number % RANGE_HUNDRED
        unit = number % RANGE_TEN

        if tens in ThousandGroup.OTHER:
            # Include: 5, ..., 20
            # It is compared before units because it
            # contains: 11, ..., 14
            return ThousandGroup.OTHER

        elif unit in ThousandGroup.UNITS:
            # Include: 2, 3, 4, 22, 23, 24, 32, ...
            return ThousandGroup.UNITS

        elif unit in ThousandGroup.FIRST:
            # Include: 1, 21, 31, ...
            return ThousandGroup.FIRST

        else:
            # Include: 25, ..., 30, 35, ...
            return ThousandGroup.OTHER


def _convert_number(
    number: int,
    gender: GenderType,
    case: CaseType,
    period_convertor: PeriodConvertorABC,
    number_mapping: dict[int, Case],
) -> str:
    """Return the word representation of number."""
    _validate_number(number)
    number_ = number
    number_converter = _NumberConverter(gender, case, number_mapping)
    part_count = 0
    numeral_parts: list[str] = []

    while number_:
        number_part = number_ % RANGE_THOUSAND

        if numeral_part := _get_hundreds_numerals(
            number_converter, number_part
        ):
            numeral_parts.insert(0, numeral_part)

        number_period = RANGE_THOUSAND**part_count

        if number_period == RANGE_THOUSAND:
            period_numeral = period_convertor.get_text(number_part, case)
            numeral_parts.insert(1, period_numeral)

        number_ //= RANGE_THOUSAND
        part_count += 1

    return ' '.join(numeral_parts)
