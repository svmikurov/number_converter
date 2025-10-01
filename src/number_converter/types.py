"""Library types."""

from typing import Literal, NamedTuple

# The function accepts gender and case aliases
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
    """Gender presentation of number."""

    masculine: str
    feminine: str
    neuter: str


class Case(NamedTuple):
    """Declension of number by case."""

    nominative: Gender
    genitive: Gender
    dative: Gender
    accusative: Gender
    instrumental: Gender
    prepositional: Gender
