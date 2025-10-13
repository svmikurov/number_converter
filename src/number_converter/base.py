"""Abstract base classes for number conversion components."""

from abc import ABC, abstractmethod

from .types import CaseType, Factor, GenderType


class NumberConverterABC(ABC):
    """The converter of integer to numeral."""

    @abstractmethod
    def get_numeral(
        self,
        case_number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get the text representation of number."""

    @abstractmethod
    def get_text(
        self,
        number: int,
        gender: GenderType,
        case: CaseType,
    ) -> str:
        """Get numeral in the thousand factor."""


class FactorConverterABC(ABC):
    """The converter of number factor to numeral."""

    @abstractmethod
    def get_text(
        self,
        number: int,
        case: CaseType,
        factor: Factor,
    ) -> str:
        """Get the number factor numeral."""
