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

    ONE = 1
    TEN = 10
    HUNDRED = 10**2
    THOUSAND = 10**3
    MILLION = 10**6
    BILLION = 10**9

    @property
    def gender(self) -> GenderType:
        """Get grammatical gender of the factor name."""
        genders: dict[Factor, GenderType] = {
            Factor.ONE: 'M',
            Factor.TEN: 'M',
            Factor.HUNDRED: 'M',
            Factor.THOUSAND: 'F',
            Factor.MILLION: 'M',
            Factor.BILLION: 'M',
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

    def __contains__(self, item: int) -> bool:
        """Return True if item is contained in the enumeration."""
        return item in self.value
