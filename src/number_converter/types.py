"""Library types."""

from enum import Enum
from typing import Literal, NamedTuple

# The function accepts grammatical gender and case aliases
# to convert a number to a text.
GenderType = Literal['M', 'F', 'N']
CaseType = Literal['N', 'G', 'D', 'A', 'I', 'P']

GENDERS: dict[GenderType, str] = {
    'M': 'masculine',
    'F': 'feminine',
    'N': 'neuter',
}
CASES: dict[CaseType, str] = {
    'N': 'nominative',
    'G': 'genitive',
    'D': 'dative',
    'A': 'accusative',
    'I': 'instrumental',
    'P': 'prepositional',
}


class Gender(NamedTuple):
    """Grammatical gender presentation of number."""

    masculine: str
    feminine: str
    neuter: str


class Case(NamedTuple):
    """Declension of number by case."""

    nominative: Gender | str
    genitive: Gender | str
    dative: Gender | str
    accusative: Gender | str
    instrumental: Gender | str
    prepositional: Gender | str


class Factor(int, Enum):
    """Enumeration of number factors for numeral conversion."""

    UNITS = 1
    TENS = 10
    HUNDREDS = 10**2
    THOUSANDS = 10**3
    MILLIONS = 10**6
    BILLIONS = 10**9

    @property
    def gender(self) -> GenderType:
        """Get grammatical gender of the factor name."""
        genders: dict[Factor, GenderType] = {
            Factor.UNITS: 'M',
            Factor.TENS: 'M',
            Factor.HUNDREDS: 'M',
            Factor.THOUSANDS: 'F',
            Factor.MILLIONS: 'M',
            Factor.BILLIONS: 'M',
        }
        return genders[self]


class CaseGroup(Enum):
    """Enumeration of grammatical cases.

    Enumerations contain the last digits of the number,
    which affect the declension.
    """

    FIRST = {1}
    UNITS = {2, 3, 4}
    OTHER = set(range(5, 21))

    def __contains__(self, number: int) -> bool:
        """Return True if item is contained in the enumeration."""
        return number in self.value

    @classmethod
    def from_number(cls, number: int) -> 'CaseGroup':
        """Get case group."""
        tens = number % Factor.HUNDREDS
        unit = number % Factor.TENS

        if tens in CaseGroup.OTHER:
            # Include: 5, ..., 20.
            # Tens compared before units because it
            # contains: 11, ..., 14.
            return cls.OTHER

        elif unit in CaseGroup.UNITS:
            # Include: 2, 3, 4, 22, 23, 24, 32, 33, 34, etc.
            return cls.UNITS

        elif unit in CaseGroup.FIRST:
            # Include: 1, 21, 31, etc.
            return cls.FIRST

        else:
            # Include: 25, ..., 30, 35, ..., 40, etc.
            return cls.OTHER
